'''
Created on Apr 14, 2016

@author: eyyylll
'''
from com.ericsson.xn.x.fm.FmCommons.AlarmListFunc import check_alarm_list_accuracy
from com.ericsson.xn.commons.caseutils import  pre_test_case,post_test_case
import os

root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__))).split('com' + os.sep + 'ericsson' + os.sep + 'xn' + os.sep + 'x' + os.sep + 'fm' + os.sep + 'TestCases')[0]
notify_mapping_cfg = root_dir + os.sep + 'x' + os.sep + 'fm' + os.sep + 'nbi_mapping' + os.sep + 'hss_get_alarm_list_new_alarm.cfg'
server_info_cfg = root_dir + os.sep + 'x' + os.sep + 'pm' + os.sep + 'execute_conf.cfg'
ne_info_cfg = root_dir + os.sep + 'x' + os.sep + 'pm' + os.sep + 'nes' + os.sep + 'imshss.cfg'


def check_imshss_get_alarmlist_accuracy():
    pre_test_case("check_imshss_get_alarmlist_case","nbi_get_alarm_list")
    check_alarm_list_accuracy(ne_info_cfg,server_info_cfg,notify_mapping_cfg)
    post_test_case()