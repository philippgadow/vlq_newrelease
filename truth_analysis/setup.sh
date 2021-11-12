#!/bin/bash

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh

RELEASE="AnalysisBase,21.2.190"

mkdir -p build run
cd build/
asetup $RELEASE
lsetup cmake
cmake ../source
make -j 5
source x*/setup.sh
cd ..
