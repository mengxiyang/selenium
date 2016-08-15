from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import test_logger
from com.ericsson.xn.commons import caseutils

nes_info =  {"PGW":{"ne_type":"PGW","nename":"PGW58","nodeid":"NodeIdpgw58","licid":"LicIdpgw58","interval":15,"time":"201608031915"}}

def check_pm_pgw():
    global nes_info
    caseutils.pre_test_case("check_nbi_pm_"+nes_info["PGW"]["ne_type"]+"_rop="+str(nes_info["PGW"]["interval"])+"_cases", "nbi_pm_automation") 
    NBIPmFunc.PMCmpInstance(nes_info["PGW"]["ne_type"],nes_info["PGW"]["nename"],nes_info["PGW"]["nodeid"],nes_info["PGW"]["licid"],nes_info["PGW"]["interval"],nes_info["PGW"]["time"]).check_pm_accuracy()  
    caseutils.post_test_case()