#! /usr/bin/env python

from __future__ import print_function

import optparse, sys, math, subprocess, os, shutil
from collections import OrderedDict
from csv import writer


parser = optparse.OptionParser(usage=__doc__)
parser.add_option("-i", "--input", default="-", dest="INPUT_FILE", metavar="PATH",   help="input logfile")
parser.add_option("-N", "--Ntotal", default=0, dest="TOTAL_EVENTS", metavar="", help="Total number of events")
parser.add_option("-m", "--mcver", dest="MC_VER", default="MC15", help="Specify MCXX campaign")
parser.add_option("-s", "--nogit", action="store_true", dest="NO_GIT", default=False, help="Turn off any checks that require git")
parser.add_option("-c", "--nocolour", action="store_true", dest="NO_COLOUR", default=False, help="Turn off colour for copying to file")
parser.add_option("-x", "--csv", action="store", dest="OUTPUT_CSV", default="test.csv", help="Output csv file")

opts, fileargs = parser.parse_args()

MCJobOptions='%sJobOptions'%opts.MC_VER
MCXX='%s.'%opts.MC_VER

def sherpaChecks(logFile):    
    file=open(logFile,"r")
    lines=file.readlines()    
    # check each line
    inside = 0
    numexceeds =0
    for line in lines:
        if "exceeds maximum by" in line:
            numexceeds +=1
            loginfo("- "+line.strip(),"")
        if "Retried events" in line:
            inside = 1
            continue
        if inside:
            if "}" in line:
                break
            if len(line.split('"')) == 1:
                break
            if len(line.split('->'))== 1:
                break
            name = line.split('"')[1]
            percent = line.split('->')[1].split("%")[0].strip()
            if float(percent) > 5.:
                logwarn("- retried events "+name+" = ",percent+" % <-- WARNING: more than 5% of the events retried")
            else:
                loginfo("- retried events "+name+" = ",percent+" %")    
    if opts.TOTAL_EVENTS:
        if numexceeds*33>int(opts.TOTAL_EVENTS):
            logwarn("","WARNING: be aware of: "+str(numexceeds*100./int(opts.TOTAL_EVENTS))+"% of the event weights exceed the maximum by a factor of ten")

def pythia8Checks(logFile,generatorName):
    file=open(logFile,"r")
    lines=file.readlines()
    usesShowerWeights = False
    usesMatchingOrMerging = False
    usesCorrectPowheg = False
    errors = False
    for line in lines:
        if "Pythia8_ShowerWeights.py" in line:
            usesShowerWeights = True
        if "Pythia8_aMcAtNlo.py" in line or "Pythia8_CKKWL_kTMerge.py" in line or "Pythia8_FxFx.py" in line:
            usesMatchingOrMerging = True
        if "Pythia8_Powheg_Main31.py" in line:
            usesCorrectPowheg = True
    if usesShowerWeights and usesMatchingOrMerging:
        logerr("ERROR:","Pythia 8 shower weights buggy when using a matched/merged calculation. Please remove the Pythia8_ShowerWeights.py include.")
        errors = True
    if "Powheg" in generatorName and not usesCorrectPowheg:
        logerr("ERROR:",generatorName+" used with incorrect include file. Please use Pythia8_Powheg_Main31.py")
        errors = True
    if not errors:
        loggood("INFO: Pythia 8 checks:","Passed")		

def herwig7Checks(logFile,generatorName,metaDataDict):
    errors = False
    allowed_tunes=['H7.1-Default', 'H7.1-SoftTune', 'H7.1-BaryonicReconnection']
    if "7.1" in generatorName:
        if metaDataDict['generatorTune'][0] not in allowed_tunes:
            logerr("ERROR:", "Metadata tune set to {0}, which is not in the list of allowed tunes: {1}".format(metaDataDict['generatorTune'][0], allowed_tunes))
            errors = True
        file=open(logFile,"r")
        lines=file.readlines()
        for line in lines:
           if "Herwig7_EvtGen.py" in line:
               logerr("ERROR:","Herwig 7.1 used with wrong include: Herwig7_EvtGen.py. Please use Herwig71_EvtGen.py instead.")
               errors = True	
               break       
    if not errors:
        loggood("INFO: Herwig 7 checks:","Passed")

