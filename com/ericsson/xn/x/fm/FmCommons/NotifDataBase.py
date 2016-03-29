'''
Created on Mar 22, 2016

@author: eyyylll
'''

from com.ericsson.xn.x.fm.FmCommons import MappingParser
import xml.etree.ElementTree as ET
from com.ericsson.xn.commons.PyProperties import Properties
import os
from com.ericsson.xn.commons import test_logger as test
from com.ericsson.xn.x.fm.FmCommons.GuiDataBase import alarmMapping
from com.ericsson.xn.x.fm.FmCommons.NotifFunc import compare_data
from com.ericsson.xn.x.fm.FmCommons.NotifFunc import get_nodeid_from_db

root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__))).split('com' + os.sep + 'ericsson' + os.sep + 'xn' + os.sep + 'x' + os.sep + 'fm' + os.sep + 'FmCommons')[0]
notify_mapping_cfg = root_dir + os.sep + 'x' + os.sep + 'fm' + os.sep + 'nbi_mapping' + os.sep + 'hss_new_alarm.cfg'

class notifMapping(alarmMapping):
    
    def __init__(self,nbi_mapping_cfg):
        alarmMapping.__init__(self, nbi_mapping_cfg)
        self.notify_mapping_info = self.dict_mapping_info
        
    
    def get_property(self, key):
        if self.notify_mapping_info.has_key(key):
            return self.notify_mapping_info[key]
        else:
            test.failed("get " + key + " from mapping Failed")