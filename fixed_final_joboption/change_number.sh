#!/bin/bash

# # helper script to change the number
# for i in 106*/; do
#     mv $i ${i/106/108}
# done

# helper script to change the JO name
for i in 108001 108002 108003 108004 108005 108006 108007 108008 108009 10801* 10802* 10803*; do
    cd $i
    ln -sfn ../108000/MGPy8EG_A14NNPDF23LO_SingleVLQ_v2.py MGPy8EG_A14NNPDF23LO_SingleVLQ_v2.py
    ln -sfn ../108000/lhe_hacker_v2.py lhe_hacker_v2.py
    ln -sfn ../108000/VLQCouplingCalculator_v2.py VLQCouplingCalculator_v2.py
    
    for f in `ls mc.*sig.py`; do
        rm $f
        ln -sfn MGPy8EG_A14NNPDF23LO_SingleVLQ_v2.py ${f/"sig"/"st"}
    done
    cd ../
done
