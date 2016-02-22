from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import test_logger

nes_info = {"IMSHSS":{"ne_type":"IMSHSS","nename":"HSSIMS77","nodeid":"HSS_IMS","licid":"","interval":5,"time":"201602181700"}}

def check_pm_imshss():
    global  nes_info
    test_logger.init_logger_instance("check_nbi_pm_"+nes_info["IMSHSS"]["ne_type"]+"_rop="+str(nes_info["IMSHSS"]["interval"])+"_cases", "nbi_pm_automation")    
    NBIPmFunc.PMCmpInstance(nes_info["IMSHSS"]["ne_type"],nes_info["IMSHSS"]["nename"],nes_info["IMSHSS"]["nodeid"],nes_info["IMSHSS"]["licid"],nes_info["IMSHSS"]["interval"],nes_info["IMSHSS"]["time"],test_logger).check_pm_accuracy()  
    test_logger.finish_test_steps()