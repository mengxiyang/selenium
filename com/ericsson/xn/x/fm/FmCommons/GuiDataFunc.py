#-*- coding: UTF-8 -*
'''
Created on Mar 1, 2016

@author: eyyylll
'''



from com.ericsson.xn.commons import test_logger
import datetime,time
from com.ericsson.xn.commons.PyProperties import Properties
import os
from com.ericsson.xn.commons import CommonStatic
from com.ericsson.xn.x.fm.FmCommons import FmCommon
from com.ericsson.xn.x.ne import NeCommon
from com.ericsson.xn.commons import base_clint_for_selenium
import re
import types
from com.ericsson.xn.x.fm.FmCommons import AlarmMapping
from selenium.common.exceptions import TimeoutException
from com.ericsson.xn.x.fm.FmCommons.FmCommon import data_init

def check_alarm_data_accuracy(ne_info_cfg,server_info_cfg,alarm_mapping_cfg):

    dict_ne_info,dict_server_info,dict_browser_chrome = data_init(ne_info_cfg,server_info_cfg)
    server_info = Properties(server_info_cfg)
    mappingInstance = AlarmMapping.alarmMapping(alarm_mapping_cfg)
    driver = CommonStatic.login_rsnms(dict_browser_chrome,dict_server_info["host"],dict_server_info["username"],dict_server_info["password"],dict_server_info["port"],dict_server_info["url"])

    if driver:
        try:
            NeCommon.to_ne_management_page_by_url(driver,server_info)
            new_ne_info=NeCommon.check_and_add_ne(driver, dict_ne_info)
            ne_name = new_ne_info["ne_name"]
            nodeid = base_clint_for_selenium.get_nodeid_by_nename(dict_server_info["host"],7070,'xoambaseserver',ne_name)
            time.sleep(60)
            FmCommon.toAlarmManagement_by_url(driver,server_info)
            FmCommon.init_and_search(driver,ne_name)

            alarmtypes = mappingInstance.dict_mapping_info["alarm_types"]
            alarm_type_list = []
            if type(alarmtypes) is types.StringType:
                alarm_type_list.append(alarmtypes)
            else:
                alarm_type_list = alarmtypes
            if dict_ne_info["ne_type"] in ("LTEHSS","IMSHSS","MSC","HLR","3GSGSN","GGSN"):
                snmp_auth_info = []
                snmp_auth_info.append(dict_ne_info["usm_user"])
                snmp_auth_info.append(dict_ne_info["auth_password"])
                snmp_auth_info.append(dict_ne_info["priv_password"])
            else:
                snmp_auth_info = None

            for alarm_type in alarm_type_list:
                test_logger.info("send alarm trap: " + dict_ne_info["ne_type"] + ":" + alarm_type + "...")
                alarm_from_ne = base_clint_for_selenium.send_trap(dict_ne_info["ne_ip"], 7070, 'xoambaseserver',dict_ne_info["ne_type"],alarm_type,dict_server_info["host"],snmp_auth_info)
                error_code = int(alarm_from_ne["code"])
                if error_code==1:
                    alarm_trap=alarm_from_ne["trap"]
                    test_logger.info("alarm sent successfully" + str(alarm_trap))
                    alarm_expected=alarm_converter(dict_ne_info["ne_type"],ne_name,alarm_type,alarm_trap,mappingInstance)
                    alarm_on_gui=FmCommon.fetch_alarm_on_gui(driver,dict_ne_info["ne_type"],alarm_trap,mappingInstance,alarm_type)
                    if alarm_on_gui != None:
                        test_logger.info("start to check alarm type: " + dict_ne_info["ne_type"] + ":" + alarm_type)
                        alarm_compare(alarm_expected,alarm_on_gui)
                    else:
                        test_logger.failed(dict_ne_info["ne_type"] + ":" + alarm_type + " accuracy test failed," + "reason:alarm not received on GUI")
                elif error_code < 0:
                    test_logger.failed(dict_ne_info["ne_type"] + ":" + alarm_type + " accuracy test failed, reason:sending alarm trap failed, the error msg is:" + alarm_from_ne["msg"])

            FmCommon.quitDriver(driver)
        except TimeoutException:
            FmCommon.quitDriver(driver)
            test_logger.error("find widget Timeout")
        except Exception as e:
            FmCommon.quitDriver(driver)
            test_logger.error(str(e))





