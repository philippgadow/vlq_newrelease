from MadGraphControl.MadGraphUtils import *
import MadGraphControl.MadGraphUtils
import re
import subprocess
import sys

# event configuration
evgenConfig.nEventsPerJob = 10000
# VLQ PDGID map
vlq_ids = {'X':"6000005", 'T':"6000006", 'B':"6000007", 'Y':"6000008"}
# get additional python modules
get_vlqcoupling = subprocess.Popen(['get_files', '-jo', 'VLQCouplingCalculator_v2.py'])
if get_vlqcoupling.wait():
    print "Could not copy VLQCouplingCalculator_v2.py"
    sys.exit(2)

get_lhehacker = subprocess.Popen(['get_files', '-jo', 'lhe_hacker_v2.py'])
if get_lhehacker.wait():
    print "Could not copy lhe_hacker_v2.py"
    sys.exit(2)

from VLQCouplingCalculator_v2 import *
from lhe_hacker_v2 import *

################################################################################
'''
Block kblh
    1 0.000000e+01 # KBLh1
    2 0.000000e+01 # KBLh2
    3 6.391170e-01 # KBLh3

###################################
## INFORMATION FOR KBLW
###################################
Block kblw
    1 0.000000e+01 # KBLw1
    2 0.000000e+01 # KBLw2
    3 1.601490e-01 # KBLw3

###################################
## INFORMATION FOR KBLZ
###################################
Block kblz
    1 0.000000e+01 # KBLz1
    2 0.000000e+01 # KBLz2
    3 2.403790e-01 # KBLz3

###################################
## INFORMATION FOR KBRH
###################################
Block kbrh
    1 0.000000e+00 # KBRh1
    2 0.000000e+00 # KBRh2
    3 0.000000e+00 # KBRh3

###################################
## INFORMATION FOR KBRW
###################################
Block kbrw
    1 0.000000e+00 # KBRw1
    2 0.000000e+00 # KBRw2
    3 0.000000e+00 # KBRw3

###################################
## INFORMATION FOR KBRZ
###################################
Block kbrz
    1 0.000000e+00 # KBRz1
    2 0.000000e+00 # KBRz2
    3 0.000000e+00 # KBRz3

###################################
## INFORMATION FOR KTLH
###################################
Block ktlh
    1 0.000000e+01 # KTLh1
    2 0.000000e+01 # KTLh2
    3 0.5 # KTLh3

###################################
## INFORMATION FOR KTLW
###################################
Block ktlw
    1 0.000000e+01 # KTLw1
    2 0.000000e+01 # KTLw2
    3 5.0e-01 # KTLw3

###################################
## INFORMATION FOR KTLZ
###################################
Block ktlz
    1 0.000000e+01 # KTLz1
    2 0.000000e+01 # KTLz2
    3 5.0e-01 # KTLz3

###################################
## INFORMATION FOR KTRH
###################################
Block ktrh
    1 0.000000e+00 # KTRh1
    2 0.000000e+00 # KTRh2
    3 0.000000e+00 # KTRh3

###################################
## INFORMATION FOR KTRW
###################################
Block ktrw
    1 0.000000e+00 # KTRw1
    2 0.000000e+00 # KTRw2
    3 0.000000e+00 # KTRw3

###################################
## INFORMATION FOR KTRZ
###################################
Block ktrz
    1 0.000000e+00 # KTRz1
    2 0.000000e+00 # KTRz2
    3 0.000000e+00 # KTRz3

###################################
## INFORMATION FOR KXLW
###################################
Block kxlw
    1 0.000000e+01 # KXL1
    2 0.000000e+01 # KXL2
    3 4.003790e-01 # KXL3

###################################
## INFORMATION FOR KXRW
###################################
Block kxrw
    1 0.000000e+00 # KXR1
    2 0.000000e+00 # KXR2
    3 0.000000e+00 # KXR3

###################################
## INFORMATION FOR KYLW
###################################
Block kylw
    1 0.000000e+01 # KYL1
    2 0.000000e+01 # KYL2
    3 4.003790e-01 # KYL3

###################################
## INFORMATION FOR KYRW
###################################
Block kyrw
    1 0.000000e+00 # KYR1
    2 0.000000e+00 # KYR2
    3 0.000000e+00 # KYR3

###################################
## INFORMATION FOR LOOP
###################################
Block loop
    1 9.118800e+01 # MU_R

###################################
## INFORMATION FOR MASS
###################################
Block mass
    5 4.700000e+00 # MB
    6 1.720000e+02 # MT
   15 1.777000e+00 # MTA
   23 9.118760e+01 # MZ
   25 1.250000e+02 # MH
  6000005 6.000000e+02 # MX
  6000006 1.400000e+03 # MTP
  6000007 6.000000e+02 # MBP
  6000008 6.000000e+02 # MY

###################################
## INFORMATION FOR DECAY
###################################
DECAY   6 1.508336e+00 # WT
DECAY  23 2.495200e+00 # WZ
DECAY  24 2.085000e+00 # WW
DECAY  25 4.070000e-03 # WH
DECAY 6000005 Auto # WX
DECAY 6000006 Auto # WTP
DECAY 6000007 Auto # WBP
DECAY 6000008 Auto # WY
'''
##################################################################################

