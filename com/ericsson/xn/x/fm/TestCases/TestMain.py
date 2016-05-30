from com.ericsson.xn.x.fm.TestCases import case_ocgas_gui
from com.ericsson.xn.x.fm.TestCases import case_ltehss_gui
from com.ericsson.xn.x.fm.TestCases import case_imshss_gui
from com.ericsson.xn.x.fm.TestCases import case_imshss_nbi
from com.ericsson.xn.x.fm.TestCases import case_ltehss_nbi
from com.ericsson.xn.x.fm.TestCases import case_imshss_alarmlist
from com.ericsson.xn.x.fm.TestCases import case_ltehss_alarmlist

if __name__ == '__main__':
    
    case_ocgas_gui.check_ocgas_alarm_accuracy()
    case_imshss_gui.check_imshss_alarm_accuracy()
    case_ltehss_gui.check_ltehss_alarm_accuracy()
    case_imshss_nbi.check_imshss_nbi_accuracy()
    case_ltehss_nbi.check_ltehss_nbi_accuracy()
    case_imshss_alarmlist.check_alarm_list_accuracy()
    case_ltehss_alarmlist.check_alarm_list_accuracy()

