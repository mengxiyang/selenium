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

root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__))).split('com' + os.sep + 'ericsson' + os.sep + 'xn' + os.sep + 'x' + os.sep + 'fm' + os.sep + 'FmCommons')[0]
notify_mapping_cfg = root_dir + os.sep + 'x' + os.sep + 'fm' + os.sep + 'nbi_mapping' + os.sep + 'ne_new_alarm.cfg'
common_mapping_cfg = root_dir + os.sep + 'x' + os.sep + 'fm' + os.sep + 'nbi_mapping' + os.sep + 'common.cfg'

class notifMapping(alarmMapping):
    
    def __init__(self,common_cfg,nbi_mapping_cfg):  
        alarmMapping.__init__(self, common_cfg)
        m_parser = MappingParser.XMLTree(notify_mapping_cfg) 
        notif_attributes = m_parser.get_children_tags()
        for a in notif_attributes:
            notify_mapping_info = m_parser.get_element_mapping(a)
        self.notify_mapping_info = dict(self.dict_mapping_info.items() + notify_mapping_info.items())
        
    
        
    
            
if __name__ == '__main__':
    notify = notifMapping(common_mapping_cfg,notify_mapping_cfg)