#encoding=utf-8
'''
Created on Dec 2, 2015

@author: lowitty
'''
import threading
from . import CommonFunc
from datetime import datetime
import time

class SeleniumThread(threading.Thread):
    
    def __init__(self,isMac, actionType, chrome, driver, host, port, username, password):
        threading.Thread.__init__(self)
        self.stopThread = False
        self.isMac = isMac
        self.actionType = actionType
        self.chrome = chrome
        self.driver = driver
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        
    def stop(self):
        self.stopThread = True
        
    def run(self):
        if(0 == self.actionType):
            btn = CommonFunc.alarmAck(self.isMac, self.chrome, self.driver, self.host, self.port, self.username, self.password)
        elif(1 == self.actionType):
            btn = CommonFunc.alarmClear(self.isMac, self.chrome, self.driver, self.host, self.port, self.username, self.password)
        elif(2 == self.actionType):
            btn = CommonFunc.alarmQuery(self.isMac, self.chrome, self.driver, self.host, self.port, self.username, self.password)
        elif(3 == self.actionType):
            btn = CommonFunc.alarmSync(self.isMac, self.chrome, self.driver, self.host, self.port, self.username, self.password)
        print "Now waiting for the last fire-up..."
        tSleep = 1.0 - datetime.now().microsecond / 1000000.0
        time.sleep(tSleep)
        while(not self.stopThread):
            tMin = datetime.now().minute
            if(0 == tMin % 5):
            #if(True):
                CommonFunc.foo(CommonFunc.clickButton, btn)
                print "5 minutes later, I will quit."
                time.sleep(60 * 5)
                self.stopThread = True
            time.sleep(0.2)
            