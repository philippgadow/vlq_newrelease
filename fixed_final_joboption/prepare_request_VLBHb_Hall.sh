#!/bin/bash
INPUT=VLBHb_Hall
LOGS=logs_VLBHb_Hall
OUTPUT=jo_request_VLBHb_Hall
DSID_START=107

rm -rf ${OUTPUT}

mkdir -p ${OUTPUT}
cd $OUTPUT
mkdir -p 100xxx
cd 100xxx

# copy job options
for i in `ls ../../${INPUT}/`; do
    cp -r ../../${INPUT}/$i ${i/${DSID_START}/100}
    cp ../../${LOGS}/mc16_13TeV.${i}.EVNT.*.log ${i/${DSID_START}/100}/log.generate

    cd ${i/${DSID_START}/100}
    ln -sfn ../100000/MGPy8EG_A14NNPDF23LO_SingleVLQ_v2.py MGPy8EG_A14NNPDF23LO_SingleVLQ_v2.py
    ln -sfn ../100000/lhe_hacker_v2.py lhe_hacker_v2.py
    ln -sfn ../100000/VLQCouplingCalculator_v2.py VLQCouplingCalculator_v2.py
    cd ../
done
ls 
cd ../
tar -cpvzf ../${OUTPUT}.tar.gz .
cd ..
