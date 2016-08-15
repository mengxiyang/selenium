from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import test_logger
from com.ericsson.xn.commons import caseutils

nes_info =  {"LTEHSS":{"ne_type":"LTEHSS","nename":"LTEHSS-1698E8C533EB3A5C","nodeid":"HSS_LTE","licid":"","interval":15,"time":"201608041745"}}

def check_pm_ltehss():
    global nes_info
    caseutils.pre_test_case("check_nbi_pm_"+nes_info["LTEHSS"]["ne_type"]+"_rop="+str(nes_info["LTEHSS"]["interval"])+"_cases", "nbi_pm_automation")   
    NBIPmFunc.PMCmpInstance(nes_info["LTEHSS"]["ne_type"],nes_info["LTEHSS"]["nename"],nes_info["LTEHSS"]["nodeid"],nes_info["LTEHSS"]["licid"],nes_info["LTEHSS"]["interval"],nes_info["LTEHSS"]["time"]).check_pm_accuracy()  
    caseutils.post_test_case()