#### Some Variables
MAX_TRIAL = 1     ## Maximum number of trials allowed for failures in event generation or reweighting
SAFE_FACTOR = 1.1  ## Number of events generated = SAFE_FACTOR * max_events
runName='run_01'   ## Run name for event generation

#### Process Descriptions with Full VLQ Decay Chain
#### Implements complete decay chain of immediate daughter particles of the VLQs
#### Higgs decay is not implemented here, taken care of in Pythia


all_VLQ_processes_fulldecay = {
    'WXWt':'''add process p p > j x t~ / tp tp~ p b b~ y y~ bp bp~ x x~ z h a, (t~ > ferm ferm b~), (x > w+ t, w+ > ferm ferm, t > ferm ferm b)
              add process p p > j x~ t / tp tp~ p b b~ y y~ bp bp~ x x~ z h a, (t > ferm ferm b), (x~ > w- t~, w- > ferm ferm, t~ > ferm ferm b~)''',
    'WTWb':'add process p p > j TPTP bb / tp tp~ p t t~ y y~ bp bp~ x x~ z h a, (TPTP > WW bb, WW > ferm ferm)',
    'WTZt':'add process p p > j TPTP bb / tp tp~ p t t~ y y~ bp bp~ x x~ z h a, (TPTP > z tt, z > ferm ferm, tt > ferm ferm bb)',
    'WTHt':'add process p p > j TPTP bb / tp tp~ p t t~ y y~ bp bp~ x x~ z h a, (TPTP > h tt, tt > ferm ferm bb)',
    'ZTWb':'''add process p p > j TPTP tt / tp tp~ p b b~ y y~ bp bp~ x x~ w+ w- h a, (tt > ferm ferm bb), (TPTP > WW bb, WW > ferm ferm)''',
    'ZTZt':'''generate p p > j z t t~ / p y y~ bp bp~ x x~ w+ w- h a VLQ=2 QED=1 QCD=1, (t~ > ferm ferm b~), (z > ferm ferm), (t > ferm ferm b)''',
    'ZTHt':'''add process p p > j h t t~ /p y y~ bp bp~ x x~ w+ w- h a VLQ=2 QED=1 QCD=1, (t~ > ferm ferm b~), (t > ferm ferm b)''',
    'WBWt':'''add process p p > j bp t~ / tp tp~ p b b~ y y~ bp bp~ x x~ z h a, (t~ > ferm ferm b~), (bp > w- t, w- > ferm ferm, t > ferm ferm b)
              add process p p > j bp~ t / tp tp~ p b b~ y y~ bp bp~ x x~ z h a, (t > ferm ferm b), (bp~ > w+ t~, w+ > ferm ferm, t~ > ferm ferm b~)''',
    'WBZb':'''add process p p > j BPBP tt / tp tp~ p b b~ y y~ bp bp~ x x~ z h a, (tt > ferm ferm bb), (BPBP > z bb, z > ferm ferm)''',
    'WBHb': '''generate  p p > j bb h tt /tp tp~ p y y~ x x~ z h a VLQ=2 QED=1 QCD=1, tt > ferm ferm bb''',
    'ZBWt':'''add process p p > j bp b~ / tp tp~ p t t~ y y~ bp bp~ x x~ w+ w- h a, (bp > w- t, w- > ferm ferm, t > ferm ferm b)
              add process p p > j bp~ b / tp tp~ p t t~ y y~ bp bp~ x x~ w+ w- h a, (bp~ > w+ t~, w+ > ferm ferm, t~ > ferm ferm b~)''',
    'ZBZb':'''add process p p > j bp b~ / tp tp~ p t t~ y y~ bp bp~ x x~ w+ w- h a, (bp > z b, z > ferm ferm)
              add process p p > j bp~ b / tp tp~ p t t~ y y~ bp bp~ x x~ w+ w- h a, (bp~ > z b~, z > ferm ferm)''',
    'ZBHb':'''generate  p p > j b~ h b /tp tp~ p t t~ y y~ x x~ w+ w- h a VLQ==2 QED=1''',
    'WYWb':'''add process p p > j y b~ / tp tp~ p t t~ y y~ bp bp~ x x~ w+ w- h a, (y > w- b, w- > ferm ferm)
              add process p p > j y~ b / tp tp~ p t t~ y y~ bp bp~ x x~ w+ w- h a, (y~ > w+  b~, w+ > ferm ferm)''',
}


