# encoding=utf-8
'''
Created on Dec 3, 2015

@author: lowitty
'''
from logging.handlers import RotatingFileHandler
import logging, os
from com.ericsson.xn.common.PyProperties import Properties

logmain = logging.getLogger('selenium')
rootPath = os.path.dirname(os.path.abspath(__file__))
logConf = Properties(rootPath + os.path.sep + 'conf' + os.path.sep + 'logs.conf')
logPath = os.path.normpath(rootPath + os.path.sep + 'logs')
if not os.path.isdir(logPath):
    os.makedirs(logPath)
logFile = os.path.normpath(logPath + os.path.sep + logConf.getProperty('logFileName').strip())
logLevel = int(logConf.getProperty('logLevel'))
logFormatter = logging.Formatter('%(asctime)s [%(levelname)s] %(module)s %(funcName)s(%(lineno)d) %(message)s')
logFileHandler = RotatingFileHandler(logFile, mode='a', maxBytes=1024 * 1024 * int(logConf.getProperty('logMaxSize')),
                                     backupCount=10, encoding='utf-8', delay=0)
logFileHandler.setFormatter(logFormatter)
logFileHandler.setLevel(logLevel)

logmain.setLevel(20)
logmain.addHandler(logFileHandler)
if 'YES' == str(logConf.getProperty('consoleLog')).upper():
    logConsoleHandler = logging.StreamHandler()
    logConsoleHandler.setFormatter(logFormatter)
    logConsoleHandler.setLevel(10)
    logmain.addHandler(logConsoleHandler)
logmain.info('##########################################################################')
logmain.info('####                                                                  ####')
logmain.info('####                 Started, logger initialized.                     ####')
logmain.info('####                                                                  ####')
logmain.info('##########################################################################')

from com.ericsson.xn.x.fm import fm_ack

if __name__ == '__main__':
    fm_ack.alarm_ack(rootPath)
