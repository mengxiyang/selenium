'''
Created on Feb 26, 2016

@author: eyyylll
'''

from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import test_logger
from com.ericsson.xn.commons import caseutils

nes_info =  {"OCGAS":{"ne_type":"OCGAS","nename":"OCGAS-EADFE61FCEE92DA8","nodeid":"01","licid":"","interval":15,"time":"201608032000"}}

def check_pm_as():
    global nes_info
    caseutils.pre_test_case("check_nbi_pm_"+nes_info["OCGAS"]["ne_type"]+"_rop="+str(nes_info["OCGAS"]["interval"])+"_cases", "nbi_pm_automation")
    NBIPmFunc.PMCmpInstance(nes_info["OCGAS"]["ne_type"],nes_info["OCGAS"]["nename"],nes_info["OCGAS"]["nodeid"],nes_info["OCGAS"]["licid"],nes_info["OCGAS"]["interval"],nes_info["OCGAS"]["time"]).check_pm_accuracy()
    caseutils.post_test_case()