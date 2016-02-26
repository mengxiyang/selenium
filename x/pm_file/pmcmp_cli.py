from optparse import OptionParser
from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import test_logger
from com.ericsson.xn.commons import caseutils
import re

def get_options():
    
    parser = OptionParser(usage="usage: %prog -t <netype> -n <nename> -o <nodeid> [-l <licid>] [-i <interval>] [-p <timestamp>]")

    parser.add_option("-i", "--interval", action="store", type="int", dest="interval", default=15,
                      help="specify the rop of northbound pm file[5|15]. The default rop is 15")

    parser.add_option("-t", "--type", action="store", type="string", dest="ne_type", default="",
                      help="specify the netype")

    parser.add_option("-n", "--nename", action="store", type="string", dest="nename", default="",
                      help="specify the nename")

    parser.add_option("-o", "--nodeid", action="store", type="string", dest="nodeid", default="",
                      help="specify the nodeid")

    parser.add_option("-l", "--licid", action="store", type="string", dest="licid", default="",
                      help="specify the licId and no need to input for NEs of AS, IMSHSS and LTEHSS")

    parser.add_option("-p", "--timestamp", action="store", type="string", dest="time", default="",
                      help="specify the timestamp back from which to process the pm file[YYmmddHHMM]")

    (options, args) = parser.parse_args()


    if (options.ne_type == ""):
        print "-t is mandatory to input."
        parser.print_help()
        return -1

    if (options.nename == ""):
        print "-n is mandatory to input."
        parser.print_help()
        return -1

    if (options.nodeid == ""):
        print "-o is mandatory to input."
        parser.print_help()
        return -1

    if (options.ne_type.lower() != 'sgsn' and options.ne_type.lower() != 'mme' and options.ne_type.lower() != 'sgw' and options.ne_type.lower() != 'pgw' and options.ne_type.lower() != 'as' and options.ne_type.lower() != 'sbc' and options.ne_type.lower() != 'imshss' and options.ne_type.lower() != 'ltehss'):
        print "Only support NETYPE including SGSN,MME,SGW,PGW,AS,SBC,IMSHSS and LTEHSS."
        parser.print_help()
        return -1

    if (options.interval % 5):
        print "incorrect interval.It must be multiples of 5"
        parser.print_help()
        return -1

    if options.time != "":

        pattern = re.compile(r'\d{12}')
        match = pattern.match(options.time)

        if match == None:
            print "The input pm_timestamp must be in format of YYmmddHHMM."
            parser.print_help()
            return -1

    return options



if __name__ == '__main__':  
    options=get_options()
    if options!=-1:
        caseutils.pre_test_case("check_nbi_pm_"+options.ne_type.lower()+"_rop="+str(options.interval)+"_cases", "nbi_pm_automation")
        NBIPmFunc.PMCmpInstance(options.ne_type,options.nename,options.nodeid,options.licid,options.interval,options.time).check_pm_accuracy()  
        caseutils.post_test_case()
