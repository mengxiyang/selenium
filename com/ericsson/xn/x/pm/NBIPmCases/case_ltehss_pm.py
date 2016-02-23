from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import test_logger

nes_info =  {"LTEHSS":{"ne_type":"LTEHSS","nename":"HSSLTE77","nodeid":"HSS_LTE","licid":"","interval":5,"time":"201602181700"}}

def check_pm_ltehss():
    global nes_info
    test_logger.init_logger_instance("check_nbi_pm_"+nes_info["LTEHSS"]["ne_type"]+"_rop="+str(nes_info["LTEHSS"]["interval"])+"_cases", "nbi_pm_automation")    
    NBIPmFunc.PMCmpInstance(nes_info["LTEHSS"]["ne_type"],nes_info["LTEHSS"]["nename"],nes_info["LTEHSS"]["nodeid"],nes_info["LTEHSS"]["licid"],nes_info["LTEHSS"]["interval"],nes_info["LTEHSS"]["time"],test_logger).check_pm_accuracy()  
    test_logger.finish_test_steps()