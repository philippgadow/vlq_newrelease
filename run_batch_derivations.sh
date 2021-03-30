#!bin/bash

# Job submission for DESY HTCondor - copy to project directory and adapt to your needs
JOBNAME="TRUTH1_vlq_VBHb"
DSIDS="101108 101110 101111 101112 101113 101114 101115 101116 101117 101118 101119 101120 101121" #DSIDs in job option directory
RUNTIME="03:00:00"         #Run time per job HH:MM:SS
MEMORY=2000                #Memory per job in MB

cd batch_submission
COMMAND="python SubmitMC/python/submit_derivation.py --jobName ${JOBNAME} --engine HTCONDOR -r ${DSIDS} --noBuildJob --accountinggroup af-atlas --deriv_runtime ${RUNTIME} --deriv_memory ${MEMORY}"
echo $COMMAND
$COMMAND
