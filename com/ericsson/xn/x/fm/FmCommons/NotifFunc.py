'''
Created on Mar 24, 2016

@author: eyyylll
'''
from com.ericsson.xn.x.fm.FmCommons.NotifDataBase import notifMapping
from com.ericsson.xn.commons import test_logger as test
from com.ericsson.xn.commons.base_clint_for_selenium import send_trap
from com.ericsson.xn.commons.PyProperties import Properties
from com.ericsson.xn.x.fm.TestCases.case_ocgas_fm import server_info_cfg
from com.ericsson.xn.x.fm.FmCommons.FmCommon import data_init, query_alarm,quitDriver
from com.ericsson.xn.commons import CommonStatic
import types

root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__))).split('com' + os.sep + 'ericsson' + os.sep + 'xn' + os.sep + 'x' + os.sep + 'fm' + os.sep + 'FmCommons')[0]
notify_mapping_cfg = root_dir + os.sep + 'x' + os.sep + 'fm' + os.sep + 'nbi_mapping' + os.sep + 'hss_new_alarm.cfg'
server_info_cfg = root_dir + os.sep + 'x' + os.sep + 'pm' + os.sep + 'execute_conf.cfg'
ne_info_cfg = root_dir + os.sep + 'x' + os.sep + 'pm' + os.sep + 'nes' + 'imshss.cfg'



def compare_data(notif_ne, expected_result):
    for key,value in expected_result.item():
        if notif_ne.has_key(key):
            if type(value) is not types.DictType:
                if notif_ne[key] ==  value:
                    test.passed("NBI notification attribute " + key + " accuracy test Passed. The NBI notification value is " + notif_ne[key] + ", and the expected result is " + value)
                else:
                    test.failed("NBI notification attribute " + key + " accuracy test Failed. The NBI notification value is " + notif_ne[key] + ", and the expected result is " + value)
            else:
                expected_result = value
                notif_ne = notif_ne[key]
                compare_data(notif_ne,expected_result)
        else:
            test.failed("NBI notification attribute " + key + " accuracy test Failed for " + key + " missing in NBI notification")
            
    
    for key_n,value_n in notif_ne.item():
        if expected_result.has_key(key_n) == None:
            test.failed("NBI notification attribute " + key + " accuracy test Failed for extra attribute " + key)
            

def get_nodeid_from_db(nename):
	return '12345'
                       
    
def getNBINotification(basemgr_ip,basemgr_port,basemgr_pwd,ne_type,alarm_type,host_ip,snmp_auth_info):
	return {'error_code':'1','msg':'get nbi notification successfully','nbi':{'event_name':'x1','event_type':{'null':{'domain_name':'Alarm IRP V3.0.0','type_name':type_name}}},'trap':{'alarmCategory':'CommunicationsAlarm'}}
    

def check_attr_accuracy(mappingInstance,alarm_trap,dict_nbi_notif,nename,*attrs):
    attr_list = attrs
    for a in attrs:
        expected_value = {}
        if 'event_name' == a:
            if dict_nbi_notif.has_key('event_name'):
                notif_value = dict_nbi_notif['event_name']
                mapped_event_name = mappingInstance.convert_event_type(alarm_trap['alarmCategory'])
                expected_value['event_name'] = '"' + mapped_event_name + '"'
                compare_data(notif_value,expected_value)
            else:
                test.failed("get 'event_name' from nbi notification Failed")

        elif "event_type" == a:
            if dict_nbi_notif.has_key("event_type"):
                notif_value = dict_nbi_notif["event_type"]
                type_name = "'" + mappingInstance.notify_mapping_info["type_name"] + "'"
                expected_value = {'event_type':{'null':{'domain_name':'Alarm IRP V3.0.0','type_name':type_name}}}
                compare_data(notif_value, expected_value)
            else:
                test.failed("get 'event_type' from nbi notification Failed")

        elif 'd'  == a:
            if dict_nbi_notif.has_key("d"):
                notif_value = dict_nbi_notif["d"]
                object_class = "'" + mappingInstance.notify_mapping_info['object_class'] + "'"
                expected_value = {'d':{'value':{'CORBA::String':object_class}}}
                compare_data(notif_value, expected_value)
            else:
                test.failed("get 'd' from nbi notification Failed")

        elif "e" == a:
            if dict_nbi_notif.has_key["e"]:
                notif_value = dict_nbi_notif["e"]
                if mappingInstance.notify_mapping_info["object_class"] == 'ManagedElement':
                    nodeid = get_nodeid_from_db(nename)
                    dn = 'DC=Ericsson,SubNetwork=1,ManagedElement=' + str(nodeid) + '|' + nename
                elif mappingInstance.notify_mapping_info["object_class"] == 'ManagedNode':
                    dn = 'DC=Ericsson,SubNetwork=1,ManagedNode=1'
                expected_value = {'e':{'value':{'CORBA::String':'"' + dn + '"'}}}
                compare_data(notif_value,expected_value)

def check_notify__data_accuracy(ne_info_cfg,server_info_cfg,mapping_info_cfg):
    dict_ne_info,dict_server_info,dict_browser_chrome = data_init(ne_info_cfg,server_info_cfg)
    #driver = CommonStatic.login_rsnms(dict_browser_chrome,dict_server_info["host"],dict_server_info["username"],dict_server_info["password"],dict_server_info["port"],dict_server_info["url"])
    driver = True
    if driver:
        try:
            #NeCommon.to_ne_management_page_by_url(driver,server_info)
            #new_ne_info=NeCommon.check_and_add_ne(driver, dict_ne_info)
            #ne_name = new_ne_info["ne_name"]
            ne_name = "IMSHSS77"
            if dict_ne_info["ne_type"] == "LTEHSS" or dict_ne_info["ne_type"] == "IMSHSS":
                snmp_auth_info = []
                snmp_auth_info.append(dict_ne_info["usm_user"])
                snmp_auth_info.append(dict_ne_info["auth_password"])
                snmp_auth_info.append(dict_ne_info["priv_password"])
            else:
                snmp_auth_info = []
                
            #FmCommon.toAlarmManagement_by_url(driver,dict_server_info)
            #FmCommon.init_and_search(driver,ne_name)
            mappingInstance = notifMapping(mapping_info_cfg)
            alarm_type_list = mappingInstance.dict_mapping_info["alarm_types"]
            for alarm_type in alarm_type_list:
                test.info("send and get NBI notification: " + dict_ne_info["ne_type"] + ":" + alarm_type + "...")
                alarm_raw = getNBINotification(dict_ne_info["ne_ip"], 7070, 'xoambaseserver',dict_ne_info["ne_type"],alarm_type,dict_server_info["host"],snmp_auth_info)
                error_code = int(alarm_raw["code"])
                if error_code==1:
                    #query_alarm(driver)
                    alarm_trap = alarm_raw["trap"]
                    nbi_notif = alarm_raw["nbi"]
                    test.info("send and get NBI notification successfully.TrapInfo:" + str(alarm_trap) + " and NotifInfo:" + str(nbi_notif))
                    check_notif_items = tuple(mappingInstance.dict_mapping_info("notif_attr_names"))
                    mappingInstance.check_attr_accuracy(mappingInstance,alarm_trap,nbi_notif,ne_name,check_notif_items)
        except Exception as e:
            #quitDriver(driver)
            test.error(e.message)


if __name__ == '__main__':
    check_notify__data_accuracy(ne_info_cfg,server_info_cfg,notify_mapping_cfg)



