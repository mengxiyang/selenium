#encoding=utf-8
'''
Created on Dec 2, 2015

@author: lowitty
'''
from com.ericsson.xn.common import CommonFunc
from com.ericsson.xn.common.SeleThread import SeleniumThread
import time
if __name__ == '__main__':
    pathDriver = 'C:\Users\EJLNOQC\Desktop\chromedriver.exe'
    pathChrome = 'C:\\installed\\chrome\\chrome.exe'
    host = '10.184.73.75'
    ack = SeleniumThread(0, chrome = pathChrome, driver = pathDriver, host = host, port = 8686, username = 'admin', password = 'Admin!@#123')
    #clear = SeleniumThread(1, chrome = pathChrome, driver = pathDriver, host = host, port = 8686, username = 'admin', password = 'Admin!@#123')
    #query = SeleniumThread(2, chrome = pathChrome, driver = pathDriver, host = host, port = 8686, username = 'admin', password = 'Admin!@#123')
    #sync = SeleniumThread(3, chrome = pathChrome, driver = pathDriver, host = host, port = 8686, username = 'admin', password = 'Admin!@#123')
    
    ack.start()
    #clear.start()
    #query.start()
    #sync.start()
    ack.join()
    #clear.join()
    #query.join()
    #sync.join()
    '''driver = CommonFunc.loginToInterface(chrome = pathChrome, driver = pathDriver, host= host)
    CommonFunc.toAlarmManagement(driver)
    #2-1 ACK, 0-2 CLEAR
    tr = CommonFunc.findLineOfCertainStatus(driver, 0)
    if(tr):
        #time.sleep(1)
        #CommonFunc.clickTheCheckboxOftheTR(tr)
        #time.sleep(1)
        #btn = CommonFunc.findBtnReturnComfirmBtn(driver, 2)
        btn = CommonFunc.findBtnReturnComfirmBtn(driver, 0)
        time.sleep(1)
        CommonFunc.clickButton(btn)
    #CommonFunc.toAlarmSyncPage(driver)
    #CommonFunc.quitDriver(driver)
    pass'''