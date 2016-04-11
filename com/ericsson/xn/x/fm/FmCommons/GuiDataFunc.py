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

def check_alarm_data_accuracy(ne_info_cfg,server_info_cfg,alarm_mapping_cfg):
    
    server_info = Properties(server_info_cfg)
    dict_browser_chrome = {
        "browser_type": server_info.getProperty('browser_type'),
        "browser_path": server_info.getProperty('browser_path'),
        "driver_path": server_info.getProperty('driver_path')
    }
    
    ne_info = Properties(ne_info_cfg)
    dict_ne_info  = {
        "ne_name": ne_info.getProperty("ne_name"),
        "ne_user": ne_info.getProperty("ne_user"),
        "ne_type": ne_info.getProperty("ne_type"),
        "ne_ip" : ne_info.getProperty("ne_ip"),
        "ne_password" : ne_info.getProperty("ne_password"),
        "pm_path": ne_info.getProperty("pm_path"),
        "log_path": ne_info.getProperty("log_path"),
        "alarm_path": ne_info.getProperty("alarm_path"),
        "ne_port": ne_info.getProperty("ne_port"),
        "sftp_port": ne_info.getProperty("sftp_port"),
        "snmp_port": ne_info.getProperty("snmp_port"),
        "usm_user": ne_info.getProperty("usm_user"),
        "auth_password": ne_info.getProperty("auth_password"),
        "priv_password": ne_info.getProperty("priv_password"),
        "app_user": ne_info.getProperty("app_user"),
        "app_password": ne_info.getProperty("app_password"),
        "li_pwd": ne_info.getProperty("li_pwd"),
        "fro_id": ne_info.getProperty("fro_id")
    }

    mappingInstance = AlarmMapping.alarmMapping(alarm_mapping_cfg)

    host = server_info.getProperty("host")
    username = server_info.getProperty("username")
    password = server_info.getProperty("password")
    port = server_info.getProperty("port")
    url = server_info.getProperty("url")
    
    driver = CommonStatic.login_rsnms(dict_browser_chrome,host,username,password,port,url)
    if driver:
        try:
            NeCommon.to_ne_management_page_by_url(driver,server_info)
            new_ne_info=NeCommon.check_and_add_ne(driver, dict_ne_info)
            ne_name = new_ne_info["ne_name"]
            FmCommon.toAlarmManagement_by_url(driver,server_info)
            time.sleep(10)
            FmCommon.init_and_search(driver,ne_name)

            alarmtypes = mappingInstance.dict_mapping_info["alarm_types"]
            alarm_type_list = []
            if type(alarmtypes) is types.StringType:
                alarm_type_list.append(alarmtypes)
            else:
                alarm_type_list = alarmtypes
            if dict_ne_info["ne_type"] == "LTEHSS" or dict_ne_info["ne_type"] == "IMSHSS":
                snmp_auth_info = []
                snmp_auth_info.append(dict_ne_info["usm_user"])
                snmp_auth_info.append(dict_ne_info["auth_password"])
                snmp_auth_info.append(dict_ne_info["priv_password"])
            else:
                snmp_auth_info = None

            for alarm_type in alarm_type_list:
                test_logger.info("send alarm trap: " + dict_ne_info["ne_type"] + ":" + alarm_type + "...")
                alarm_from_ne = base_clint_for_selenium.send_trap(dict_ne_info["ne_ip"], 7070, 'xoambaseserver',dict_ne_info["ne_type"],alarm_type,host,snmp_auth_info)
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
            ne_severity = alarm_raw["alarmLevel"]
            if ne_severity:
                gui_severity = mappingInstance.convert_alarm_severity(ne_severity)
                if(gui_severity):
                    expected_alarm["告警级别"]= gui_severity
            else:
                test_logger.failed("get alarmLevel from trap Failed")
        elif(key == "告警时间"):
            ne_event_time = alarm_raw["timeStamp"]
            if ne_event_time:
                if (re.findall(r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}.\d{1}",ne_event_time)[0]!= None):
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
            if(netype == 'OCGAS'):
                gui_alarmtype_id = mappingInstance.convert_alarmtype_id(alarmtype)
            else:
                ne_specificProblem = alarm_raw["specificProblem"]
                if ne_specificProblem:
                    gui_alarmtype_id = mappingInstance.convert_alarmtype_id(ne_specificProblem)
                else:
                    test_logger.failed("get specificProblem from trap Failed.")
            if gui_alarmtype_id:
                expected_alarm["告警编号"]=gui_alarmtype_id
        elif(key == "告警名称"):
            if(netype == 'OCGAS'):
                gui_alarmtype_cn = mappingInstance.convert_alarmtype_cn(alarmtype)
            else:
                ne_specificProblem = alarm_raw["specificProblem"]
                if ne_specificProblem:
                    gui_alarmtype_cn = mappingInstance.convert_alarmtype_cn(ne_specificProblem)
                else:
                    test_logger.failed("get specificProblem from Trap Failed.")
            if gui_alarmtype_cn:
                expected_alarm["告警名称"] = gui_alarmtype_cn
        elif(key == "定位信息"):
            ne_source_info =  alarm_raw["alarmSource"]
            if ne_source_info:
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
            if (netype == 'OCGAS'):
                specific_problem = mappingInstance.convert_specific_problem(alarmtype)
            else:
                ne_specificProblem = alarm_raw["specificProblem"]
                if ne_specificProblem:
                    specific_problem = ne_specificProblem
                else:
                    test_logger.failed("get specificProblem from trap Failed")
            if specific_problem:
                expected_alarm["问题描述"] = specific_problem
        elif(key == "可能原因"):
            if(netype == 'OCGAS'):
                probable_cause = mappingInstance.convert_probable_cause(alarmtype)
            else:
                ne_probableCause = alarm_raw["probableCause"]
                if ne_probableCause:
                    probable_cause = mappingInstance.convert_probable_cause(ne_probableCause)
                else:
                    test_logger.failed("get probableCause from trap Failed")
            if probable_cause:
                expected_alarm["可能原因"] = probable_cause
        elif(key == "告警类型"):
            ne_event_type = alarm_raw["alarmCategory"]
            if ne_event_type:
                gui_event_type = mappingInstance.convert_event_type(ne_event_type)
                if gui_event_type:
                    expected_alarm["告警类型"] = gui_event_type
            else:
                test_logger.failed("get alarmCategory from trap Failed")
        elif(key == "补充信息"):
            additionInfo = alarm_raw["alarmDescription"]
            if additionInfo:
                expected_alarm["补充信息"] = additionInfo
            else:
                test_logger.failed("get alarmDescription from trap Failed")
    return expected_alarm