#### Process Descriptions with Min VLQ Decay Chain
#### Implements decay of VLQs to immediate daughters only

all_VLQ_processes_mindecay = {
    'WXWt':'''add process p p > j x t~ / tp tp~ p b b~ y y~ bp bp~ x x~ z h a, (x > w+ t)
              add process p p > j x~ t / tp tp~ p b b~ y y~ bp bp~ x x~ z h a, (x~ > w- t~)''',
    'WTWb':'add process p p > j TPTP bb / tp tp~ p t t~ y y~ bp bp~ x x~ z h a, (TPTP > WW bb)',
    'WTZt':'add process p p > j TPTP bb / tp tp~ p t t~ y y~ bp bp~ x x~ z h a, (TPTP > z tt)',
    'WTHt':'add process p p > j TPTP bb / tp tp~ p t t~ y y~ bp bp~ x x~ z h a, (TPTP > h tt)',
    'ZTWb':'''add process p p > j TPTP tt / tp tp~ p b b~ y y~ bp bp~ x x~ w+ w- h a, (TPTP > WW bb)''',
    'ZTZt':'''generate p p > j z t t~ / p y y~ bp bp~ x x~ w+ w- h a VLQ=2 QED=1 QCD=1''',
    'ZTHt':'''add process p p > j h t t~ / p y y~ bp bp~ x x~ w+ w- h a VLQ=2 QED=1 QCD=1''',
    'WBWt':'''add process p p > j bp t~ / tp tp~ p b b~ y y~ bp bp~ x x~ z h a, (bp > w- t)
              add process p p > j bp~ t / tp tp~ p b b~ y y~ bp bp~ x x~ z h a, (bp~ > w+ t~)''',
    'WBZb':'''add process p p > j BPBP tt / tp tp~ p b b~ y y~ bp bp~ x x~ z h a, (BPBP > z bb)''',
    'WBHb': '''generate  p p > j bb h tt /tp tp~ p y y~ x x~ z h a VLQ=2 QED=1 QCD=1''',
    'ZBWt':'''add process p p > j bp b~ / tp tp~ p t t~ y y~ bp bp~ x x~ w+ w- h a, (bp > w- t)
              add process p p > j bp~ b / tp tp~ p t t~ y y~ bp bp~ x x~ w+ w- h a, (bp~ > w+ t~)''',
    'ZBZb':'''add process p p > j bp b~ / tp tp~ p t t~ y y~ bp bp~ x x~ w+ w- h a, (bp > z b)
              add process p p > j bp~ b / tp tp~ p t t~ y y~ bp bp~ x x~ w+ w- h a, (bp~ > z b~)''',
    'WYWb':'''add process p p > j y b~ / tp tp~ p t t~ y y~ bp bp~ x x~ w+ w- h a, (y > w- b)
              add process p p > j y~ b / tp tp~ p t t~ y y~ bp bp~ x x~ w+ w- h a, (y~ > w+ b~)''',
}

#### Additional parameters to build the run card
if hasattr(runArgs,'ecmEnergy'):
    beamEnergy = runArgs.ecmEnergy / 2.
else:
    beamEnergy = 6500.

