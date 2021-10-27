#!/bin/bash

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh

MYRELEASE="AthGeneration,21.6.57,here"

rm -rf workdir
mkdir workdir
cp -r 100xxx/* workdir/
cp -r 101xxx/* workdir/
cp -r 102xxx/* workdir/
cp -r 103xxx/* workdir/
cp -r 104xxx/* workdir/
cp -r 105xxx/* workdir/
cp -r 106xxx/* workdir/
cp -r 107xxx/* workdir/
cp -r 108xxx/* workdir/
cd workdir
asetup ${MYRELEASE}
cd -
