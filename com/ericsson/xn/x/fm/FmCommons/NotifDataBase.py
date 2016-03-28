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
        
    
    def get_property(self, key):
        if self.notify_mapping_info.has_key(key):
            return self.notify_mapping_info[key]
        else:
            test.failed("get " + key + " from mapping Failed")
                
    
    def check_attr_accuacy(self,alarm_trap,dict_nbi_notif,nename,*attrs):
        attr_list = attrs
        for a in attrs:
            expected_value = {}
            if 'event_name' == a:    
                if dict_nbi_notif.has_key('event_name'):
                    notif_value = dict_nbi_notif['event_name']
                    mapped_event_name = self.convert_event_type(alarm_trap['alarmLevel'])
                    expected_value['event_name'] = '"' + mapped_event_name + '"'
                    compare_data(notif_value,expected_value)
                else:
                    test.failed("get 'event_name' from nbi notification Failed")
                
            elif "event_type" == a:
                if dict_nbi_notif.has_key("event_type"):
                    notif_value = dict_nbi_notif["event_type"]
                    expected_value = {'event_type':{'null':{'domain_name':'Alarm IRP V3.0.0','type_name':'x1'}}}
                    compare_data(notif_value, expected_value)
                else:
                    test.failed("get 'event_type' from nbi notification Failed")
            
            elif 'd'  == a:
                if dict_nbi_notif.has_key("d"):
                    notif_value = dict_nbi_notif["d"]
                    expected_value = {'d':{'value':{'CORBA::String':'"ManagementNode"'}}}
                    compare_data(notif_value, expected_value)
                else:
                    test.failed("get 'd' from nbi notification Failed")
                    
            elif "e" == a:
                if dict_nbi_notif.has_key["e"]:
                    notif_value = dict_nbi_notif["e"]
                    if self.dict_mapping_info["object_class"] == 'ManagedElement':
                        nodeid = get_nodeid_from_db(nename)
                        dn = 'DC=Ericsson,SubNetwork=1,ManagedElement=' + nodeid + '|' + nename
                        expected_value = {'e':{'value':{'CORBA::String':'"' + dn + '"'}}
                
                    
        
    
            
if __name__ == '__main__':
    notify = notifMapping(common_mapping_cfg,notify_mapping_cfg)