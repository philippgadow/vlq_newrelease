#!/usr/bin/env python

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from argparse import ArgumentParser
from os.path import join
from AnaAlgorithm.AnaAlgSequence import AnaAlgSequence
from AnaAlgorithm.DualUseConfig import createAlgorithm
from AnaAlgorithm.DualUseConfig import addPrivateTool
from AnaAlgorithm.DualUseConfig import createService


# Read the submission directory as a command line argument. You can
# extend the list of arguments with your private ones later on.
parser = ArgumentParser()
parser.add_argument('-s', '--submission_dir', default='submitDir',
                    help='Submission directory for EventLoop')
parser.add_argument('-i', '--input_dir',
                    default='/nfs/dust/atlas/user/pgadow/MC/TRUTH/',
                    help='Input directory to be scanned for samples')
parser.add_argument('--dsid_pattern', help='Pattern to be contained within DSID.')
args = parser.parse_args()

# Set up (Py)ROOT for xAOD access
ROOT.xAOD.Init().ignore()

# Set up the sample handler object. See comments from the C++ macro
# for the details about these lines.
sh = ROOT.SH.SampleHandler()
sh.setMetaString( 'nc_tree', 'CollectionTree' )
inputFilePath = args.input_dir
ROOT.SH.ScanDir().samplePattern(args.dsid_pattern + "*").filePattern('DAOD_TRUTH1.mc16_13TeV.*.root').scan(sh, inputFilePath)
sh.printContent()

# Create an EventLoop job.
job = ROOT.EL.Job()
job.sampleHandler(sh)
job.options().setDouble(ROOT.EL.Job.optMaxEvents, 10000)
job.options().setString(ROOT.EL.Job.optSubmitDirMode, 'unique-link')

# Create the analysis algorithm sequence object + register systematics
algSequence = AnaAlgSequence("TruthAnalysisSequence")
sysService = createService('CP::SystematicsSvc', 'SystematicsSvc', sequence=algSequence)
sysService.sigmaRecommended = 1

# Event weight algorithm:
# provides event weights as generatorWeight_%SYS% decorators to EventInfo
alg = createAlgorithm('CP::PMGTruthWeightAlg', 'PMGTruthWeightAlg')
addPrivateTool(alg, 'truthWeightTool', 'PMGTools::PMGTruthWeightTool')
alg.decoration = 'generatorWeight_%SYS%'
algSequence.append(alg, inputPropName=None)

# Truth Analysis algorithm:
# extracts mtt
alg = createAlgorithm ('TruthAnalysis', 'AnalysisAlg')
algSequence.append(alg, inputPropName=None)

# Schedule output
treeName = 'truth'
treeMaker = createAlgorithm('CP::TreeMakerAlg', 'TreeMaker')
treeMaker.TreeName = treeName
algSequence += treeMaker
# Add truth event weights from reweighting and event-level mtt variable
ntupleMaker = createAlgorithm('CP::AsgxAODNTupleMakerAlg', 'NTupleMakerEventInfo')
ntupleMaker.TreeName = treeName
ntupleMaker.Branches = [
    'EventInfo.ev_m_Hb_max           -> m_Hb_max',
    'EventInfo.ev_m_Hb_highpt        -> ev_m_Hb_highpt',
    'EventInfo.generatorWeight_%SYS% -> generatorWeight_%SYS%'
]
algSequence += ntupleMaker
# Write to tree
treeFiller = createAlgorithm('CP::TreeFillerAlg', 'TreeFiller')
treeFiller.TreeName = treeName
algSequence += treeFiller

# Add our algorithm to the job
for alg in algSequence:
    job.algsAdd(alg)

# Output
job.outputAdd(ROOT.EL.OutputStream('ANALYSIS'))

# Run the job using the direct driver.
driver = ROOT.EL.DirectDriver()
driver.submit(job, args.submission_dir)