extras = { 'nevents': evgenConfig.nEventsPerJob * SAFE_FACTOR,
           'iseed': str(runArgs.randomSeed),
           'xqcut': "0.",
           'lhe_version'   : '3.0',
           'cut_decays'    : 'F',
           'bwcutoff'      : '10000',
           'event_norm'    : 'average',
           'drjj'          :  -1.0,
           'drll'          :  -1.0,
           'draa'          :  -1.0,
           'draj'          :  -1.0,
           'drjl'          :  -1.0,
           'dral'          :  -1.0,
           'etal'          :  -1.0,
           'etaj'          :  -1.0,
           'etaa'          :  -1.0,
}

#### PDF definition
#### - use LO 4FS PDF: 263400 - NNPDF30_lo_as_0130_nf_4
#### - alternative PDFs for systematic variations: 262400 - NNPDF30_lo_as_0118_nf_4 and 13202 - CT14lo_NF4
MadGraphControl.MadGraphUtils.MADGRAPH_PDFSETTING={
    'central_pdf':263400, # the lhapf id of the central pdf, see https://lhapdf.hepforge.org/pdfsets
    'pdf_variations':[263400], # pdfs for which all variations (error sets) will be included as weights
    'alternative_pdfs':[262400,13202], # pdfs for which only the central set will be included as weights
    'scale_variations':[0.5,1.,2.], # variations of muR and muF wrt the central scale, all combinations of muF and muR will be evaluated
    'use_syst': True,
}


#### Find the process details from top level JobOption

def findprocdetails():

    '''
    The Top level JO should have a name of the following form:

    mc.MGPy8EG_${PROC}${MASS}${CHIRALITY}${COUPLING}${FLAGS}.py

    PROC: Single VLQ process in the VQAq form (e.g. WTHt, ZBHb)
    MASS: Pole mass of VLQ in GeV
    CHIRALITY: LH or RH
    COUPLING: Value of Kappa*100, formatted with preceeding zeros if needed. (e.g. '035' represents kappa = 0.35
    FLAGS: Other essential flags
           _sigonly -> allows event generation for particles only
           _sigbaronly -> allows event generation for anti-particles only
           _norwt -> Reweighting is not applied
           _hyy -> Higgs BR to photons 100%
    '''

    THIS_DIR = (os.environ['JOBOPTSEARCHPATH']).split(":")[0]
    jobname = [f for f in os.listdir(THIS_DIR) if (f.startswith('mc') and f.endswith('.py'))][0]
    for proc in all_VLQ_processes_fulldecay.keys():
        if proc in jobname:
            process = proc
            break
    ProdMode = process[0]
    VLQMode = process[1]
    DecayMode = process[2]

    if 'LH' in jobname: chirality = 'LH'
    elif 'RH' in jobname: chirality = 'RH'

    Mass = int(re.findall(r'\d+',re.findall(r'\d+' + chirality,jobname)[0])[0])*1.0
    Kappa = int(re.findall(r'\d+', jobname)[-1])*0.01

    if '_sigbaronly' in jobname: doSig, doSigbar = False, True
    elif '_sigonly'  in jobname: doSig, doSigbar = True,  False
    else: doSig, doSigbar = True, True

    dorwt = ('_norwt' not in jobname)
    doHiggsyy = ('_hyy' in jobname)

    return VLQMode, ProdMode, DecayMode, process, chirality, Mass, Kappa, doSig, doSigbar, dorwt, doHiggsyy


## Creates the process strings necessary for creating the process_dir. fcardmode = fulldecay or mindecay

def processmaker(processmode='fulldecay'):
    if processmode == 'mindecay':
        procmap_to_use = all_VLQ_processes_mindecay
    else:
        procmap_to_use = all_VLQ_processes_fulldecay

    this_procs = procmap_to_use[runArgs.vlqprocess].split('\n')

    if len(this_procs) > 1 and not runArgs.dosigbar:
        proc_to_use = this_procs[0].strip() + '\n'
    elif len(this_procs) > 1 and not runArgs.dosig:
        proc_to_use = this_procs[1].strip() + '\n'
    else:
        proc_to_use = ""
        for ii in range(len(this_procs)): proc_to_use += this_procs[ii].strip() + '\n'
    process = "set zerowidth_tchannel False\n"
    process += "import model /cvmfs/atlas.cern.ch/repo/sw/Generators/madgraph/models/latest/VLQ_v4_4FNS_UFO-3rd\n"
    process += "define p = g u c d s u~ c~ d~ s~\n"
    process += "define j = g u c d s u~ c~ d~ s~\n"
    process += "define bb = b b~\n"
    process += "define WW = w+ w-\n"
    process += "define tt = t t~\n"
    process += "define ferm = ve vm vt ve~ vm~ vt~ mu- ta- e- mu+ ta+ e+ u c d s b u~ c~ d~ s~ b~\n"
    process += "define TPTP = tp tp~\n"
    process += "define BPBP = bp bp~\n"
    process += "define XX = x x~\n"
    process += "define YY = y y~\n"
    process += proc_to_use
    process += "output -f"
    return process

