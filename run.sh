#!/bin/bash

DSID=${1}

if [[ -z ${DSID} ]]; then
    echo "DSID not provided, using 100001 as default.";
    DSID=100001;
fi

cd workdir
Gen_tf.py --ecmEnergy=13000. --firstEvent=1 --maxEvents=1 --randomSeed=1234 --jobConfig=${DSID} --runNumber=${DSID} --outputEVNTFile=test_DSID_${DSID}.EVNT.root
cd -
ls workdir
