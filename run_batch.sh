#!bin/bash

# Job submission for DESY HTCondor - copy to project directory and adapt to your needs
JOBNAME="EVGEN_vlq_VBHb"
#List of DSIDs in job option directory
DSIDS="101000 101001 101002 101003 101004 101005 101006 101007 101008 \
       101100 101101 101102 101103 101104 101105 101106 101107 101108 \
       101110 101111 101112 101113 101114 101115 101116 101117 101118 101119 101120 101121"
EVENTS=10000               #Events per job
NJOBS=1                    #Number of jobs per DSID
RUNTIME="03:00:00"         #Run time per job HH:MM:SS
MEMORY=2000                #Memory per job in MB

cd batch_submission
COMMAND="python SubmitMC/python/submit.py --jobName ${JOBNAME} --engine HTCONDOR --eventsPerJob ${EVENTS} --nJobs ${NJOBS} -r ${DSIDS} --noBuildJob --accountinggroup af-atlas --evgen_runtime ${RUNTIME} --evgen_memory ${MEMORY}"
echo $COMMAND
$COMMAND
