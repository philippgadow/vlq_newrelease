#!/bin/bash

DSID=${1}

if [[ -z ${DSID} ]]; then
    echo "DSID not provided, using 107000 as default.";
    DSID=107000;
fi

cd workdir
Gen_tf.py --ecmEnergy=13000. --firstEvent=1 --maxEvents=100 --randomSeed=1234 --jobConfig=${DSID} --outputEVNTFile=test_DSID_${DSID}.EVNT.root
cd -
ls workdir
