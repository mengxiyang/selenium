'''
Created on Feb 26, 2016

@author: eyyylll
'''

from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import test_logger
from com.ericsson.xn.commons import caseutils

nes_info =  {"AS":{"ne_type":"AS","nename":"ocgas67","nodeid":"1","licid":"","interval":15,"time":"201602010900"}}

def check_pm_as():
    global nes_info
    caseutils.pre_test_case("check_nbi_pm_"+nes_info["AS"]["ne_type"]+"_rop="+str(nes_info["AS"]["interval"])+"_cases", "nbi_pm_automation")
    NBIPmFunc.PMCmpInstance(nes_info["AS"]["ne_type"],nes_info["AS"]["nename"],nes_info["AS"]["nodeid"],nes_info["AS"]["licid"],nes_info["AS"]["interval"],nes_info["AS"]["time"]).check_pm_accuracy()  
    caseutils.post_test_case()