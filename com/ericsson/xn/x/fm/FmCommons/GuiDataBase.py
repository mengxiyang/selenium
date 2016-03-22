#-*- coding: UTF-8 -*
'''
Created on Mar 1, 2016

@author: eyyylll
'''



from com.ericsson.xn.commons import test_logger
from com.ericsson.xn.commons.PyProperties import Properties
import os
from com.ericsson.xn.commons import CommonStatic
from com.ericsson.xn.x.fm.FmCommons import FmCommon
from com.ericsson.xn.x.ne import NeCommon
from com.ericsson.xn.commons import base_clint_for_selenium
import re
import types

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

    mappingInstance = alarmMapping(alarm_mapping_cfg)

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
            FmCommon.init_and_search(driver,ne_name)
            alarm_type_list= mappingInstance.get_property("alarm_types")
            for alarm_type in alarm_type_list:
                test_logger.info("send alarm trap: " + dict_ne_info["ne_type"] + ":" + alarm_type + "...")
                alarm_from_ne = base_clint_for_selenium.send_trap(dict_ne_info["ne_ip"], 7070, 'xoambaseserver',dict_ne_info["ne_type"],alarm_type,host)
                error_code = int(alarm_from_ne["code"])
                if error_code==1:
                    alarm_trap=alarm_from_ne["trap"]
                    test_logger.info("alarm sent successfully" + str(alarm_trap))
                    alarm_expected=alarm_converter(ne_name,alarm_type,alarm_trap,mappingInstance)
                    alarm_on_gui=FmCommon.fetch_alarm_on_gui(driver,mappingInstance,alarm_type)
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
            test_logger.error(e.message)




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

            
def alarm_converter(nename,alarmtype,alarm_raw,mappingInstance):
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
                test_logger.failed("The alarm severity can't be found on Node")
        elif(key == "告警时间"):
            ne_event_time = alarm_raw["timeStamp"]
            if ne_event_time:
                if (re.findall(r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}",ne_event_time)[0]!= None):
                    expected_alarm["告警时间"] = ne_event_time + ".0"
                else:
                    test_logger.failed("Incorrect eventTime format on Node")
            else:
                test_logger.failed("The eventTime can't be found on Node")
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
            specific_problem = mappingInstance.convert_specific_problem(alarmtype)
            if specific_problem:
                expected_alarm["问题描述"] = specific_problem
        elif(key == "可能原因"):
            probable_cause = mappingInstance.convert_probable_cause(alarmtype)
            if probable_cause:
                expected_alarm["可能原因"] = probable_cause
        elif(key == "告警类型"):
            ne_event_type = alarm_raw["alarmCategory"]
            if ne_event_type:
                gui_event_type = mappingInstance.convert_event_type(ne_event_type)
                if gui_event_type:
                    expected_alarm["告警类型"] = gui_event_type
            else:
                test_logger.failed("The eventType can't be found on Node")
        elif(key == "补充信息"):
            additionInfo = alarm_raw["alarmDescription"]
            if additionInfo:
                expected_alarm["补充信息"] = additionInfo
            else:
                test_logger.failed("The additionalText can't be found on Node")
    return expected_alarm


class alarmMapping():
    def __init__(self,alarm_mapping_cfg):
        if(not os.path.exists(alarm_mapping_cfg)):
            test_logger.error("The alarm mapping cfg files: " + alarm_mapping_cfg + " not existed")

        mapping_info = Properties(alarm_mapping_cfg)
        self.dict_mapping_info = {}
        for key in mapping_info.dict_info().keys():
            self.dict_mapping_info[key] = mapping_info.getProperty(key)

    def get_property(self,key):
        if self.dict_mapping_info.has_key(key):
            if type(self.dict_mapping_info[key]) is types.DictionaryType or type(self.dict_mapping_info[key])is types.ListType:
                return self.dict_mapping_info[key]
            elif type(self.dict_mapping_info[key]) is types.StringType:
                value = []
                value.append(self.dict_mapping_info[key])
                return value
        else:
            test_logger.failed("key name: " + key + " can't be found in mapping.cfg")

    def convert_alarm_severity(self,severity):
        if self.dict_mapping_info["alarm_severity"].has_key(str(severity)):
            return self.dict_mapping_info["alarm_severity"][str(severity)]
        else:
            test_logger.failed("alarm_severity convert failed for " + str(severity))
            return None

    def convert_alarmtype_id(self,alarm_type):
        if self.dict_mapping_info["alarmtype_id"].has_key(alarm_type):
            return self.dict_mapping_info["alarmtype_id"][alarm_type]
        else:
            test_logger.failed("alarmtype_id convert failed for " + alarm_type)
            return None

    def convert_event_type(self,alarm_category):
        if self.dict_mapping_info["event_type"].has_key(str(alarm_category)):
            return self.dict_mapping_info["event_type"][str(alarm_category)]
        else:
            test_logger.failed("event_type convert failed for alarm_category:" + str(alarm_category))
            return None

    def convert_alarmtype_cn(self,alarm_type):
        if self.dict_mapping_info["alarmtype_cn"].has_key(alarm_type):
            return self.dict_mapping_info["alarmtype_cn"][alarm_type]
        else:
            test_logger.failed("alarmtype_cn convert failed for " + alarm_type)

    def convert_specific_problem(self,alarm_type):
        if self.dict_mapping_info["specific_problem"].has_key(alarm_type):
            return self.dict_mapping_info["specific_problem"][alarm_type]
        else:
            test_logger.failed("specific_problem convert failed for " + alarm_type)


    def convert_probable_cause(self,probable_cause):
        if self.dict_mapping_info["probable_cause"].has_key(probable_cause):
            return self.dict_mapping_info["probable_cause"][probable_cause]
        else:
            test_logger.failed("probable_cause convert failed for " + probable_cause)





