'''
Created on Mar 24, 2016

@author: eyyylll
'''
from com.ericsson.xn.x.fm.FmCommons import NotifDataBase
from com.ericsson.xn.commons import test_logger as test
from com.ericsson.xn.commons.base_clint_for_selenium import send_trap
from com.ericsson.xn.commons.PyProperties import Properties
from com.ericsson.xn.x.fm.TestCases.case_ocgas_fm import server_info_cfg
from com.ericsson.xn.x.fm.FmCommons.FmCommon import data_init, query_alarm,quitDriver
from com.ericsson.xn.commons import CommonStatic
from com.ericsson.xn.x.ne import  NeCommon
from com.ericsson.xn.x.fm.FmCommons import FmCommon
from libs.mysql import connector
from com.ericsson.xn.commons.caseutils import pre_test_case, post_test_case
import types,os

root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__))).split('com' + os.sep + 'ericsson' + os.sep + 'xn' + os.sep + 'x' + os.sep + 'fm' + os.sep + 'FmCommons')[0]
notify_mapping_cfg = root_dir + os.sep + 'x' + os.sep + 'fm' + os.sep + 'nbi_mapping' + os.sep + 'hss_new_alarm.cfg'
server_info_cfg = root_dir + os.sep + 'x' + os.sep + 'pm' + os.sep + 'execute_conf.cfg'
ne_info_cfg = root_dir + os.sep + 'x' + os.sep + 'pm' + os.sep + 'nes' + os.sep + 'imshss.cfg'


def compare_data(notif_ne,expected_result):
    for key,value in expected_result.items():
        if notif_ne.has_key(key):
            if type(value) is not types.DictType:
                if notif_ne[key] ==  value:
                    test.passed(key + " accuracy test Passed. The NBI notification value is " + notif_ne[key] + ", and the expected result is " + value)
                else:
                    test.failed(key + " accuracy test Failed. The NBI notification value is " + notif_ne[key] + ", and the expected result is " + value)
            else:
                expected_result = value
                notif_ne = notif_ne[key]
                compare_data(notif_ne,expected_result)
        else:
            test.failed(key + " accuracy test Failed for " + key + " missing in NBI notification")

    for key_n,value_n in notif_ne.items():
        if expected_result.has_key(key_n) == None:
            test.failed("NBI notification attribute " + key + " accuracy test Failed for extra attribute " + key)




def get_nodeid_by_nename(nename,host_ip):
    try:
        cnx = connector.connect(user='root',password='root',host=host_ip,database='xoam')
        cursor = cnx.cursor()
        query = ("SELECT nodeId from neconfig where neid in select neid from nes where nename = '%s'")
        cursor.execute(query,nename)
        node_id=[]
        for nodeId in cursor:
            node_id.append(nodeId.strim())
        cursor.close
        cnx.close
        return node_id

    except Exception as e:
        test.error(e.message)


def getNBINotification(basemgr_ip,basemgr_port,basemgr_pwd,ne_type,alarm_type,host_ip,snmp_auth_info):
	return {'code':'1','msg':'get nbi notification successfully','nbi':{'event_name':'"x2"','event_type':{'null':{'domain_name':'"Alarm IRP V3.0.0"','type_name':'"x1"'}},'d':{'value':{'CORBA::String':'"ManagedElement"'}},'e':{'value':{'CORBA::String':'"CORBA::String "DC=Ericsson,SubNetwork=1,ManagedElement=ocgas58|ocgas58"'}}},'trap':{'alarmCategory':'CommunicationsAlarm'}}
    

