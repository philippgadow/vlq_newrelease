# Truth analysis of VLQ sample production

This directory contains code to make plots of VLQ samples using MadGraph matrix element reweighting.

## How to use this

Before you can use the code within this `truth_analysis` directory, you need to generate VLQ signal samples using MadGraph reweigthing in the ATLAS MC workflow.

The expected input files for the truth analysis is a number of TRUTH1 derivation files.

The workflow is to process the TRUTH1 derivation files with an EventLoop based AnalysisAlgorithm to create small files with ROOT trees. These files can be analysed interactively in a second step using Jupyter notebooks.

## Installation

We assume that you already obtained the analysis code from GitHub on a machine with access to `/cvmfs` and the ATLAS software. You can set up an analysis release and install the truth analysis software by opening a clean shell and entering:

```bash
cd truth_analysis
source setup.sh
```

This will set up an ATLAS AnalysisBase release, create a `build` folder, compile the program and set the according environment variables.

Every time you log into a new shell you should again `source setup.sh`.

## Adapting the code

The algorithm for creating small ntuples is provided in `source/TruthAnalysis/Root/TruthAnalysis.cxx`.
Currently, the code is adapted for running over samples with a VLB resonance. You might need to adapt the code for your VLQ signal accordingly. The algorithm takes `TruthParticles` as input and computes from parton level entries in the truth record the invariant mass of the VLB candidate. The result is stored by decorating the `EventInfo` and writing out this information to a small tree.

The algorithm is steered and executed using the python job option `source/TruthAnalysis/share/truthanalysis_eljob.py`. Please examine the file and modify it accordingly. In the following, the structure of it is described:

Using the SampleHandler tool, the input folder is scanned for all files which contain a certain DSID and follow a certain structure. As an example, the folder which was used for the VLB truth analysis and which contained the TRUTH1 files had the structure

```
/nfs/dust/atlas/user/pgadow/MC/TRUTH/100000/DAOD_TRUTH1.mc16_13TeV.100000.478898.root
```

where the DSID for the sample was `100000` and the ROOT file followed the pattern `DAOD_TRUTH1.mc16_13TeV.100000.478898.root`. You might need to adapt the corresponding parts of the script.

After all input files have been scheduled, a CP algorithm which outputs all event weights used in the MadGraph reweighting is scheduled. You can inspect the corresponding files in the analysis release here:

- [PMGTruthWeightAlg header](https://gitlab.cern.ch/atlas/athena/-/blob/21.2/PhysicsAnalysis/Algorithms/AsgAnalysisAlgorithms/AsgAnalysisAlgorithms/PMGTruthWeightAlg.h)
- [PMGTruthWeightAlg source ](https://gitlab.cern.ch/atlas/athena/-/blob/21.2/PhysicsAnalysis/Algorithms/AsgAnalysisAlgorithms/Root/PMGTruthWeightAlg.cxx)

Then, the `TruthAnalysis` algorithm is scheduled to compute the VLQ mass and add it to the output by decorating the EventInfo with it.

Finally, the output is defined, which includes the VLQ mass (computed in two different ways) and (using a wildcard) all MadGraph reweighting event weights.

Remember to compile the code again after having modified it.

## Running over TRUTH1 files

To process all TRUTH1 files in an input directory, follow these instructions.
It is assumed, that the input TRUTH1 files for DSID `100000` (as an example) are stored in `/nfs/dust/atlas/user/pgadow/MC/TRUTH/100000/` and that the corresponding ROOT files follow the pattern of the file `DAOD_TRUTH1.mc16_13TeV.100000.478898.root`, which is `DAOD_TRUTH1.mc16_13TeV.<DSID>.<random seed>.root`.

Rembember that you first need to install and setup the code. Then you can execute to process all DSIDs which start with `100` (similar meaning to the wildcard `100*`):

```bash
cd run
truthanalysis_eljob.py -i /nfs/dust/atlas/user/pgadow/MC/TRUTH/ --dsid_pattern 100
```

## Analysis of output root trees

The analysis of the small trees can occur locally on a laptop or private machine using jupyter notebooks in python.
The two examples in this directory should be self-explanatory.