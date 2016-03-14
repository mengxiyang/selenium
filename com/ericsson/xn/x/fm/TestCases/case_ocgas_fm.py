'''
Created on Mar 1, 2016

@author: eyyylll
'''

import os
from com.ericsson.xn.x.fm.FmCommons.DataBase import check_alarm_data_accuracy
from com.ericsson.xn.commons import caseutils
from com.ericsson.xn.commons.caseutils import pre_test_case, post_test_case

root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__))).split('com' + os.sep + 'ericsson' + os.sep + 'xn' + os.sep + 'x' + os.sep + 'fm' + os.sep + 'TestCases')[0]
server_info_cfg = root_dir +  "x" + os.sep  + "pm" + os.sep + "execute_conf.cfg"
ne_info_cfg = root_dir + "x" + os.sep + "pm" + os.sep + "nes" + os.sep + "ocgas.cfg"
alarm_mapping_cfg = root_dir + "x" + os.sep + "fm" + os.sep + "mapping" + os.sep + "ocgas.cfg"

def check_ocgas_alarm_accuracy(): 
    pre_test_case("check_ocgas_alarm_accuracy_case","alarm_accuracy")
    check_alarm_data_accuracy(ne_info_cfg,server_info_cfg,alarm_mapping_cfg)
    post_test_case()
    
