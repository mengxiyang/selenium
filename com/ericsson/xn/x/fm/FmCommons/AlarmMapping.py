'''
Created on Mar 31, 2016

@author: eyyylll
'''
import os
import datetime,time
from com.ericsson.xn.commons.PyProperties import Properties
import com.ericsson.xn.commons.test_logger as test
import types

class alarmMapping():
    def __init__(self,alarm_mapping_cfg):
        if(not os.path.exists(alarm_mapping_cfg)):
            test.error("The alarm mapping cfg files: " + alarm_mapping_cfg + " not existed")

        mapping_info = Properties(alarm_mapping_cfg)
        self.dict_mapping_info = {}
        for key in mapping_info.dict_info().keys():
            self.dict_mapping_info[key] = mapping_info.getProperty(key)

    def get_property(self,key):
        if self.dict_mapping_info.has_key(key):
            if type(self.dict_mapping_info[key]) is types.DictionaryType or type(self.dict_mapping_info[key])is types.ListType:
                return self.dict_mapping_info[key]
            elif type(self.dict_mapping_info[key]) is types.StringType:
                value = []
                value.append(self.dict_mapping_info[key])
                return value
        else:
            test.failed("key name: " + key + " can't be found in mapping.cfg")

    def convert_alarm_severity(self,key):
        if self.dict_mapping_info["alarm_severity"].has_key(str(key)):
            return self.dict_mapping_info["alarm_severity"][str(key)]
        else:
            test.failed("alarm_severity convert failed for " + str(key))
            return None

    def convert_alarmtype_id(self,key):
        if self.dict_mapping_info["alarmtype_id"].has_key(key):
            return self.dict_mapping_info["alarmtype_id"][key]
        else:
            test.failed("alarmtype_id convert failed for " + key)
            return None

    def convert_event_type(self,key):
        if self.dict_mapping_info["event_type"].has_key(str(key)):
            return self.dict_mapping_info["event_type"][str(key)]
        else:
            test.failed("event_type convert failed for alarm_category:" + str(key))
            return None

    def convert_alarmtype_cn(self,key):
        if self.dict_mapping_info["alarmtype_cn"].has_key(key):
            return self.dict_mapping_info["alarmtype_cn"][key]
        else:
            test.failed("alarmtype_cn convert failed for " + key)

    def convert_specific_problem(self,key):
        if self.dict_mapping_info["specific_problem"].has_key(key):
            return self.dict_mapping_info["specific_problem"][key]
        else:
            test.failed("specific_problem convert failed for " + key)


    def convert_probable_cause(self,key):
        if self.dict_mapping_info["probable_cause"].has_key(key):
            return self.dict_mapping_info["probable_cause"][key]
        else:
            test.failed("probable_cause convert failed for " + key)
            
    def convert_object_instance(self,nodeid,nename):
        if self.dict_mapping_info["object_class"] == 'ManagedElement':
            dn = 'DC=Ericsson,SubNetwork=1,ManagedElement=' + str(nodeid) + '|' + nename
        elif self.dict_mapping_info["object_class"] == 'ManagedNode':
            dn = 'DC=Ericsson,SubNetwork=1,ManagedNode=1'
        return dn
    
    def convert_event_time(self,event_time):
        event_time = event_time + "000"
        d_event_time = datetime.datetime.strptime(event_time,"%Y-%m-%d %H:%M:%S.%f")
        t_event_time = d_event_time.timetuple()
        timestamp = time.mktime(t_event_time)
        utct_time = timestamp*10000000 + 122192928000000000
        return "%d"%utct_time
    
