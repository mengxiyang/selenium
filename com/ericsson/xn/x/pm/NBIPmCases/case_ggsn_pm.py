from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import caseutils
from com.ericsson.xn.commons import test_logger

nes_info = {"GGSN":{"ne_type":"GGSN","nename":"GGSN-53E2DB0004389683","nodeid":"260","licid":"","interval":15,"time":"201608040900"}}

def check_pm_ggsn():
    global  nes_info
    caseutils.pre_test_case("check_nbi_pm_"+nes_info["GGSN"]["ne_type"]+"_rop="+str(nes_info["GGSN"]["interval"])+"_cases", "nbi_pm_automation")
    NBIPmFunc.PMCmpInstance(nes_info["GGSN"]["ne_type"],nes_info["GGSN"]["nename"],nes_info["GGSN"]["nodeid"],nes_info["GGSN"]["licid"],nes_info["GGSN"]["interval"],nes_info["GGSN"]["time"]).check_pm_accuracy()
    caseutils.post_test_case()
    
    
check_pm_ggsn()