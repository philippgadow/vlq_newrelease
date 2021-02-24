export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh

rm -rf workdir
mkdir workdir
cp -r 100xxx/100001/ workdir/
cd workdir
asetup AthGeneration, 21.6.57,here
cd -
