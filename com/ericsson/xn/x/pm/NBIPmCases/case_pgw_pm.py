from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import test_logger

nes_info =  {"PGW":{"ne_type":"PGW","nename":"PGW72","nodeid":"default","licid":"LLLLtest","interval":15,"time":"201602181300"}}

def check_pm_pgw():
    global nes_info
    test_logger.init_logger_instance("check_nbi_pm_"+nes_info["PGW"]["ne_type"]+"_rop="+str(nes_info["PGW"]["interval"])+"_cases", "nbi_pm_automation")    
    NBIPmFunc.PMCmpInstance(nes_info["PGW"]["ne_type"],nes_info["PGW"]["nename"],nes_info["PGW"]["nodeid"],nes_info["PGW"]["licid"],nes_info["PGW"]["interval"],nes_info["PGW"]["time"],test_logger).check_pm_accuracy()  
    test_logger.finish_test_steps()