def alarm_compare(alarm_expected,alarm_on_gui):
    for name,value in alarm_expected.items():
        if alarm_on_gui.has_key(name):
            if (alarm_on_gui[name] == value):
                test_logger.passed("alarm counter " + name + " accuracy test passed. GUI value is " + str(alarm_on_gui[name]) + ", and the expected value is " + str(value))
            else:
                test_logger.failed("alarm counter " + name + " accuracy test failed. GUI value is " + alarm_on_gui[name] + " ,and the expected value is " + str(value))
        else:
            test_logger.failed("alarm counter " + name + " missing on GUI")

    for name,value in alarm_on_gui.items():
        if not alarm_expected.has_key(name):
            test_logger.failed("extra alarm counter " + name + " on GUI")

            
def alarm_converter(netype,nename,alarmtype,alarm_raw,mappingInstance):
    alarm_fields = mappingInstance.get_property("alarm_gui_name")
    expected_alarm = {}.fromkeys(alarm_fields)
    for key in expected_alarm.keys():
        if(key == "网元名称"):
            expected_alarm["网元名称"]=nename
        elif(key == "告警级别"):
            if alarm_raw.has_key("alarmLevel"):
                ne_severity = alarm_raw["alarmLevel"]
                gui_severity = mappingInstance.convert_alarm_severity(ne_severity)
                if gui_severity:
                    expected_alarm["告警级别"]= gui_severity
            else:
                test_logger.failed("get alarmLevel from trap Failed")
        elif(key == "告警时间"):
            if alarm_raw.has_key("timeStamp"):
                ne_event_time = alarm_raw["timeStamp"]
                if (re.findall(r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}.\d{3}",ne_event_time)[0]!= None):
                    expected_alarm["告警时间"] = ne_event_time
                else:
                    test_logger.failed("Incorrect eventTime format on Node")
            else:
                test_logger.failed("get timeStamp from trap Failed ")
        elif(key == "清除状态"):
            expected_alarm["清除状态"] = "未清除"
        elif(key == "确认状态"):
            expected_alarm["确认状态"] = "未确认"
        elif(key == "告警编号"):
            gui_alarmtype_id = mappingInstance.convert_alarmtype_id(alarmtype)
            if gui_alarmtype_id:
                expected_alarm["告警编号"]=gui_alarmtype_id
        elif(key == "告警名称"):
            gui_alarmtype_cn = mappingInstance.convert_alarmtype_cn(alarmtype)
            if gui_alarmtype_cn:
                expected_alarm["告警名称"] = gui_alarmtype_cn
        elif(key == "定位信息"):
            if alarm_raw.has_key("alarmSource"):
                ne_source_info =  alarm_raw["alarmSource"]
                expected_alarm["定位信息"] = ne_source_info
            else:
                test_logger.failed("The managedObject can't be found on Node")
        elif(key == "清除时间"):
            expected_alarm["清除时间"] = ""
        elif(key == "清除类型"):
            expected_alarm["清除类型"] = ""
        elif(key == "确认时间"):
            expected_alarm["确认时间"] = ""
        elif(key == "确认用户"):
            expected_alarm["确认用户"] = ""
        elif(key == "问题描述"):
            if netype in ("OCGAS","GMLC"):
                specific_problem = mappingInstance.convert_specific_problem(alarmtype)
            else:
                if alarm_raw.has_key("specificProblem"):
                    specific_problem = alarm_raw["specificProblem"]
                else:
                    test_logger.failed("get specificProblem from trap Failed")
            if specific_problem:
                expected_alarm["问题描述"] = specific_problem
        elif(key == "可能原因"):
            if alarm_raw.has_key("probableCause"):
                ne_probableCause = alarm_raw["probableCause"]
                probable_cause = mappingInstance.convert_probable_cause(ne_probableCause)
                if probable_cause:
                    expected_alarm["可能原因"] = probable_cause
            else:
            		test_logger.failed("get probableCause from trap Failed")                

        elif(key == "告警类型"):
            if alarm_raw.has_key("alarmCategory"):
                ne_event_type = alarm_raw["alarmCategory"]
                gui_event_type = mappingInstance.convert_event_type(ne_event_type)
                if gui_event_type:
                    expected_alarm["告警类型"] = gui_event_type
            else:
                test_logger.failed("get alarmCategory from trap Failed")
        elif(key == "补充信息"):
            if alarm_raw.has_key("alarmDescription"):
                expected_alarm["补充信息"] = alarm_raw["alarmDescription"]
            else:
                test_logger.failed("get alarmDescription from trap Failed")
        elif(key == "变更时间"):
                expected_alarm["变更时间"] = ""


    return expected_alarm


