from com.ericsson.xn.x.fm.TestCases import case_ocgas_fm
from com.ericsson.xn.x.fm.TestCases import case_ltehss_fm
from com.ericsson.xn.x.fm.TestCases import case_imshss_fm
from com.ericsson.xn.x.fm.TestCases import case_imshss_nbi
from com.ericsson.xn.x.fm.TestCases import case_ltehss_nbi

if __name__ == '__main__':
    
    #case_ocgas_fm.check_ocgas_alarm_accuracy()
    #case_imshss_fm.check_imshss_alarm_accuracy()
    case_ltehss_fm.check_ltehss_alarm_accuracy()
    #case_imshss_nbi.check_imshss_nbi_accuracy()
    case_ltehss_nbi.check_ltehss_nbi_accuracy()

