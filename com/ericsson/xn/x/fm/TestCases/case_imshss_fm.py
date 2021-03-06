'''
Created on Mar 1, 2016

@author: eyyylll
'''

import os
from com.ericsson.xn.x.fm.FmCommons.GuiDataFunc import check_alarm_data_accuracy
from com.ericsson.xn.commons.caseutils import pre_test_case, post_test_case

root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__))).split('com' + os.sep + 'ericsson' + os.sep + 'xn' + os.sep + 'x' + os.sep + 'fm' + os.sep + 'TestCases')[0]
server_info_cfg = root_dir +  "x" + os.sep  + "pm" + os.sep + "execute_conf.cfg"
ne_info_cfg = root_dir + "x" + os.sep + "pm" + os.sep + "nes" + os.sep + "imshss.cfg"
alarm_mapping_cfg = root_dir + "x" + os.sep + "fm" + os.sep + "gui_mapping" + os.sep + "hss.cfg"

def check_imshss_alarm_accuracy():
    pre_test_case("check_imshss_gui_accuracy_case","gui_fm_accuracy")
    check_alarm_data_accuracy(ne_info_cfg,server_info_cfg,alarm_mapping_cfg)
    post_test_case()

