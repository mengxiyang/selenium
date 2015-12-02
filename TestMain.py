#encoding=utf-8
'''
Created on Dec 2, 2015

@author: lowitty
'''
from com.ericsson.xn.common import CommonFunc
if __name__ == '__main__':
    pathChrome = 'C:\Users\EJLNOQC\Desktop\chromedriver.exe'
    pathDriver = 'C:\\installed\\chrome\\chrome.exe'
    host = '10.184.73.75'
    driver = CommonFunc.loginToInterface(chrome = pathChrome, driver = pathDriver, host= host)
    CommonFunc.toAlarmManagement(driver)
    CommonFunc.toAlarmSyncPage(driver)
    pass