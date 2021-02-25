# must use this for 21.6.50 or earlier
 if [[ -f "/singularity" ]]; then
	MYRELEASE="AthGeneration,21.6.48,here"

	rm -rf workdir
	mkdir workdir
	cp -r 100xxx/* workdir/
	cd workdir
	asetup ${MYRELEASE}
	cd -
 else
     echo "Setting up singularity container, please run >source setup_sl6.sh< a second time."
     export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
     source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh -c sl6
 fi