def generatorChecks(logFile, generatorName,metaDataDict):
    print ("")
    print ("-------------------------")
    print ("Generator specific tests: ", generatorName)
    print ("-------------------------")
    if "Sherpa" in generatorName:
        sherpaChecks(logFile)
    if "Pythia8" in generatorName:
        pythia8Checks(logFile,generatorName)
    if "Herwig7" in generatorName:
       herwig7Checks(logFile,generatorName,metaDataDict)

def getMCJOrepository():
    if os.path.exists("mc15joboptions"):
        shutil.rmtree("mc15joboptions")
    gitcomm="git clone --quiet ssh://git@gitlab.cern.ch:7999/atlas-physics/pmg/infrastructure/mc15joboptions.git"
    command = subprocess.Popen(gitcomm, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    command.communicate()
    retcode = command.returncode
    if retcode != 0:
        logerr("ERROR:","can't clone mc15joboptions repository")

def main():
    """logParser.py script for parsing log.generate files to check MC production settings and output
     - Written by Josh McFayden <mcfayden@cern.ch> Nov 2016 """


    if opts.INPUT_FILE=="-":
        parser.print_help()
        return 
    
        
    # define dictionaries with keys as variables to be searched for and values to store the results
    
    JOsDict={
        'using release':[],
        "including file \""+MCJobOptions+"/":[],
        "including file \""+MCXX:[]
        }
    
    testHepMCDict={
        'Events passed':[],
        'Efficiency':[]
        }
    
    countHepMCDict={
        'Events passing all checks and written':[]
        }
    
    evgenFilterSeqDict={
        'Weighted Filter Efficiency':[],
        'Filter Efficiency':[]
        }
    
    simTimeEstimateDict={
        'RUN INFORMATION':[]
        }
    
    metaDataDict={ 
        'physicsComment =':[],
        'generatorName =':[],
        'generatorTune':[],
        'keywords =':[],
        'specialConfig =':[],
        'contactPhysicist =':[],
#        'randomSeed':[],
        'genFilterNames = ':[],
        'cross-section (nb)':[],
        'generator =':[],
        'weights =':[],
        'PDF =':[],
        'GenFiltEff =':[],
        'sumOfNegWeights =':[],
        'sumOfPosWeights =':[]
        }
    
    generateDict={
        'minevents':[0]
        }
    
    perfMonDict={
        'snapshot_post_fin':[],
        'jobcfg_walltime':[],
        'last -evt vmem':[]
        }
    
    # open and read log file
    file=open(opts.INPUT_FILE,"r")
    lines=file.readlines()
    
    # check each line
    for line in lines:
    
        checkLine(line,'Py:Athena',JOsDict,'INFO')
    
        checkLine(line,'MetaData',metaDataDict,'=')
        checkLine(line,'Py:Generate',generateDict,'=')
    
        checkLine(line,'Py:PerfMonSvc',perfMonDict,':')
        checkLine(line,'PMonSD',perfMonDict,'---')
    
        checkLine(line,'TestHepMC',testHepMCDict,'=')
        checkLine(line,'Py:EvgenFilterSeq',evgenFilterSeqDict,'=')
        checkLine(line,'CountHepMC',countHepMCDict,'=')
        checkLine(line,'SimTimeEstimate',simTimeEstimateDict,'|')
            
    
            
    # # print results
    # JOsErrors=[]
    # print ("")
    # print ("---------------------")
    # print ("jobOptions and release:")
    # print ("---------------------")

    # #Checking jobOptions
    # JOsList=getJOsList(JOsDict)
    # if not len(JOsList):
    #     JOsErrors.append("including file \""+MCJobOptions+"/")
    #     JOsErrors.append("including file \""+MCXX)
    # else:
          
    #     if not len(JOsDict["including file \""+MCJobOptions+"/"]):
    #         JOsErrors.append("including file \""+MCJobOptions+"/")
    #     if not len(JOsDict["including file \""+MCXX]):
    #         JOsErrors.append("including file \""+MCXX)
    
    #     DSIDxxx=''
    #     topJO=''
    #     nTopJO=0
    #     loginfo( '- jobOptions =',"")
    #     for jo in JOsList:
    #         pieces=jo.replace('.py','').split('.')
    #         if len(pieces) and pieces[0]==MCXX.replace('.',''):
    #             ##This is top JO
    #             nTopJO=nTopJO+1
    #             topJO=jo
    #             DSID=pieces[1]
    #             DSIDxxx="DSID"+DSID[:3]+"xxx"
    
    #     if nTopJO!=1:
    #         logerr( "","ERROR: !=1 (%i) \"top\" JO files found!"%nTopJO)
    #         raise RuntimeError("!= 1 \"top\" JO file found")
    #     else:
    #         #Check if JOs are on git!
    #         if not opts.NO_GIT:
    #             # Download git repository
    #             getMCJOrepository()
                
    #             # Check if jO exist in the repository
    #             for jo in JOsList:
    #                 if jo == topJO:
    #                     if os.path.isfile("mc15joboptions/share/%s/%s"%(DSIDxxx,jo)):
    #                         loggood("",jo)
    #                     else:
    #                         logerr("",jo+" ERROR <-- jobOptions not found on git!")
    #                 else:
    #                     indices = subprocess.Popen("find mc15joboptions -type f -name {0}".format(jo), shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.readlines()
    #                     if len(indices)==1:
    #                         loggood("",jo)
    #                     else:
    #                         if not len(indices):
    #                             logerr("",jo+" - jobOptions not found on git!")
    #                         else:
    #                             logwarn("",jo+" - multiple instances of jobOptions not found on git!")
    #                             for ix in indices:
    #                                 logwarn("",jo+" --> %s"%ix)
    #         else:
    #             for jo in JOsList:
    #                 loginfo("",jo)
    
    
    # #Checking release
    # release="not found"
    # if not len(JOsDict['using release']):
    #     JOsErrors.append(JOsDict['using release'])
    # else:
    #     name='using release'
    #     tmp=JOsDict[name][0].replace('using release','').strip().split()[0]
    #     val=tmp.replace('[','').replace(']','')
    #     release=val.split('-')[1]
    #     #checkForBlacklist
    #     if not opts.NO_GIT and opts.MC_VER!="MC12":
    #         blacklisted=checkBlackList(val.split('-')[0],val.split('-')[1],MCJobOptions,".",JOsList) 
    #         if blacklisted:
    #             logerr( '- '+name+' = ',"".join(val)+" <-- ERROR: %s"%blacklisted)
    #         else:
    #             loggood( '- '+name+' = ',"".join(val))
    #     else:
    #         loginfo( '- '+name+' = ',"".join(val))
    
    
    
    # if len(JOsErrors):
    #     print ("---------------------")
    #     print ("MISSING JOs:")
    #     for i in JOsErrors:
    #         if i == "including file \""+MCXX:
    #             #do nothing
    #             logwarn("","INFO: local version of JOs used?")
    #         else:
    #             logwarn("","ERROR: %s is missing!"%i)
    
    
    # ###
    # generateErrors=[]
    # print ("")
    # print ("---------------------")
    # print ("Generate params:")
    # print ("---------------------")
    # for key in generateDict:
    #     name=key
    #     val=generateDict[key]
    
    #     if not len(val):
    #         generate.append(name)
    #     else:
    #         if key == 'minevents':
    #             tmp=str(val[2]).split('#')[0].strip()
    #             generateDict['minevents']=tmp
    #             val=tmp
    
    #         loginfo( '- '+name+' = ',"".join(val))
    
    # if len(generateErrors):
    #     print ("---------------------")        
    #     print ("MISSING Generate params:")
    #     for i in generateErrors:
    #         logerr("","ERROR: %s is missing!"%i)
            
    
    ###
    metaDataErrors=[]
    print ("")
    print ("---------------------")
    print ("Metadata:")
    print ("---------------------")
    for key in metaDataDict:
        name=key.replace("=","").strip()
        val=metaDataDict[key]
        if not len(val):
            metaDataErrors.append(name)
        else:
            if name=="contactPhysicist":
                if '@' in "".join(val):
                    loggood( '- '+name+' = ',"".join(val))
                else:
                    logerr( '- '+name+' = ',"".join(val)+"  <-- ERROR: No email found")
                continue
            elif name=="cross-section (nb)":
                if float(val[0]) < 0:
                    logerr( '- '+name+' = ',"".join(val)+"  <-- ERROR: Cross-section is negative")
                    continue
            elif name=="GenFiltEff":
                if float(val[0]) < 1E-5:
                    logerr( '- '+name+' = ',"".join(val)+"  <-- ERROR: Filter efficiency too low")
                    continue
                elif float(val[0]) < 5E-2:
                    logwarn( '- '+name+' = ',"".join(val)+"  <-- WARNING: Low filter efficiency")
                    continue
            elif name=="keywords" and not opts.NO_GIT:
                tmpkeyword = "mc15joboptions/common/evgenkeywords.txt"
                if not os.path.isfile(tmpkeyword):
                    logerr("ERROR:", "can't find mc15joboptions/common/evgenkeywords.txt")
                    continue

                kfile = open(tmpkeyword)
                klines = kfile.readlines()
                foundkeywordlist=""
                for keyword in (",".join(val)).split(','):
                    keywordfound=False
                    for line in klines:
                        if line.strip().lower()==keyword.strip().lower():
                            keywordfound=True
                            break
                    if not keywordfound:
                        logwarn( '- '+name+' = ',keyword.strip()+"  <-- WARNING: keyword not found in "+MCJobOptions+"/common/evgenkeywords.txt")
                    else:
                        if len(foundkeywordlist): foundkeywordlist+=","+keyword
                        else: foundkeywordlist=keyword
                if len(foundkeywordlist): loggood( '- '+name+' = ',foundkeywordlist)
                        
                continue
                

            loginfo( '- '+name+' = ',"".join(val))
    
    if len(metaDataDict["sumOfPosWeights ="]) and len(metaDataDict["sumOfNegWeights ="]):
        ratio = float(metaDataDict["sumOfNegWeights ="][0])*1.0/(float(metaDataDict["sumOfPosWeights ="][0]) + float(metaDataDict["sumOfNegWeights ="][0]))
        if ratio>0.15:
            logwarn( '- sumOfNegWeights/(sumOfPosWeights+sumOfNegWeights) = ',str(ratio)+"  <-- WARNING: more than 15% of the weights are negative")


    if len(metaDataErrors):
        print ("---------------------")
        print ("MISSING Metadata:")
        for i in metaDataErrors:
            if i=="weights" or i=="genFilterNames" or i=="generator" or i=="PDF" or i=="sumOfNegWeights" or i=="sumOfPosWeights":
                loginfo("INFO:","%s is missing"%i)
            else:
                logerr("","ERROR: %s is missing!"%i)
            

    # Generator specific tests
    # First find generator first
    generatorName=metaDataDict['generatorName ='][0]
    generatorChecks(opts.INPUT_FILE, generatorName,metaDataDict)
    
    ####
    cpuPerJob=0.0
    perfMonErrors=[]
    print ("")
    print ("---------------------")
    print ("Performance metrics:")
    print ("---------------------")
    for key in perfMonDict:
        name=key
        val=perfMonDict[key]
        if not len(val):
            perfMonErrors.append(name)
        else:
    
            if key == 'snapshot_post_fin':
                name = 'CPU'
                tmp = 0.
                tmp=float(val[0].split()[3])
                if len(perfMonDict['jobcfg_walltime']):
                    tmp+=float(perfMonDict['jobcfg_walltime'][0].split()[1].split('=')[1])
                tmp=tmp/(1000.*60.*60.)
                cpuPerJob=tmp
                
                val = "%.2f hrs"%tmp
                if tmp > 18.: 
                    logerr( '- '+name+' = ',"".join(val))
                else:
                    loggood( '- '+name+' = ',"".join(val))
    
            if key == 'last -evt vmem':
                name = 'Virtual memory'
                tmp=float(val[0].split()[0])
                if tmp > 2048.: 
                    logerr( '- '+name+' = ',"".join(val))
                else:
                    loggood( '- '+name+' = ',"".join(val))
    
    
    if len(perfMonErrors):
        print ("---------------------")     
        print ("MISSING Performance metric:")
        for i in perfMonErrors:
            print ("ERROR: %s is missing!"%i)
            
    
    
    ####     
    testDict = {
        'TestHepMC':testHepMCDict,
        'EvgenFilterSeq':evgenFilterSeqDict,
        'CountHepMC':countHepMCDict,
        'SimTimeEstimate':simTimeEstimateDict
        }
    
    testErrors=[]
    filt_eff=1.0
    # print ("")
    # print ("---------------------")
    # print ("Event tests:")
    # print ("---------------------")
    # for dictkey in testDict:
    #     for key in testDict[dictkey]:
    #         name=key
    #         val=testDict[dictkey][key]
    #         if not len(val):
    #             testErrors.append("%s %s"%(dictkey,name))
    #         else:
    #             #Check final Nevents processed
    #             if dictkey=="CountHepMC":
    #                 allowed_minevents_lt1000 = [1, 2, 5, 10, 20, 25, 50, 100, 200, 500]
    #                 if int(val[0])%1000!=0 and not int(val[0]) in allowed_minevents_lt1000:
    #                     logerr( '- '+dictkey+" "+name+' = ',"".join(val)+"  <-- ERROR: Not an acceptable number of events for production")
    #                 elif int(val[0]) != int(generateDict['minevents']):
    #                     logerr( '- '+dictkey+" "+name+' = ',"".join(val)+"  <-- ERROR: This is not equal to minevents")
    #                 else:
    #                     loggood( '- '+dictkey+" "+name+' = ',"".join(val))
    #                 continue
		
    #             #Check filter efficiencies aren not too low
    #             if dictkey=="EvgenFilterSeq":
    #                 if name=="Weighted Filter Efficiency":
    #                     filt_eff=float(val[0].split()[0])
    #                 if float(val[0].split()[0])<0.01:
    #                     logerr( '- '+dictkey+" "+name+' = ',"".join(val))
    #                 else:
    #                     loggood( '- '+dictkey+" "+name+' = ',"".join(val))
    #                 continue
    
    #             if dictkey=="TestHepMC" and name=="Efficiency":
    #                 if float(val[0].replace('%',''))<100. and float(val[0].replace('%',''))>=98.:
    #                     logwarn( '- '+dictkey+" "+name+' = ',"".join(val))
    #                 elif float(val[0].replace('%',''))<100.:
    #                     logerr( '- '+dictkey+" "+name+' = ',"".join(val))
    #                 else:
    #                     loggood( '- '+dictkey+" "+name+' = ',"".join(val))
    #                 continue
    
    
    #             loginfo( '- '+dictkey+" "+name+' = ',"".join(val))
    
    # if len(testErrors):
    #     print ("---------------------")
    #     print ("Failed tests:")
    #     for i in testErrors:
    #         if i =="SimTimeEstimate RUN INFORMATION":
    #             logwarn("","WARNING: %s is missing!"%i)
    #         else:
    #             if "TestHepMC" in i and "Sherpa" in metaDataDict['generatorName ='][0]:
    #                 logwarn("","WARNING: %s is missing, but expected as it's Sherpa!"%i)
    #             else:
    #                 logerr("","ERROR: %s is missing!"%i)
    
    
    ## Add equivalent lumi information
    if opts.TOTAL_EVENTS:
        print ("")
        print ("")
        print ("---------------------") 
        print (" Others:")
        print ("---------------------")

    xs_nb=0.0
    eff_lumi_fb=0.0

    if opts.TOTAL_EVENTS:
        xs_nb=float(metaDataDict['cross-section (nb)'][0])
        eff_lumi_fb=float(opts.TOTAL_EVENTS)/(1.E+06*xs_nb*filt_eff)
        if eff_lumi_fb > 1000.:
            logwarn("- Effective lumi (fb-1):",str(eff_lumi_fb)+" <-- WARNING: very high effective luminosity")
        elif eff_lumi_fb < 40.:
            logwarn("- Effective lumi (fb-1):",str(eff_lumi_fb)+" <-- WARNING: low effective luminosity")
        else:
            loggood("- Effective lumi (fb-1):",str(eff_lumi_fb))
        # minevents=int(generateDict['minevents'])
        # #int(countHepMCDict['Events passing all checks and written'][0])
        # loginfo("- Number of jobs:",int(opts.TOTAL_EVENTS)/minevents)
        # if int(opts.TOTAL_EVENTS) <= 5000:
        #     logwarn("- Total no. of events:",opts.TOTAL_EVENTS+" <-- WARNING: This total is low enough that the mu profile may be problematic - INFORM MC PROD")
    
    # if not opts.TOTAL_EVENTS or opts.NO_GIT:
    #     print ("")
    #     print ("")
    #     print ("---------------------")
    #     print ("Incomplete tests:")
    #     if not opts.TOTAL_EVENTS:
    #         logerr("","ERROR: --Ntotal (-N) flag is not used - total number of events not given - impossible to calculated effective lumi.")
    #     if opts.NO_GIT:
    #         logerr("","ERROR: --nogit (-x) flag is used - could not check that git JOs are registered or whether release is blacklisted.")


    # Print total number of Errors/Warnings
    print ("")
    print ("")
    print ("---------------------")
    print (" Summary:")
    print ("---------------------")
    if (LogCounts.Errors == 0):
        if (LogCounts.Warnings == 0):
            loggood("Errors : "+str(LogCounts.Errors)+" , Warnings : "+str(LogCounts.Warnings)," -> OK for production")
        else:
            loggood("Errors : "+str(LogCounts.Errors)+" , Warnings : "+str(LogCounts.Warnings)," -> Some warnings encountered, check that these are ok before submitting production!")
    else:
        logerr("Errors : "+str(LogCounts.Errors)+" , Warnings : "+str(LogCounts.Warnings)," -> Errors encountered! Not ready for production!")  
    print ("")


    # hacky fix
    topJO = "JO"
    release = "21.6.57"

    #Write csv file output
    cols=['Brief desciption','JobOptions','CoM energy [GeV]','Events (Evgen-only)','Events (FullSim)','Events (Atlfast II)','Priority','Output formats','Cross section [pb]','Effective luminosity [fb-1]','Filter efficiency','Evgen CPU time/job [hr]','Input files','MC-tag','Release','Comments','Evgen tag','Simul tag','Merge tag','Digi tag','Reco tag','Rec Merge tag','Atlfast tag','Atlf Merge tag']
    row=[]
    row=pad(row,24,"")
    row[cols.index('JobOptions')]=topJO
    #row[cols.index('CoM energy [GeV]')]=13000.
    #row[cols.index('Events (Evgen-only)')]=opts.TOTAL_EVENTS
    if opts.TOTAL_EVENTS:
        row[cols.index('Events (Evgen-only)')]=str(opts.TOTAL_EVENTS)+" (CHECK MANUALLY)"
    row[cols.index('Cross section [pb]')]=xs_nb*1000.
    if opts.TOTAL_EVENTS:
        row[cols.index('Effective luminosity [fb-1]')]=eff_lumi_fb
    row[cols.index('Filter efficiency')]=filt_eff
    row[cols.index('Evgen CPU time/job [hr]')]=cpuPerJob
    row[cols.index('Release')]=release
    #for n,c in enumerate(cols):
    #    print c,row[n]
    outCSV=open(opts.OUTPUT_CSV,'w')
    outCSVwriter=writer(outCSV)
    outCSVwriter.writerow(row)
    outCSV.close()
        
    return 
    


def getJOsList(JOsDict):
    liststr=''
    if len(JOsDict["including file \""+MCJobOptions+"/"]):
        liststr+="|".join(JOsDict["including file \""+MCJobOptions+"/"]).replace("nonStandard/","")
    if len(JOsDict["including file \""+MCXX]):
        if len(liststr): liststr+="|"
        liststr+="|".join(JOsDict["including file \""+MCXX]).replace("nonStandard/","")
    liststr=liststr.replace(MCJobOptions+'/','').replace('"','').replace('including file','').replace(' ','')
    tmplist=liststr.split('|')
    return tmplist


def checkBlackList(branch,cache,MCJobOptions,outnamedir,JOsList) :
    aJOs=[]
    for l in JOsList:
        if MCXX in l:
            aJOs.append(l)   
    ## Black List Caches MC15
    tmpblackfile = "mc15joboptions/common/BlackList_caches.txt"
    isError=None
    if not os.path.isfile(tmpblackfile):
        logerr("ERROR:","can't find BlackList_caches.txt" )
        isError = "can't find BlackList_caches.txt"
        return isError

    bfile = open(tmpblackfile)
    blines=bfile.readlines()
    for line in blines:
        if not line.strip():
            continue

        bad = "".join(line.split()).split(",")
        
        badgens=[bad[2]]
        if bad[2]=="Pythia8":
            badgens.append("Py8")
        if bad[2]=="Pythia":
            badgens.append("Py")
        if bad[2]=="MadGraph":
            badgens.append("MG")
        if bad[2]=="Powheg":
            badgens.append("Ph")
        if bad[2]=="Herwigpp":
            badgens.append("Hpp")
        if bad[2]=="Herwig7":
            badgens.append("H7")
        if bad[2]=="Sherpa":
            badgens.append("Sh")
        if bad[2]=="Alpgen":
            badgens.append("Ag")
        if bad[2]=="EvtGen":
            badgens.append("EG")
        if bad[2]=="ParticleGun":
            badgens.append("PG")
        
        #Match Generator and release type e.g. AtlasProduction, MCProd
        if any( badgen in s.split('_')[0] for s in aJOs for badgen in badgens ) and branch in bad[0]:
            #Match cache
            cacheMatch=True               
            for i,c in enumerate(cache.split('.')):
                if not c == bad[1].split('.')[i]:
                    cacheMatch=False
                    break

            if cacheMatch:            
                #logerr("", "Combination %s_%s for %s it is blacklisted"%(bad[0],bad[1],bad[2]))
                isError = "%s_%s is blacklisted for %s"%(bad[0],bad[1],bad[2])
                return isError

            
    return isError


# find identifiers and variables in log file lines
def checkLine(line, lineIdentifier, dict, splitby ):
    if lineIdentifier in line:
        for param in dict:
            if param=="including file \""+MCXX:
                if "including file" in line and MCXX in line:
                    if len(line.split(splitby))==0:
                        raise RuntimeError("Found bad entry %s"%line)
                    else:
                        thing="".join(line.split(lineIdentifier)[1].split(splitby)[1:]).split("/")[-1].strip()
                        dict[param].append(thing)
                    break
            else:
                if param in line:
                    if len(line.split(splitby))==0:
                        raise RuntimeError("Found bad entry %s"%line)
                    else:
                        thing="".join(line.split(lineIdentifier)[1].split(splitby)[1:]).strip()     
                        dict[param].append(thing)
                    break
		    
class bcolors:
    if not opts.NO_COLOUR:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
    else:
        HEADER = ''
        OKBLUE = ''
        OKGREEN = ''
        WARNING = ''
        FAIL = ''
        ENDC = ''

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

class LogCounts:
    Errors = 0
    Warnings = 0

def loginfo(out1,out2):
    print (str(out1),bcolors.OKBLUE + str(out2) + bcolors.ENDC)
def loggood(out1,out2):
    print (str(out1),bcolors.OKGREEN + str(out2) + bcolors.ENDC)
def logerr(out1,out2):
    print (str(out1),bcolors.FAIL + str(out2) + bcolors.ENDC)
    LogCounts.Errors += 1
def logwarn(out1,out2):
    print (str(out1),bcolors.WARNING + str(out2) + bcolors.ENDC)
    LogCounts.Warnings += 1

def pad(seq, target_length, padding=None):
    length = len(seq)
    if length > target_length:
        return seq
    seq.extend([padding] * (target_length - length))
    return seq

if __name__ == "__main__":
    main()

