from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import caseutils
from com.ericsson.xn.commons import test_logger

nes_info = {"MSC":{"ne_type":"MSC","nename":"MSC-941733D94DA78236","nodeid":"11","licid":"","interval":15,"time":"201607061400"}}

def check_pm_msc():
    global  nes_info
    caseutils.pre_test_case("check_nbi_pm_"+nes_info["MSC"]["ne_type"]+"_rop="+str(nes_info["MSC"]["interval"])+"_cases", "nbi_pm_automation")
    NBIPmFunc.PMCmpInstance(nes_info["MSC"]["ne_type"],nes_info["MSC"]["nename"],nes_info["MSC"]["nodeid"],nes_info["MSC"]["licid"],nes_info["MSC"]["interval"],nes_info["MSC"]["time"]).check_pm_accuracy()
    caseutils.post_test_case()