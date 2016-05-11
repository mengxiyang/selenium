'''
Created on Apr 13, 2016

@author: eyyylll
'''

from com.ericsson.xn.commons import test_logger as test
from com.ericsson.xn.commons.PyProperties import Properties
from com.ericsson.xn.x.fm.FmCommons.FmCommon import data_init,quitDriver
from com.ericsson.xn.commons import CommonStatic
from com.ericsson.xn.x.ne import  NeCommon
from com.ericsson.xn.x.fm.FmCommons import AlarmMapping
import types
from com.ericsson.xn.commons import base_clint_for_selenium
from selenium.common.exceptions import TimeoutException
import time
from com.ericsson.xn.x.fm.FmCommons import NotifFunc

def check_alarm_list_accuracy(ne_info_cfg,server_info_cfg,mapping_info_cfg):
    dict_ne_info,dict_server_info,dict_browser_chrome = data_init(ne_info_cfg,server_info_cfg)
    server_info = Properties(server_info_cfg)
    driver = CommonStatic.login_rsnms(dict_browser_chrome,dict_server_info["host"],dict_server_info["username"],dict_server_info["password"],dict_server_info["port"],dict_server_info["url"])
    if driver:
        try:
            NeCommon.to_ne_management_page_by_url(driver,server_info)
            new_ne_info=NeCommon.check_and_add_ne(driver,dict_ne_info)
            ne_name = new_ne_info["ne_name"]
            #ne_name = 'IMSHSS-9A8ACC8039B1B283'
            quitDriver(driver)

            mappingInstance = AlarmMapping.alarmMapping(mapping_info_cfg)
            #nodeid = get_nodeid_by_nename(ne_name,mysqlInst)

            nodeid = base_clint_for_selenium.get_nodeid_by_nename(dict_server_info["host"],7070,'xoambaseserver',ne_name)
            time.sleep(60)
            if nodeid == False:
                test.error("update nodeid Failure")
                
            if dict_ne_info["ne_type"] == "LTEHSS" or dict_ne_info["ne_type"] == "IMSHSS":
                snmp_auth_info = []
                snmp_auth_info.append(dict_ne_info["usm_user"])
                snmp_auth_info.append(dict_ne_info["auth_password"])
                snmp_auth_info.append(dict_ne_info["priv_password"])
            else:
                snmp_auth_info = None

            alarmtypes = mappingInstance.dict_mapping_info["alarm_types"]
            alarm_type_list = []
            if type(alarmtypes) is types.StringType:
                alarm_type_list.append(alarmtypes)
            else:
                alarm_type_list = alarmtypes

            for alarm_type in alarm_type_list:
                test.info("send and get alarmlist result for " + dict_ne_info["ne_type"] + ":" + alarm_type + "...")
                alarm_raw = NotifFunc.getNBINotification(dict_ne_info["ne_ip"], 7070, 'xoambaseserver',dict_ne_info["ne_type"],alarm_type,dict_server_info["host"],snmp_auth_info)
                #alarm_raw = base_clint_for_selenium.send_trap_nbi(dict_ne_info["ne_ip"],7070,'xoambaseserver',dict_ne_info["ne_type"],alarm_type,dict_server_info["host"],auth_info=snmp_auth_info)
                error_code = int(alarm_raw["code"])
                if error_code==1:
                    alarm_trap = alarm_raw["trap"]
                    nbi_alarm_list = alarm_raw["nbi"]
                    test.info("get TrapInfo is:" + str(alarm_trap) + " and AlarmList is:" + str(nbi_alarm_list))
                    test.info("start to check " + alarm_type)
                    check_alarmlist_attrs = mappingInstance.get_property("alarmlist_attrs")
                    attr_list = []
                    if type(check_alarmlist_attrs) is types.StringType:
                        attr_list.append(check_alarmlist_attrs)
                    else:
                        attr_list = check_alarmlist_attrs
                    NotifFunc.check_attr_accuracy(mappingInstance,alarm_trap,nbi_alarm_list,ne_name,nodeid,attr_list,dict_server_info)
                else:
                    test.failed(dict_ne_info["ne_type"] + ":" + alarm_type + " accuracy test failed, reason:sending alarm trap failed, the error msg is:" + alarm_raw["msg"])

        except TimeoutException:
            test.error("find widget timeout")
        except Exception as e:
            test.error(str(e))

