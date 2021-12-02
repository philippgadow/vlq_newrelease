#!/bin/bash

# H(all) decay
cd VLBHb_Hall
tar -cpvzf ../JobOptions_VLBHb_Hall.tar.gz .
cd ..

cd logs_VLBHb_Hall
tar -cpvzf ../logs_VLBHb_Hall.tar.gz .
cd ..

# H(yy) decay
cd VLBHb_Hyy
tar -cpvzf ../JobOptions_VLBHb_Hyy.tar.gz .
cd ..

cd logs_VLBHb_Hyy
tar -cpvzf ../logs_VLBHb_Hyy.tar.gz .
cd ..
