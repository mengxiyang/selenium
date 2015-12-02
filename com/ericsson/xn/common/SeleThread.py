#encoding=utf-8
'''
Created on Dec 2, 2015

@author: lowitty
'''
import threading

class SeleniumThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.stopThread = False
        
    def stop(self):
        self.stopThread = True
        
    def run(self):
        while(not self.stopThread):
            pass