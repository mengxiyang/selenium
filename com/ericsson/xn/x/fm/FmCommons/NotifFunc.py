'''
Created on Mar 24, 2016

@author: eyyylll
'''
from com.ericsson.xn.x.fm.FmCommons.NotifDataBase import notifMapping
from com.ericsson.xn.commons import test_logger as test
from com.ericsson.xn.commons.base_clint_for_selenium import send_trap
from com.ericsson.xn.commons.PyProperties import Properties
from com.ericsson.xn.x.fm.TestCases.case_ocgas_fm import server_info_cfg
from com.ericsson.xn.x.fm.FmCommons.FmCommon import data_init, query_alarm
from com.ericsson.xn.commons import CommonStatic
import types

    
def compare_data(notif_ne, expected_result):
    for key,value in expected_result.item():
        if notif_ne.has_key(key):
            if type(value) is not types.DictType:
                if notif_ne[key] ==  value:
                    test.passed("NBI notification attribute " + key + " accuracy test Passed. The NBI notification value is " + notif_ne[key] + ", and the expected result is " + value)
                else:
                    test.failed("NBI notification attribute " + key + " accuracy test Failed. The NBI notification value is " + notif_ne[key] + ", and the expected result is " + value)
            else:
                expected_result = value
                notif_ne = notif_ne[key]
                compare_data(notif_ne,expected_result)
        else:
            test.failed("NBI notification attribute " + key + " accuracy test Failed for " + key + " missing in NBI notification")
            
    
    for key_n,value_n in notif_ne.item():
        if expected_result.has_key(key_n) == None:
            test.failed("NBI notification attribute " + key + " accuracy test Failed for extra attribute " + key)
            

def get_nodeid_from_db(nename):
                       
    
def getNBINotification(basemgr_ip,basemgr_port,basemgr_pwd,ne_type,alarm_type,host_ip):
    
def check_notify__data_accuracy(ne_info_cfg,server_info_cfg,mapping_info_cfg,common_cfg):
    dict_ne_info,dict_server_info,dict_browser_chrome = data_init(ne_info_cfg,server_info_cfg,mapping_info_cfg,common_cfg)
    driver = CommonStatic.login_rsnms(dict_browser_chrome,dict_server_info["host"],dict_server_info["username"],dict_server_info["password"],dict_server_info["port"],dict_server_info["url"])
    if driver:
        try:
            NeCommon.to_ne_management_page_by_url(driver,server_info)
            new_ne_info=NeCommon.check_and_add_ne(driver, dict_ne_info)
            ne_name = new_ne_info["ne_name"]
            if dict_ne_info["ne_type"] == "LTEHSS" or dict_ne_info["ne_type"] == "IMSHSS":
                snmp_auth_info = []
                snmp_auth_info.append(dict_ne_info["usm_user"])
                snmp_auth_info.append(dict_ne_info["auth_password"])
                snmp_auth_info.append(dict_ne_info["priv_password"])
            else:
                snmp_auth_info = []
                
            FmCommon.toAlarmManagement_by_url(driver,dict_server_info)
            FmCommon.init_and_search(driver,ne_name)
            mappingInstance = notifMapping(common_cfg)
            alarm_type_list = mappingInstance.dict_mapping_info["alarm_types"]
            for alarm_type in alarm_type_list:
                test.info("send and get NBI notification: " + dict_ne_info["ne_type"] + ":" + alarm_type + "...")
                alarm_raw = getNBINotification(dict_ne_info["ne_ip"], 7070, 'xoambaseserver',dict_ne_info["ne_type"],alarm_type,dict_server_info["host"],snmp_auth_info)
                error_code = int(alarm_raw["code"])
                if error_code==1:
                    query_alarm(driver)
                    alarm_trap = alarm_raw["trap"]
                    nbi_notif = alarm_raw["nbi"]
                    test.info("send and get NBI notification successfully.TrapInfo:" + str(alarm_trap) + " and NotifInfo:" + str(nbi_notif))
                    check_notif_items = tuple(mappingInstance.dict_mapping_info("notif_attr_names"))
                    mappingInstance.check_attr_accuacy(alarm_trap,nbi_notif,dict_ne_info['nename'],check_notif_items)
