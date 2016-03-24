'''
Created on Mar 24, 2016

@author: eyyylll
'''
from com.ericsson.xn.x.fm.FmCommons.NotifDataBase import notifMapping
from com.ericsson.xn.commons import test_logger as test
from com.ericsson.xn.commons.base_clint_for_selenium import send_trap
from com.ericsson.xn.commons.PyProperties import Properties
from com.ericsson.xn.x.fm.TestCases.case_ocgas_fm import server_info_cfg
from com.ericsson.xn.x.fm.FmCommons.FmCommon import init_data

    
def compare_data(notif_ne, expected_result):
    
    
def dn_transformer():
    
    
def get_notif(attr_name):
    
    

def check_notify__data_accuracy(ne_info_cfg,server_info_cfg,mapping_info_cfg,common_cfg):
    dict_ne_info,dict_server_info,dict_browser_info = init_data(ne_info_cfg,server_info_cfg,mapping_info_cfg,common_cfg)
    mappingInstance = notifMapping(common_cfg,mapping_info_cfg)
    alarm_type_list = mappingInstance.dict_mapping_info["alarm_types"]
    for alarm_type in alarm_type_list:
        test.info("send alarm trap: " + dict_ne_info["ne_type"] + ":" + alarm_type + "...")
        alarm_from_ne = send_trap(dict_ne_info["ne_ip"], 7070, 'xoambaseserver',dict_ne_info["ne_type"],alarm_type,dict_server_info["host"])
        error_code = int(alarm_from_ne["code"])
        if error_code==1:
            alarm_trap=alarm_from_ne["trap"]
            test.info("alarm sent successfully" + str(alarm_trap))
            check_notif_items = mappingInstance.dict_mapping_info("notif_attr_names")
            for item in check_notif_items:
                notif_value = get_notif(item)
                expected_value = mappingInstance.dict_mapping_info.get_property(item)
                if "event_name" == item:
                    ne_event_name = alarm_trap["alarmLevel"]
                    mapped_event_name = mappingInstance.convert_event_type(ne_event_name)
                    expected_value.update("event_name":mapped_event_name)
                    compare_data(notif_value,expected_value)
                else:
                    compare_data(notif_value,expected_value)
                    