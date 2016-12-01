from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import test_logger
from com.ericsson.xn.commons import caseutils

nes_info =  {"MME":{"ne_type":"MME","nename":"MME76","nodeid":"8613743641","licid":"LTE987654321","interval":15,"time":"201602030600"}}

def check_pm_mme():
    global nes_info
    caseutils.pre_test_case("check_nbi_pm_"+nes_info["MME"]["ne_type"]+"_rop="+str(nes_info["MME"]["interval"])+"_cases", "nbi_pm_automation")
    NBIPmFunc.PMCmpInstance(nes_info["MME"]["ne_type"],nes_info["MME"]["nename"],nes_info["MME"]["nodeid"],nes_info["MME"]["licid"],nes_info["MME"]["interval"],nes_info["MME"]["time"]).check_pm_accuracy()  
    caseutils.post_test_case()