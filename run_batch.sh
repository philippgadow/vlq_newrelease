#!bin/bash

# Job submission for DESY HTCondor - copy to project directory and adapt to your needs
JOBNAME="EVGEN_vlq_VBHb"
#List of DSIDs in job option directory
DSIDS="107000 107001 107002 107003 107004 107005 107006 107007 107008 107009 \
       107010 107011 107012 107013 107014 107015 107016 107017 107018 107019 \
       107020 107021 107022 107023 107024 107025 107026 107027 107028 107029 \
       107030 107031 \
       108000 108001 108002 108003 108004 108005 108006 108007 108008 108009 \
       108010 108011 108012 108013 108014 108015 108016 108017 108018 108019 \
       108020 108021 108022 108023 108024 108025 108026 108027 108028 108029 \
       108030 108031"

EVENTS=10000               #Events per job
NJOBS=1                    #Number of jobs per DSID
RUNTIME="03:00:00"         #Run time per job HH:MM:SS
MEMORY=2000                #Memory per job in MB

cd batch_submission
COMMAND="python SubmitMC/python/submit.py --jobName ${JOBNAME} --engine HTCONDOR --eventsPerJob ${EVENTS} --nJobs ${NJOBS} -r ${DSIDS} --noBuildJob --accountinggroup af-atlas --evgen_runtime ${RUNTIME} --evgen_memory ${MEMORY}"
echo $COMMAND
$COMMAND
