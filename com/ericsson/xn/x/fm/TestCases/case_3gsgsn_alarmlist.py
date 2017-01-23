'''
Created on Apr 14, 2016

@author: eyyylll
'''
from com.ericsson.xn.x.fm.FmCommons.AlarmListFunc import check_alarm_list_accuracy
from com.ericsson.xn.commons.caseutils import  pre_test_case,post_test_case
import os

root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__))).split('com' + os.sep + 'ericsson' + os.sep + 'xn' + os.sep + 'x' + os.sep + 'fm' + os.sep + 'TestCases')[0]
getalarmlist_mapping_cfg_new = root_dir + os.sep + 'x' + os.sep + 'fm' + os.sep + 'nbi_mapping' + os.sep + 'ims_get_alarm_list_new_alarm.cfg'
getalarmlist_mapping_cfg_clear = root_dir + os.sep + 'x' + os.sep + 'fm' + os.sep + 'nbi_mapping' + os.sep + 'ims_get_alarm_list_clear_alarm.cfg'
getalarmlist_mapping_cfg_change = root_dir + os.sep + 'x' + os.sep + 'fm' + os.sep + 'nbi_mapping' + os.sep + 'ims_get_alarm_list_change_alarm.cfg'
server_info_cfg = root_dir + os.sep + 'x' + os.sep + 'pm' + os.sep + 'execute_conf.cfg'
ne_info_cfg = root_dir + os.sep + 'x' + os.sep + 'pm' + os.sep + 'nes' + os.sep + '3gsgsn.cfg'


def check_get_alarmlist_accuracy():
    pre_test_case("check_3gsgsn_get_alarmlist_case","nbi_get_alarm_list")
    check_alarm_list_accuracy(ne_info_cfg,server_info_cfg,getalarmlist_mapping_cfg_new)
    #check_alarm_list_accuracy(ne_info_cfg,server_info_cfg,getalarmlist_mapping_cfg_clear)
    check_alarm_list_accuracy(ne_info_cfg,server_info_cfg,getalarmlist_mapping_cfg_change)
    post_test_case()