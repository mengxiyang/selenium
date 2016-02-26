from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import test_logger
from com.ericsson.xn.commons import caseutils

nes_info={"SGW":{"ne_type":"SGW","nename":"SGW72","nodeid":"abcd","licid":"ttttt","interval":15,"time":"201602181300"}}

def check_pm_sgw():
    global nes_info
    caseutils.pre_test_case("check_nbi_pm_"+nes_info["SGW"]["ne_type"]+"_rop="+str(nes_info["SGW"]["interval"])+"_cases", "nbi_pm_automation")
    NBIPmFunc.PMCmpInstance(nes_info["SGW"]["ne_type"],nes_info["SGW"]["nename"],nes_info["SGW"]["nodeid"],nes_info["SGW"]["licid"],nes_info["SGW"]["interval"],nes_info["SGW"]["time"]).check_pm_accuracy()  
    caseutils.post_test_case()