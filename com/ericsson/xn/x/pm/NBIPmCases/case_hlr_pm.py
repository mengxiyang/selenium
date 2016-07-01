from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import caseutils
from com.ericsson.xn.commons import test_logger

nes_info = {"HLR":{"ne_type":"HLR","nename":"HLR-354FAE463B4D0C98","nodeid":"111","licid":"","interval":15,"time":"201607010500"}}

def check_pm_hlr():
    global  nes_info
    caseutils.pre_test_case("check_nbi_pm_"+nes_info["HLR"]["ne_type"]+"_rop="+str(nes_info["HLR"]["interval"])+"_cases", "nbi_pm_automation")
    NBIPmFunc.PMCmpInstance(nes_info["HLR"]["ne_type"],nes_info["HLR"]["nename"],nes_info["HLR"]["nodeid"],nes_info["HLR"]["licid"],nes_info["HLR"]["interval"],nes_info["HLR"]["time"]).check_pm_accuracy()
    caseutils.post_test_case()