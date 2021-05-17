#!bin/bash

# Job submission for DESY HTCondor - copy to project directory and adapt to your needs
JOBNAME="EVGEN_vlq_VBHb_JOTEST"
#List of DSIDs in job option directory
# DSIDS="105000 105001 105002 105003 105004 105005 105006 105007 105008 105009 \
#        105010 105011 105012 105013 105014 105015 105016 105017 105018 105019 \
#        105020 105021 105022 105023 105024 105025 105026 105027 105028 105029 \
#        105030 105031 \
#        106000 106001 106002 106003 106004 106005 106006 106007 106008 106009 \
#        106010 106011 106012 106013 106014 106015 106016 106017 106018 106019 \
#        106020 106021 106022 106023 106024 106025 106026 106027 106028 106029 \
#        106030 106031"
DSIDS="105000 105016 106000 106016"

EVENTS=10000               #Events per job
NJOBS=1                    #Number of jobs per DSID
RUNTIME="03:00:00"         #Run time per job HH:MM:SS
MEMORY=2000                #Memory per job in MB

cd batch_submission
COMMAND="python SubmitMC/python/submit.py --jobName ${JOBNAME} --engine HTCONDOR --eventsPerJob ${EVENTS} --nJobs ${NJOBS} -r ${DSIDS} --noBuildJob --accountinggroup af-atlas --evgen_runtime ${RUNTIME} --evgen_memory ${MEMORY}"
echo $COMMAND
$COMMAND
