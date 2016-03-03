'''
Created on Mar 1, 2016

@author: eyyylll
'''


from com.ericsson.xn.commons import test_logger, PyProperties
import os
from com.ericsson.xn.commons import caseutils
from com.ericsson.xn.commons import CommonStatic
from com.ericsson.xn.x.fm.FmCommons import FmCommon
from com.ericsson.xn.common.CommonFunc import toAlarmManagement
from com.ericsson.xn.x.ne import NeCommon


def check_alarm_data_accuracy(ne_info_cfg,server_info_cfg):
    
    server_info = PyProperties(server_info_cfg)   
    dict_browser_chrome = {
        "browser_type": server_info.getProperty('browser_type'),
        "browser_path": server_info.getProperty('browser_path'),
        "driver_path": server_info.getProperty('driver_path')
    }
    
    ne_info = PyProperties(ne_info_cfg)
    dict_ne_info  = {
        "ne_name": ne_info.getProperty("ne_name"),
        "ne_type": ne_info.getProperty("ne_type"),
        "ne_ip" : ne_info.getProperty("ne_ip"),
        "ne_password" : ne_info.getProperty("ne_password"),
        "pm_path": ne_info.getProperty("pm_path"),
        "log_path": ne_info.getProperty("log_path"),
        "alarm_path": ne_info.getProperty("alarm_path"),
        "ne_port": ne_info.getProperty("ne_port"),
        "sftp_port": ne_info.getProperty("sftp_port"),
        "tab_pre": ne_info.getProperty("tab_pre")
    }
    
    host = server_info.getProperty("host")
    username = server_info.getProperty("username")
    password = server_info.getProperty("password")
    port = server_info.getProperty("port")
    url = server_info.getProperty("url")
    
    driver = CommonStatic.login_rsnms(dict_browser_chrome,username,password,port,url)
    if driver:
        try:
            NeCommon.to_ne_management_page_by_url(driver,server_info)
            new_dict_new_info=NeCommon.check_and_add_ne(driver, dict_ne_info)
            FmCommon.toAlarmManagement(driver,server_info)
            FmCommon.init_and_search(driver,new_dict_new_info["ne_name"])
            FmCommon.quitDriver(driver)
   
        except Exception as e:
            test_logger.error(e.msg)
            FmCommon.quitDriver(driver)


            
