from com.ericsson.xn.x.fm.FmCommons.NotifFunc import check_notify_accuracy
from com.ericsson.xn.commons.caseutils import  pre_test_case,post_test_case
import os

root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__))).split('com' + os.sep + 'ericsson' + os.sep + 'xn' + os.sep + 'x' + os.sep + 'fm' + os.sep + 'TestCases')[0]
notify_new_cfg = root_dir + os.sep + 'x' + os.sep + 'fm' + os.sep + 'nbi_mapping' + os.sep + 'gmlc_nbi_new_alarm.cfg'
notify_clear_cfg = root_dir + os.sep + 'x' + os.sep + 'fm' + os.sep + 'nbi_mapping' + os.sep + 'gmlc_nbi_clear_alarm.cfg'
server_info_cfg = root_dir + os.sep + 'x' + os.sep + 'pm' + os.sep + 'execute_conf.cfg'
ne_info_cfg = root_dir + os.sep + 'x' + os.sep + 'pm' + os.sep + 'nes' + os.sep + 'gmlc.cfg'


def check_gmlc_nbi_accuracy():
    pre_test_case("check_gmlc_nbi_accuracy_case","nbi_notify_accuracy")
    check_notify_accuracy(ne_info_cfg,server_info_cfg,notify_new_cfg)
    check_notify_accuracy(ne_info_cfg,server_info_cfg,notify_clear_cfg)
    post_test_case()