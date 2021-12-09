#!/bin/bash
INPUT=VLBHb_Hyy
LOGS=logs_VLBHb_Hyy
OUTPUT=jo_request_VLBHb_Hyy
DSID_START=108

rm -rf ${OUTPUT}

mkdir -p ${OUTPUT}
cd $OUTPUT
mkdir -p 200xxx
cd 200xxx

# copy job options
for i in `ls ../../${INPUT}/`; do
    cp -r ../../${INPUT}/$i ${i/${DSID_START}/200}
    cp ../../${LOGS}/mc16_13TeV.${i}.EVNT.*.log ${i/${DSID_START}/200}/log.generate

    cd ${i/${DSID_START}/200}
    ln -sfn ../200000/MGPy8EG_A14NNPDF23LO_SingleVLQ_v2.py MGPy8EG_A14NNPDF23LO_SingleVLQ_v2.py
    ln -sfn ../200000/lhe_hacker_v2.py lhe_hacker_v2.py
    ln -sfn ../200000/VLQCouplingCalculator_v2.py VLQCouplingCalculator_v2.py
    JONAME=`ls mc*`
    unlink $JONAME
    echo "include(\"MGPy8EG_A14NNPDF23LO_SingleVLQ_v2.py\")" > $JONAME
    cd ../
done
ls 
cd ../
tar -cpvzf ../${OUTPUT}.tar.gz .
cd ..
