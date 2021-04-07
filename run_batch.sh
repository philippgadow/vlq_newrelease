#!bin/bash

# Job submission for DESY HTCondor - copy to project directory and adapt to your needs
JOBNAME="EVGEN_vlq_VBHb_v3"
#List of DSIDs in job option directory
DSIDS="102000 102001 102002 102003 102004 102005 102006 102007 102008 102009 102010 102011 \
       102100 102101 102102 102103 102104 102105 102106 102107 102108 102109 102110 102111 \
       102200 102201 102202 102203 102204 102205 102206 102207 102208 102209 102210 102211 102212 102213 102214 102215"
EVENTS=10000               #Events per job
NJOBS=5                    #Number of jobs per DSID
RUNTIME="03:00:00"         #Run time per job HH:MM:SS
MEMORY=2000                #Memory per job in MB

cd batch_submission
COMMAND="python SubmitMC/python/submit.py --jobName ${JOBNAME} --engine HTCONDOR --eventsPerJob ${EVENTS} --nJobs ${NJOBS} -r ${DSIDS} --noBuildJob --accountinggroup af-atlas --evgen_runtime ${RUNTIME} --evgen_memory ${MEMORY}"
echo $COMMAND
$COMMAND
