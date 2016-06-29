from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import caseutils
from com.ericsson.xn.commons import test_logger

nes_info = {"GMLC":{"ne_type":"GMLC","nename":"GMLC77","nodeid":"12345","licid":"","interval":15,"time":"201606291200"}}

def check_pm_gmlc():
    global  nes_info
    caseutils.pre_test_case("check_nbi_pm_"+nes_info["GMLC"]["ne_type"]+"_rop="+str(nes_info["GMLC"]["interval"])+"_cases", "nbi_pm_automation")
    NBIPmFunc.PMCmpInstance(nes_info["GMLC"]["ne_type"],nes_info["GMLC"]["nename"],nes_info["GMLC"]["nodeid"],nes_info["GMLC"]["licid"],nes_info["GMLC"]["interval"],nes_info["GMLC"]["time"]).check_pm_accuracy()
    caseutils.post_test_case()