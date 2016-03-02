'''
Created on Mar 1, 2016

@author: eyyylll
'''


from com.ericsson.xn.commons import test_logger, PyProperties
import os
from com.ericsson.xn.commons import caseutils
from com.ericsson.xn.commons import CommonStatic
from com.ericsson.xn.common import CommonFunc
from com.ericsson.xn.common.CommonFunc import toAlarmManagement


def check_alarm_data_accuracy(ne_info_cfg,server_info_cfg):
    
    server_info = PyProperties(server_info_cfg)
    
    dict_browser_chrome = {
        "browser_type": server_info.getProperty('browser_type'),
        "browser_path": server_info.getProperty('browser_path'),
        "driver_path": server_info.getProperty('driver_path')
    }
    
    host = server_info.getProperty("host")
    username = server_info.getProperty("username")
    password = server_info.getProperty("password")
    port = server_info.getProperty("port")
    url = server_info.getProperty("url")
    
    driver = CommonStatic.login_rsnms(dict_browser_chrome,username,password,port,url)
    if driver:
        try:
            toAlarmManagement(driver)
            