def check_attr_accuracy(mappingInstance,alarm_trap,dict_nbi_notif,nename,host,*attrs):
    attr_list = attrs
    for a in attrs:
        expected_value = {}
        notif_value = {}
        if 'event_name' == a:
            if dict_nbi_notif.has_key('event_name'):
                notif_value['event_name'] = dict_nbi_notif['event_name']
                mapped_event_name = mappingInstance.convert_event_type(alarm_trap['alarmCategory'])
                expected_value['event_name'] = '"' + mapped_event_name + '"'
                test.info("check 'event_name',the nbi notification result is " + str(notif_value) + ",and the expected result is " + str(expected_value))
                compare_data(notif_value,expected_value)
            else:
                test.failed("get 'event_name' from nbi notification Failed")

        elif "event_type" == a:
            if dict_nbi_notif.has_key("event_type"):
                notif_value['event_type'] = dict_nbi_notif["event_type"]
                type_name = '"' + mappingInstance.notify_mapping_info["type_name"] + '"'
                expected_value = {'event_type':{'null':{'domain_name':'"Alarm IRP V3.0.0"','type_name':type_name}}}
                test.info("check 'event_type',the nbi notification result is " + str(notif_value) + ",and the expected result is " + str(expected_value))
                compare_data(notif_value, expected_value)
            else:
                test.failed("get 'event_type' from nbi notification Failed")

        elif 'd'  == a:
            if dict_nbi_notif.has_key("d"):
                notif_value['d'] = dict_nbi_notif["d"]
                object_class = '"' + mappingInstance.notify_mapping_info['object_class'] + '"'
                expected_value = {'d':{'value':{'CORBA::String':object_class}}}
                test.info("check 'objectClass',the nbi notification result is " + str(notif_value) + ",and the expected result is " + str(expected_value))
                compare_data(notif_value, expected_value)
            else:
                test.failed("get 'd' from nbi notification Failed")

        elif "e" == a:
            if dict_nbi_notif.has_key["e"]:
                notif_value['e'] = dict_nbi_notif["e"]
                if mappingInstance.notify_mapping_info["object_class"] == 'ManagedElement':
                    nodeid = get_nodeid_by_nename(nename,host)
                    dn = 'DC=Ericsson,SubNetwork=1,ManagedElement=' + str(nodeid) + '|' + nename
                elif mappingInstance.notify_mapping_info["object_class"] == 'ManagedNode':
                    dn = 'DC=Ericsson,SubNetwork=1,ManagedNode=1'
                expected_value = {'e':{'value':{'CORBA::String':'"' + dn + '"'}}}
                test.info("check 'objectInstance',the nbi notification result is " + str(notif_value) + ",and the expected result is " + str(expected_value))
                compare_data(notif_value,expected_value)

def check_notify__data_accuracy(ne_info_cfg,server_info_cfg,mapping_info_cfg):
    dict_ne_info,dict_server_info,dict_browser_chrome = data_init(ne_info_cfg,server_info_cfg)
    server_info = Properties(server_info_cfg)
    #driver = CommonStatic.login_rsnms(dict_browser_chrome,dict_server_info["host"],dict_server_info["username"],dict_server_info["password"],dict_server_info["port"],dict_server_info["url"])
    driver = True
    if driver:
        try:
            '''
            NeCommon.to_ne_management_page_by_url(driver,server_info)
            new_ne_info=NeCommon.check_and_add_ne(driver,dict_ne_info)
            ne_name = new_ne_info["ne_name"]
            '''
            ne_name = 'IMSHSS-9A8ACC8039B1B283'
            if dict_ne_info["ne_type"] == "LTEHSS" or dict_ne_info["ne_type"] == "IMSHSS":
                snmp_auth_info = []
                snmp_auth_info.append(dict_ne_info["usm_user"])
                snmp_auth_info.append(dict_ne_info["auth_password"])
                snmp_auth_info.append(dict_ne_info["priv_password"])
            else:
                snmp_auth_info = []
            '''
            FmCommon.toAlarmManagement_by_url(driver,server_info)
            FmCommon.init_and_search(driver,ne_name)
            '''
            mappingInstance = NotifDataBase.notifMapping(mapping_info_cfg)
            alarmtypes = mappingInstance.dict_mapping_info["alarm_types"]
            alarm_type_list = []
            if type(alarmtypes) is types.StringType:
                alarm_type_list.append(alarmtypes)
            else:
                alarm_type_list = alarmtypes
            for alarm_type in alarm_type_list:
                test.info("send and get NBI notification for " + dict_ne_info["ne_type"] + ":" + alarm_type + "...")
                alarm_raw = getNBINotification(dict_ne_info["ne_ip"], 7070, 'xoambaseserver',dict_ne_info["ne_type"],alarm_type,dict_server_info["host"],snmp_auth_info)
                error_code = int(alarm_raw["code"])
                if error_code==1:
                    #query_alarm(driver)
                    alarm_trap = alarm_raw["trap"]
                    nbi_notif = alarm_raw["nbi"]
                    test.info("get TrapInfo is:" + str(alarm_trap) + " and NotifInfo is:" + str(nbi_notif))
                    test.info("start to check " + alarm_type)
                    check_notif_items = mappingInstance.get_property("notif_attr_names")
                    check_attr_accuracy(mappingInstance,alarm_trap,nbi_notif,ne_name,dict_server_info["host"],check_notif_items[3])
        except Exception as e:
            #quitDriver(driver)
            test.error(e.message)


if __name__ == '__main__':
    pre_test_case("check_hss_nbi_notif_accuracy_case","notify_accuracy")
    check_notify__data_accuracy(ne_info_cfg,server_info_cfg,notify_mapping_cfg)
    post_test_case()



