import sys,os
root_dir=os.path.normpath(os.path.dirname(os.path.abspath(__file__))).split('com' + os.sep + 'ericsson' + os.sep + 'xn' + os.sep + 'x' + os.sep + 'pm' + os.sep + 'NBIPmCases')[0]
sys.path.append(root_dir)
from com.ericsson.xn.commons import test_logger
from com.ericsson.xn.commons import caseutils
from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from datetime import datetime, timedelta, tzinfo
import time
from optparse import OptionParser

def check_options():
    parser=OptionParser(usage="usage: %prog --type --name --nodeid --licid --interval --starttime --endtime")
    parser.add_option("--type",action="store",type="string",dest="netype",help="Specify the netype")
    parser.add_option("--name",action="store",type="string",dest="nename",help="Specify the nename")
    parser.add_option("--nodeid",action="store",type="string",dest="nodeid",help="Specify the nodeid")
    parser.add_option("--licid",action="store",type="string",dest="licid",help="Specify the licid")
    parser.add_option("--interval",action="store",type="int",dest="interval",default=5,help="Specify the pm interval")
    parser.add_option("--starttime",action="store",type="string",dest="starttime",help="Specify the starttime of checking pm files.The format must be like 201612010000")
    parser.add_option("--endtime",action="store",type="string",dest="endtime",help="Specify the endtime of checking pm files. The format must be like 201612012359")
    parser.add_option("--path",action="store",type="string",dest="path",help="Specify the pm files storage path")
    
    (options,args) = parser.parse_args()
    if options.netype == None or options.nename == None or options.nodeid == None or options.licid == None or \
        options.starttime == None or options.endtime == None or options.path == None:
        parser.print_help()
        print options,-1
    
    return options,0
    

if __name__ == '__main__':  
    options,i=check_options()
    if i==0:
        starttime=datetime.strptime(options.starttime,"%Y%m%d%H%M")
        endtime=datetime.strptime(options.endtime,"%Y%m%d%H%M")
        starttime_utc=starttime+timedelta(hours=-8)
        endtime_utc=endtime+timedelta(hours=-8)
        totalseconds=(endtime_utc-datetime(1970,1,1)).total_seconds() - (starttime_utc-datetime(1970,1,1)).total_seconds()
        hours_to_check=int(totalseconds/3600)
        starttime = endtime + timedelta(hours=-hours_to_check) + timedelta(minutes=options.interval)
        print "start to check pm files for " + starttime.strftime("%Y%m%d%H%M") + " to " + endtime.strftime("%Y%m%d%H%M")
        caseutils.pre_test_case("check_spm_"+options.netype+"_cases", "nbi_spm_pm_check")
        circletime=endtime
        while circletime > starttime:    
            circletime = circletime.strftime("%Y%m%d%H%M")
            NBIPmFunc.PMCmpInstance(options.netype,options.nename,options.nodeid,options.licid,options.interval,circletime,options.path).check_pm_accuracy()
            timeshift =  datetime.strptime(circletime,"%Y%m%d%H%M").minute % options.interval
            circletime = datetime.strptime(circletime,"%Y%m%d%H%M") + timedelta(hours=-1) + timedelta(minutes=-timeshift)
        print "finish to check pm files"
        caseutils.post_test_case() 
    
        
        
    