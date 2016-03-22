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



class notifMapping():
    def __init__(self,common_cfg,nbi_mapping_cfg):
        
        self.com_mappingInstance = alarmMapping(common_cfg)
        self.notif_mappingInstance = MappingParser(nbi_mapping_cfg)

        
        print self.com_mappingInstance.dict_mapping_info
        
    
            
    