#### Creates the param card dictionary based on the process details
#### Currently only assumes only third generation couplings

def paramdictmaker():
    chiralityIndex = runArgs.chirality.replace('H','')
    all_blocks = ["k"+a+b+c for a in ["t","b"] for b in ["l","r"] for c in ["w", "h", "z"]] + ["k"+a+b+"w" for a in ["y","x"] for b in ["l","r"]]
    all_vars = ["K"+a+b+c+d for a in ["T","B"] for b in ["L","R"] for c in ["w", "h", "z"] for d in ["1","2","3"]] + ["K"+a+b+d for a in ["Y","X"] for b in ["L","R"] for d in ["1","2","3"]]

    paramdict = {}
    for block in ['mass', 'decay'] + all_blocks:
        paramdict[block] = {}
    
    for vlqmode in vlq_ids.keys():
        paramdict['mass'][vlq_ids[vlqmode]] = str(runArgs.mass)
        paramdict['decay'][vlq_ids[vlqmode]] = str(runArgs.gamma)

    if runArgs.vlqmode in ['X', 'Y']:
        paramdict['k'+runArgs.vlqmode.lower()+chiralityIndex.lower()+'w']['K' + runArgs.vlqmode + chiralityIndex + '3'] = str(runArgs.kw)
    else:
        paramdict['k'+runArgs.vlqmode.lower()+chiralityIndex.lower()+'w']['K' + runArgs.vlqmode + chiralityIndex + 'w3'] = str(runArgs.kw)
        paramdict['k'+runArgs.vlqmode.lower()+chiralityIndex.lower()+'z']['K' + runArgs.vlqmode + chiralityIndex + 'z3'] = str(runArgs.kz)
        paramdict['k'+runArgs.vlqmode.lower()+chiralityIndex.lower()+'h']['K' + runArgs.vlqmode + chiralityIndex + 'h3'] = str(runArgs.kh)

    return paramdict


def Vars():
    chiralityIndex = runArgs.chirality.replace('H','')
    all_vars = ["K"+a+b+c+d for a in ["T","B"] for b in ["L","R"] for c in ["w", "h", "z"] for d in ["1","2","3"]] + ["K"+a+b+d for a in ["Y","X"] for b in ["L","R"] for d in ["1","2","3"]]
    if runArgs.vlqmode in ['X', 'Y']:
        vars_to_change = ['M' + runArgs.vlqmode,
                          'W' + runArgs.vlqmode,
                          'K' + runArgs.vlqmode + chiralityIndex + '3']
    else:
        vars_to_change = ['M' + runArgs.vlqmode + 'P',
                          'W' + runArgs.vlqmode + 'P',
                          'K' + runArgs.vlqmode + chiralityIndex + 'w3',
                          'K' + runArgs.vlqmode + chiralityIndex + 'z3',
                          'K' + runArgs.vlqmode + chiralityIndex + 'h3']
    return  vars_to_change

#### makes a reweight card based for an input choice of mass and coupling grid

def rewtcardmaker(ms, Ks, process_dir):
    tagnames = []
    launch_line = "launch --rwgt_name="
    f = open(process_dir + "/Cards/reweight_card.dat", "w")
    for m in ms:
        for K in Ks:
            tagname = 'M{:02d}K{:03d}'.format(int(m/100), int(K*100))
            tagnames.append(tagname)
            print tagname
            c = VLQCouplingCalculator(float(m), runArgs.vlqmode)
            if runArgs.vlqmode in ['X', 'Y']:
                c.setKappaxi(K, 1.0, 0.0)
            else:
                c.setKappaxi(K, 0.5, 0.25)
            kappas = c.getKappas()
            gamma = c.getGamma()
            Modified_Vars = [float(m), gamma, kappas[0], kappas[1], kappas[2]]
            print K, gamma
            f.write(launch_line + tagname + '\n')
            for vlqmode in vlq_ids.keys():
                f.write('\tset MASS ' + vlq_ids[vlqmode] + ' ' + str(Modified_Vars[0]) + '\n')
                f.write('\tset DECAY ' + vlq_ids[vlqmode] + ' ' + str(Modified_Vars[1]) + '\n')
            for ii in range(len(paramlist)):
                if str(paramlist[ii])[0] not in ['M','W']:
                    f.write('\tset ' + str(paramlist[ii]) + ' ' + str(Modified_Vars[ii]) + '\n')
            f.write('\n\n')
    f.flush()
    f.close()
    return tagnames

