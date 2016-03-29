'''
Created on Mar 22, 2016

@author: eyyylll
'''

import os
from com.ericsson.xn.commons import test_logger as test
from com.ericsson.xn.x.fm.FmCommons.GuiDataBase import alarmMapping

class notifMapping(alarmMapping):
    
    def __init__(self,nbi_mapping_cfg):
        alarmMapping.__init__(self, nbi_mapping_cfg)
        self.notify_mapping_info = self.dict_mapping_info
        
    
    def get_property(self, key):
        if self.notify_mapping_info.has_key(key):
            return self.notify_mapping_info[key]
        else:
            test.failed("get " + key + " from mapping Failed")






















