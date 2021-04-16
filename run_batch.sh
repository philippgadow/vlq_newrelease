#!bin/bash

# Job submission for DESY HTCondor - copy to project directory and adapt to your needs
JOBNAME="EVGEN_vlq_VBHb_JOTEST"
#List of DSIDs in job option directory
DSIDS="103000 103001 103002 103003 103004 103005 103006 103007 103008 103009 \
       103010 103011 103012 103013 103014 103015 103016 103017 103018 103019 \
       103020 103021 103022 103023 103024 103025 103026 103027 103028 103029 \
       103030 103031 103032 103033 103034 103035 \
       104000 104001 104002 104003 104004 104005 104006 104007 104008 104009 \
       104010 104011 104012 104013 104014 104015 104016 104017 104018 104019 \
       104020 104021 104022 104023 104024 104025 104026 104027 104028 104029 \
       104030 104031 104032 104033 104034 104035"

EVENTS=10000               #Events per job
NJOBS=1                    #Number of jobs per DSID
RUNTIME="03:00:00"         #Run time per job HH:MM:SS
MEMORY=2000                #Memory per job in MB

cd batch_submission
COMMAND="python SubmitMC/python/submit.py --jobName ${JOBNAME} --engine HTCONDOR --eventsPerJob ${EVENTS} --nJobs ${NJOBS} -r ${DSIDS} --noBuildJob --accountinggroup af-atlas --evgen_runtime ${RUNTIME} --evgen_memory ${MEMORY}"
echo $COMMAND
$COMMAND