runArgs.vlqmode, runArgs.prodmode, runArgs.decaymode, \
runArgs.vlqprocess, runArgs.chirality, runArgs.mass, \
runArgs.kappa, runArgs.dosig, runArgs.dosigbar, \
runArgs.dorwt, runArgs.doHiggsyy = findprocdetails()

M_grid = [runArgs.mass-100., runArgs.mass] ## Mass grid for reweighting
K_grid = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6] ## Kappa grid for reweighting
me_exec = os.environ['MADPATH'] + '/bin/mg5_aMC' ## MadGraph executable

if not os.access(me_exec, os.R_OK):
    print "mg5_aMC not located. Aborting!!"
    sys.exit(2)

c = VLQCouplingCalculator(runArgs.mass, runArgs.vlqmode)

if runArgs.vlqmode in ['X', 'Y']:
    c.setKappaxi(runArgs.kappa, 1.0, 0.0)
else:
    c.setKappaxi(runArgs.kappa, 0.5, 0.25)

[runArgs.kw, runArgs.kz, runArgs.kh, ks] = c.getKappas()
runArgs.gamma = c.getGamma()

print ("VLQ:   ", runArgs.vlqmode)
print ("Mass:  ", runArgs.mass)
print ("Kappa: ", runArgs.kappa)
print ("Process:  ", runArgs.vlqprocess)


#### Make the proc cards for full decay and min decay


process_fulldecay = processmaker('fulldecay')
paramlist = Vars()
params = paramdictmaker()
#### Process generation for full decay chain

process_dir_fullDecay = new_process(process_fulldecay)
modify_run_card(process_dir=process_dir_fullDecay, settings=extras)
modify_param_card(process_dir=process_dir_fullDecay, params=params)
MadGraphControl.MadGraphUtils.MADGRAPH_RUN_NAME = runName + "_fullDecay"

if runArgs.vlqprocess not in all_VLQ_processes_mindecay and runArgs.dorwt:
    tagnames = rewtcardmaker(M_grid, K_grid, process_dir_fullDecay)
    

generate(process_dir=process_dir_fullDecay, runArgs=runArgs)

if os.path.exists(process_dir_fullDecay + '/Events/' + runName + '_fullDecay/unweighted_events.lhe.gz') == False\
   and os.path.exists(process_dir_fullDecay + '/Events/' + runName + '_fullDecay/unweighted_events.lhe') == False:

    print "ERROR: Event Generation with full decay chain failed. Aborting!"
    sys.exit(2)


arrange_output(process_dir=process_dir_fullDecay, runArgs=runArgs, lhe_version=3, saveProcDir=True)

#### Start building the reweighting scenario

if runArgs.vlqprocess in all_VLQ_processes_mindecay and runArgs.dorwt:
    print "Reweighting is enabled\n\n\n"
    process_mindecay = processmaker('mindecay')
    process_dir_minDecay = new_process(process_mindecay)
    modify_run_card(process_dir=process_dir_minDecay, settings=extras)
    rewtcardmaker([runArgs.mass], [0.5], process_dir_minDecay) #### Make A Dummy Reweight Card to be used for reweighting with minDecay event generation
    modify_param_card(process_dir=process_dir_minDecay, params=params)
    MadGraphControl.MadGraphUtils.MADGRAPH_RUN_NAME = runName + "_minDecay"
    generate(process_dir=process_dir_minDecay, runArgs=runArgs)
    arrange_output(process_dir=process_dir_minDecay, runArgs=runArgs, lhe_version=3, saveProcDir=True)

    if os.path.exists(process_dir_minDecay + '/Events/' + runName + '_minDecay/unweighted_events.lhe.gz') == False\
       and os.path.exists(process_dir_minDecay + '/Events/' + runName + '_minDecay/unweighted_events.lhe') == False:

        print "ERROR: Event Generation with min decay chain failed. Aborting!"
        sys.exit(2)


    hack_status = lhe_hacker(lhe_minDecay  = process_dir_minDecay + '/Events/run_01_minDecay/unweighted_events.lhe',
                        lhe_fullDecay = process_dir_fullDecay + '/Events/run_01_fullDecay/unweighted_events.lhe',
                        vlq           = runArgs.vlqmode,
                        decay         = runArgs.decaymode)

    if hack_status :
        print " \n\n\n LHE Hacker was successful \n\n\n"
    else:
        print " \n\n\n LHE Hacker was NOT successful \n\n\n"
        sys.exit(1)

    placeback_status = False

    ME_script = open('script.txt','w')
    ME_script.write('''
    launch ''' + process_dir_minDecay + ''' -i
    reweight run_RWT
    ''')

    ME_script.flush()
    ME_script.close()
