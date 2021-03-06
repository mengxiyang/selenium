from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import test_logger
from com.ericsson.xn.commons import caseutils

nes_info = {"SGSN":{"ne_type":"SGSN","nename":"SGSN76","nodeid":"8613743640","licid":"LTE123456789-modify","interval":15,"time":"201602030600"}}

def check_pm_sgsn():
    global nes_info
    caseutils.pre_test_case("check_nbi_pm_"+nes_info["SGSN"]["ne_type"]+"_rop="+str(nes_info["SGSN"]["interval"])+"_cases", "nbi_pm_automation")  
    NBIPmFunc.PMCmpInstance(nes_info["SGSN"]["ne_type"],nes_info["SGSN"]["nename"],nes_info["SGSN"]["nodeid"],nes_info["SGSN"]["licid"],nes_info["SGSN"]["interval"],nes_info["SGSN"]["time"]).check_pm_accuracy()  
    caseutils.post_test_case()