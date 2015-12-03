#encoding=utf-8
'''
Created on Dec 3, 2015

@author: lowitty
'''
import logging, os
logAlarmAck = logging.getLogger('selenium.alarmack')
from com.ericsson.xn.common import CommonFunc
def alarm_ack(rootPath):
    logAlarmAck.info('Start to perform alarm ack...')
    pathDriver = '/Users/lowitty/Downloads/chromedriver'
    pathChrome = 'C:\\installed\\chrome\\chrome.exe'
    host = '10.184.73.75'
    driver = CommonFunc.loginToInterface(True, pathChrome, pathDriver, host, 8686, 'admin', 'Admin!@#123')
    if(driver):
        CommonFunc.toAlarmManagement(driver)
        CommonFunc.queryUnAcked(driver)
        tr = CommonFunc.findLineOfCertainStatus(driver, 2)
        if(tr):
            CommonFunc.clickTheCheckboxOftheTR(tr)
            btn = CommonFunc.findBtnReturnComfirmBtn(driver, 1)
            CommonFunc.clickButton(btn)
            CommonFunc.checkAcked(tr, None, driver, os.path.normpath(rootPath + os.path.sep + 'snaps' + os.path.sep + 'ack.png'))
    pass