else:
    hack_status = False
    placeback_status = False

if hack_status and runArgs.dorwt:
    print "Starting Reweighting Sequence\n\n"
    subprocess.call('mkdir -p ' + process_dir_minDecay+'/Events/run_RWT/', shell=True)
    subprocess.call('cp unweighted_events.lhe ' + process_dir_minDecay+'/Events/run_RWT/', shell=True)
    tagnames = rewtcardmaker(M_grid, K_grid, process_dir_minDecay)
    did_it_work = False
    trial_count = 0
    while not did_it_work and trial_count < MAX_TRIAL:
        trial_count += 1
        reweight_now = subprocess.Popen(['python', me_exec, ' script.txt'])
        reweight_now.wait()
        sys.stdout.flush()
        try:
            subprocess.call('gunzip ' + process_dir_minDecay + '/Events/run_RWT/unweighted_events.lhe.gz', shell=True)
            print "found gzipped file in run_RWT and unzipped it"
        except:
            print "did not find gzipped file. Already unzipped?"
            pass
        for tagname in tagnames:
            did_it_work = False
            thisfile = open(process_dir_minDecay + '/Events/run_RWT/unweighted_events.lhe' , 'r')
            for line in thisfile:
                if "<weight id='" + tagname +"'" in line:
                    print tagname, " reweighting worked"
                    did_it_work = True
                    break
                else:
                    continue
            if not did_it_work:
                print tagname, " reweighting did not work. Retrying!"
                sys.stdout.flush()
                break
        sys.stdout.flush()

    if did_it_work:    
        placeback_status = placeback(lhe_fullDecay  = process_dir_fullDecay + '/Events/run_01_fullDecay/unweighted_events.lhe',
                                     lhe_reweighted = process_dir_minDecay  + '/Events/run_RWT/unweighted_events.lhe')
    else:
         placeback_status = False

    if placeback_status:
        print "Placeback Successful.\n\n\n"
        subprocess.call('tar -czf tmp_final_events.events.tar.gz tmp_final_events.events', shell=True)
    else:
        print "Placeback Unsuccessful.\n\n\n"
        sys.exit(2)

if not (hack_status and placeback_status):
    subprocess.call("cp tmp_LHE_events.events tmp_final_events.events", shell=True)
    subprocess.call('tar -czf tmp_final_events.events.tar.gz tmp_final_events.events', shell=True)

runArgs.inputGeneratorFile = 'tmp_final_events'


include("Pythia8_i/Pythia8_A14_NNPDF23LO_EvtGen_Common.py")
include("Pythia8_i/Pythia8_MadGraph.py")


# following example from
# https://gitlab.cern.ch/atlas-physics/pmg/infrastructure/mc15joboptions/-/blob/master/common/MadGraph/MadGraphControl_MGPy8EvGen_NNPDF30LO_A14NNPDF23LO_VLBSingle.py#L175
# set BR of H(yy) to 100%: turn off all h decays and then turn on only h->yy
if runArgs.doHiggsyy:
    genSeq.Pythia8.Commands += ["25:onMode = off",
                                "25:onIfMatch = 22 22"]

evgenConfig.description = "MadGraph+Pythia8 production JO with NNPDF30LN and A15NNPDF23LO for VLQ single " + runArgs.vlqmode + " to " + runArgs.vlqprocess[2:] + " while produced via " + runArgs.prodmode
evgenConfig.keywords = ["BSM", "BSMtop", "exotic"]
evgenConfig.process = runArgs.vlqprocess
evgenConfig.contact =  ['avik.roy@cern.ch, fschenck@cern.ch']
