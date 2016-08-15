from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import caseutils
from com.ericsson.xn.commons import test_logger

nes_info = {"3GSGSN":{"ne_type":"3GSGSN","nename":"3GSGSN-B99AB11D7C143F57","nodeid":"160","licid":"","interval":15,"time":"201608041800"}}

def check_pm_3gsgsn():
    global  nes_info
    caseutils.pre_test_case("check_nbi_pm_"+nes_info["3GSGSN"]["ne_type"]+"_rop="+str(nes_info["3GSGSN"]["interval"])+"_cases", "nbi_pm_automation")
    NBIPmFunc.PMCmpInstance(nes_info["3GSGSN"]["ne_type"],nes_info["3GSGSN"]["nename"],nes_info["3GSGSN"]["nodeid"],nes_info["3GSGSN"]["licid"],nes_info["3GSGSN"]["interval"],nes_info["3GSGSN"]["time"]).check_pm_accuracy()
    caseutils.post_test_case()