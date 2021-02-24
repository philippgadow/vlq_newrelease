# must use this for 21.6.50 or earlier
if [[ -f "/singularity" ]]; then
	rm -rf workdir
	mkdir workdir
	cp -r 100xxx/100001/ workdir/
	cd workdir
	# asetup AthGeneration, 21.6.12,here
	# asetup AthGeneration, 21.6.21,here
	asetup AthGeneration, 21.6.22,here
	cd -
else
	export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
	source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh -c sl6
fi

