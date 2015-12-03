#encoding=utf-8
'''
Created on Dec 2, 2015

@author: lowitty
'''
from com.ericsson.xn.common import CommonFunc
from com.ericsson.xn.common.SeleThread import SeleniumThread
import time
if __name__ == '__main__':
    #pathDriver = 'C:\Users\EJLNOQC\Desktop\chromedriver.exe'
    pathDriver = '/Users/lowitty/Downloads/chromedriver'
    pathChrome = 'C:\\installed\\chrome\\chrome.exe'
    host = '10.184.73.75'
    ack = SeleniumThread(True, 0, pathChrome, pathDriver, host, 8686, 'admin', 'Admin!@#123')
    clear = SeleniumThread(True, 1, chrome = pathChrome, driver = pathDriver, host = host, port = 8686, username = 'admin', password = 'Admin!@#123')
    query = SeleniumThread(True, 2, chrome = pathChrome, driver = pathDriver, host = host, port = 8686, username = 'admin', password = 'Admin!@#123')
    sync = SeleniumThread(True, 3, chrome = pathChrome, driver = pathDriver, host = host, port = 8686, username = 'admin', password = 'Admin!@#123')
    
    ack.start()
    time.sleep(1)
    clear.start()
    time.sleep(1)
    query.start()
    time.sleep(1)
    sync.start()
    ack.join()
    clear.join()
    query.join()
    sync.join()