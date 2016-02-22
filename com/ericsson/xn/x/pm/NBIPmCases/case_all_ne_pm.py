from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import test_logger

nes_info = {"SGSN":{"ne_type":"SGSN","nename":"SGSN76","nodeid":"8613743640","licid":"LTE123456789-modify","interval":15,"time":"201602030600"},
            "MME":{"ne_type":"MME","nename":"MME76","nodeid":"8613743641","licid":"LTE987654321","interval":15,"time":"201602030600"},
           "SGW":{"ne_type":"SGW","nename":"SGW72","nodeid":"abcd","licid":"ttttt","interval":15,"time":"201602181300"},
           "PGW":{"ne_type":"PGW","nename":"PGW72","nodeid":"default","licid":"LLLLtest","interval":15,"time":"201602181300"},
           "AS":{"ne_type":"AS","nename":"ocgas67","nodeid":"1","licid":"","interval":15,"time":"201602010900"},
           "IMSHSS":{"ne_type":"IMSHSS","nename":"HSSIMS77","nodeid":"HSS_IMS","licid":"","interval":5,"time":"201602181700"},
           "LTEHSS":{"ne_type":"LTEHSS","nename":"HSSLTE77","nodeid":"HSS_LTE","licid":"","interval":5,"time":"201602181700"}
           }
           

def check_pm_all_nes():
    global nes_info
    test_logger.init_logger_instance("check_nbi_pm_all_nes_cases", "nbi_pm_automation")
    for ne,info in nes_info.items():
        test_logger.info("Start to check pm data of " + info["ne_type"])     
        NBIPmFunc.PMCmpInstance(info["ne_type"],info["nename"],info["nodeid"],info["licid"],info["interval"],info["time"],test_logger).check_pm_accuracy()  
    test_logger.finish_test_steps()