'''
Created on Mar 24, 2016

@author: eyyylll
'''

from com.ericsson.xn.commons import test_logger as test
from com.ericsson.xn.commons.PyProperties import Properties
from com.ericsson.xn.x.fm.FmCommons.FmCommon import data_init,query_alarm,quitDriver
from com.ericsson.xn.commons import CommonStatic
from com.ericsson.xn.x.ne import  NeCommon
from com.ericsson.xn.x.fm.FmCommons import FmCommon
from com.ericsson.xn.x.fm.FmCommons import AlarmMapping
from libs.mysql import connector
import types,os
from com.ericsson.xn.commons import PyMysql
from com.ericsson.xn.commons import base_clint_for_selenium
from selenium.common.exceptions import TimeoutException
import time

root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__))).split('com' + os.sep + 'ericsson' + os.sep + 'xn' + os.sep + 'x' + os.sep + 'fm' + os.sep + 'FmCommons')[0]
notify_mapping_cfg = root_dir + os.sep + 'x' + os.sep + 'fm' + os.sep + 'nbi_mapping' + os.sep + 'hss_new_alarm.cfg'
server_info_cfg = root_dir + os.sep + 'x' + os.sep + 'pm' + os.sep + 'execute_conf.cfg'
ne_info_cfg = root_dir + os.sep + 'x' + os.sep + 'pm' + os.sep + 'nes' + os.sep + 'ltehss.cfg'


def compare_data(notif_ne,expected_result):
    for key,value in expected_result.items():
        if notif_ne.has_key(key):
            if type(value) is not types.DictType:
                if str(notif_ne[key]) ==  str(value):
                    test.passed(key + " accuracy test Passed. The NBI value is " + notif_ne[key] + ", and the expected result is " + str(value))
                else:
                    test.failed(key + " accuracy test Failed. The NBI value is " + notif_ne[key] + ", and the expected result is " + str(value))
            else:
                expected_result = value
                notif_ne = notif_ne[key]
                compare_data(notif_ne,expected_result)
        else:
            test.failed(key + " accuracy test Failed for " + key + " missing in NBI")

    for key_n,value_n in notif_ne.items():
        if expected_result.has_key(key_n) == None:
            test.failed("NBI attribute " + key + " accuracy test Failed for extra attribute " + key)




def get_nodeid_by_nename(nename,mysqlInst):
        sql = ('SELECT nodeId from neconfig where neid in (SELECT neid from nes where nename = "%s")'%nename)
        rowcount,dataset = mysqlInst.query(sql)
        if dataset[0] == None:
            sql = ('UPDATE neconfig set nodeId = "%s" where neid in (SELECT neid from nes where nename = "%s")'%(nename,nename))
            mysqlInst.execute(sql)
            nodeId=nename
        else:
            nodeId = dataset[0]
        return nodeId

def check_unique_id(sqltext,mysqlnst):
    rowcount,dataset = mysqlnst.query(sqltext,'all')
    return rowcount

def getNBINotification(basemgr_ip,basemgr_port,basemgr_pwd,ne_type,alarm_type,host_ip,snmp_auth_info):
    return {'msg': 'SUCCESS', 'nbi': {'event_type': {'none': {u'type_name': u'"x1"', u'domain_name': u'"Alarm IRP V3.0.0"'}}, 'event_name': u'"x2"', 'jj': {'value': {u'CORBA::String': u'"1||SW fault detected"'}}, 'ai_at': {'value': {u'CORBA::String': u'"x2"'}}, 'a': {'value': {u'CORBA::LongLong': u'1459411325921100000'}}, 'c': {'value': {u'CORBA::String': u'"DC=Ericsson,SubNetwork=1,ManagementNode=1,IRPAgent=1"'}}, 'b': {'value': {'Security::UtcT': {'none': {u'inacclo': u'0', u'tdf': u'480', u'inacchi': u'0', u'time': u'136756781410000000'}}}}, 'e': {'value': {u'CORBA::String': u'"DC=Ericsson,SubNetwork=1,ManagedElement=1|HSS"'}}, 'd': {'value': {u'CORBA::String': u'"ManagedElement"'}}, 'g': {'value': {u'CORBA::Short': u'348'}}, 'f': {'value': {u'CORBA::String': u'"4"'}}, 'i': {'value': {u'CORBA::String': u'"SW fault detected"'}}, 'h': {'value': {u'CORBA::Short': u'1'}}, 'j': {'value': {u'CORBA::String': u'"ALL"'}}, 'ai_ps': {'value': {u'CORBA::String': u'"1"'}}, 'q': {'value': {u'CORBA::String': u'"NULL"'}}, 'p': {'value': {u'CORBA::Boolean': u'false'}}, 's': {'value': {u'AlarmIRPConstDefs::TrendIndication': u'NO_CHANGE'}}, 'ai_vs_threshold': {'value': {u'CORBA::String': u'""'}}, 't': {'value': {'AlarmIRPConstDefs::AttributeChangeSet': {'none': {'none': {'old_value': {u'CORBA::String': u'""'}, u'attribute_name': u'""', 'new_value': {u'CORBA::String': u'""'}}}}}}, 'w': {'value': {'AlarmIRPConstDefs::CorrelatedNotification': {'none': {u'source': u'"DC=Ericsson,SubNetwork=1,ManagedElement=1|HSS"', 'notif_id_set': {'none': u'2147483647'}}}}}, 'v': {'value': {u'CORBA::String': u'""'}}}, 'code': 1, 'trap': {'probableCause': 'Software Program Error', 'timeStamp': '2016-03-31 16:50:38', 'alarmDescription': 'ALL', 'seqNo': '1.3.6.1.4.1.193.114.3.1.1', 'specificProblem': 'SW fault detected', 'alarmSource': 'Database', 'alarmLevel': 'Indeterminate', 'alarmCategory': 'Processing Error Alarm'}}

def check_common_accuracy(attr_name,dict_nbi_info,expected_value):
    nbi_value = {}
    if dict_nbi_info.has_key(attr_name):
        nbi_value[attr_name] = dict_nbi_info[attr_name]
        test.info("check '" + attr_name + "',the nbi data result is " + str(nbi_value) + ",and the expected result is " + str(expected_value))
        compare_data(nbi_value, expected_value)
    else:
        test.failed("get '" + attr_name + "' from NBI Failed")


def check_attr_accuracy(mappingInstance,alarm_trap,dict_nbi_info,nename,netype,alarmtype,nodeid,attrs,server_info):
    for a in attrs:
        expected_value = {}
        nbi_value = {}
        if 'event_name' == a:
            if dict_nbi_info.has_key('event_name'):
                nbi_value['event_name'] = dict_nbi_info['event_name']
                mapped_event_name = mappingInstance.convert_event_type(alarm_trap['alarmCategory'])
                if mapped_event_name != None:
                    expected_value['event_name'] = '"' + mapped_event_name + '"'
                    test.info("check 'event_name',the nbi data result is " + str(nbi_value) + ",and the expected result is " + str(expected_value))
                    compare_data(nbi_value,expected_value)
            else:
                test.failed("get 'event_name' from Base Server Failed")

        elif "event_type" == a:
            if dict_nbi_info.has_key("event_type"):
                nbi_value['event_type'] = dict_nbi_info["event_type"]
                type_name = '"' + mappingInstance.dict_mapping_info["type_name"] + '"'
                expected_value = {'event_type':{'none':{'domain_name':'"Alarm IRP V3.0.0"','type_name':type_name}}}
                test.info("check 'event_type',the nbi data result is " + str(nbi_value) + ",and the expected result is " + str(expected_value))
                compare_data(nbi_value, expected_value)
            else:
                test.failed("get 'event_type' from Base Server Failed")

        elif 'd'  == a:
            if dict_nbi_info.has_key("d"):
                nbi_value['d'] = dict_nbi_info["d"]
                object_class = '"' + mappingInstance.dict_mapping_info['object_class'] + '"'
                expected_value = {'d':{'value':{'CORBA::String':object_class}}}
                test.info("check 'objectClass',the nbi data result is " + str(nbi_value) + ",and the expected result is " + str(expected_value))
                compare_data(nbi_value, expected_value)
            else:
                test.failed("get 'd' from Base Server Failed")

        elif "e" == a:
            if dict_nbi_info.has_key("e"):
                nbi_value['e'] = dict_nbi_info["e"]
                dn = mappingInstance.convert_object_instance(nodeid,nename)
                if dn != None:
                    expected_value = {'e':{'value':{'CORBA::String':'"' + dn + '"'}}}
                    test.info("check 'objectInstance',the nbi result is " + str(nbi_value) + ",and the expected result is " + str(expected_value))
                    compare_data(nbi_value,expected_value)
            else:
                test.failed("get 'e' from nbi Failed")
            
        elif "b" == a:
            if dict_nbi_info.has_key("b"):
                nbi_value["b"] = dict_nbi_info["b"]
                mapped_event_time = mappingInstance.convert_event_time(alarm_trap["timeStamp"])
                if mapped_event_time!= None:
                    expected_value = {'b':{'value':{'TimeBase::UtcT':{'none':{'time':mapped_event_time,'inacclo':'0','inacchi':'0','tdf':'480'}}}}}
                    test.info("check 'eventTime',the nbi result is " + str(nbi_value) + ",and the expected result is " + str(expected_value))
                    compare_data(nbi_value, expected_value)
            else:
                test.failed("get 'b' from Base Server Failed")
           
        elif "c" == a:
            expected_value = {'c':{'value':{'CORBA::String':'"DC=Ericsson,SubNetwork=1,ManagementNode=1,IRPAgent=1"'}}}
            check_common_accuracy('c', dict_nbi_info, expected_value)
        
        elif "jj" == a:
            if dict_nbi_info.has_key("jj"):
                nbi_value["jj"] = dict_nbi_info["jj"]
                if netype in ("OCGAS","GMLC"):
                    specific_problem = mappingInstance.convert_specific_problem(alarmtype)
                else:
                    specific_problem = alarm_trap["specificProblem"]                
                
                alarmtypeid = mappingInstance.convert_alarmtype_id(alarmtype)
                
                if alarmtypeid != None and specific_problem != None:
                    mapped_vender_specificAlarmType = '"' + alarmtypeid + "||" + specific_problem + '"'
                    expected_value = {'jj':{'value':{'CORBA::String':mapped_vender_specificAlarmType}}}
                    test.info("check 'vendorSpecificAlarmType',the nbi data result is " + str(nbi_value) + ",and the expected result is " + str(expected_value))
                    compare_data(nbi_value,expected_value)
            else:
                test.failed("get 'jj' from Base Server Failed")
                
        elif "g" == a:
            if dict_nbi_info.has_key("g"):
                nbi_value["g"] = dict_nbi_info["g"]
                if alarm_trap.has_key("probableCause"):
                    mapped_probable_cause = mappingInstance.convert_probable_cause(alarm_trap["probableCause"])
                else:
                    test.failed("get 'g' from NBI Failed")
                if mapped_probable_cause != None:
                    expected_value = {'g':{'value':{'CORBA::Short':mapped_probable_cause}}}
                    test.info("check 'probableCause',the nbi data result is " + str(nbi_value) + ",and the expected result is " + str(expected_value))
                    compare_data(nbi_value, expected_value)
            else:
                test.failed("get 'g' from Base Server Failed")
        
        elif "h" == a:
            if dict_nbi_info.has_key("h"):
                nbi_value['h'] = dict_nbi_info['h']
                mapped_alarm_severity = mappingInstance.convert_alarm_severity(alarm_trap["alarmLevel"])
                if mapped_alarm_severity != None:
                    expected_value = {'h':{'value':{'CORBA::Short':mapped_alarm_severity}}}
                    test.info("check 'perceivedSeverity',the nbi data result is " + str(nbi_value) + ",and the expected result is " + str(expected_value))
                    compare_data(nbi_value, expected_value)
            else:
                test.failed("get 'h' from Base Server Failed")
                
        elif "a" == a:
            if dict_nbi_info.has_key("a"):
                nbi_value["a"] = dict_nbi_info["a"]
                '''X use CORBA:LongLong although CORBA::Long is required in spec'''
                notif_id = dict_nbi_info["a"]["value"]["CORBA::LongLong"]
                test.info("check 'notificationId',the nbi data result is " + str(nbi_value) )
                #sqltext = ('SELECT notificationId from alarms where notificationId = "%s"'%notif_id)
                #is_unique=check_unique_id(sqltext,mysqlInst)
                is_unique = base_clint_for_selenium.is_notification_id_unic(server_info["host"],7070,'xoambaseserver',notif_id)
                if is_unique == 0:
                    test.failed("the notificationId of " + notif_id + " not existed in database")
                elif is_unique == 1:
                    test.passed("the notificationId of " + notif_id + " is unique in database")
                elif is_unique > 1:
                    test.failed("more than one notificationId of " + notif_id + "found in database")
            else:
                test.failed("get 'a' from Base Server Failed")
        
        elif "w" == a:
            if dict_nbi_info.has_key("w"):
                nbi_value["w"] = dict_nbi_info["w"]
                dn = '"' + mappingInstance.convert_object_instance(nodeid,nename) + '"'
                if dn != None:
                    notification_id = dict_nbi_info["a"]["value"]["CORBA::LongLong"]
                    expected_value = {'w':{'value':{'AlarmIRPConstDefs::CorrelatedNotification':{'none':{'source':dn,'notif_id_set':{'none':notification_id}}}}}}
                    test.info("check 'correlatedNotifications',the nbi data result is " + str(nbi_value) + ",and the expected result is " + str(expected_value))
                    compare_data(nbi_value, expected_value)
            else:
                test.failed("get 'w' from Base Server Failed")
                
        elif "p" == a:
            expected_value = {'p':{'value':{'CORBA::Boolean':'FALSE'}}}
            check_common_accuracy('p',dict_nbi_info,expected_value)
            
        elif "q"  == a:
            expected_value = {'q':{'value':{'CORBA::String':'"NULL"'}}}
            check_common_accuracy('q', dict_nbi_info, expected_value)
            
        elif "s" == a:
            expected_value = {'s':{'value':{'AlarmIRPConstDefs::TrendIndication':'NO_CHANGE'}}}
            check_common_accuracy('s', dict_nbi_info, expected_value)
            
        elif "v" == a:
            expected_value = {'v':{'value':{'CORBA::String':'""'}}}
            check_common_accuracy('v', dict_nbi_info, expected_value)
            
        elif "j" == a:
            if dict_nbi_info.has_key("j"):
                nbi_value ["j"] = dict_nbi_info["j"]
                additionaltext = '"' + alarm_trap["alarmDescription"] + '"'
                expected_value = {'j':{'value':{'CORBA::String':additionaltext}}}
                test.info("check 'additionalText',the nbi data result is " + str(nbi_value) + ",and the expected result is " + str(expected_value))
                compare_data(nbi_value, expected_value)
            else:
                test.failed("get 'j' from Base Server Failed")
        
        elif "ai_vs_threshold" == a:
            expected_value = {'ai_vs_threshold':{'value':{'CORBA::String':'""'}}}
            check_common_accuracy('ai_vs_threshold', dict_nbi_info, expected_value)
        
        elif "ai_ps" == a:
            if dict_nbi_info.has_key("ai_ps"):
                nbi_value["ai_ps"] = dict_nbi_info["ai_ps"]
                mapped_alarm_severity = '"' + mappingInstance.convert_alarm_severity(alarm_trap["alarmLevel"]) + '"'
                if mapped_alarm_severity != None:
                    expected_value = {'ai_ps':{'value':{'CORBA::String':mapped_alarm_severity}}}
                    test.info("check 'AI_VS_PERCEIVED_SEVERITY',the nbi data result is " + str(nbi_value) + ",and the expected result is " + str(expected_value))
                    compare_data(nbi_value, expected_value)
            else:
                test.failed("get 'ai_ps' from Base Server Failed")
                
        elif "ai_at" == a:
            if dict_nbi_info.has_key('ai_at'):
                nbi_value['ai_at'] = dict_nbi_info['ai_at']
                mapped_event_name = '"' + mappingInstance.convert_event_type(alarm_trap['alarmCategory']) + '"'
                if mapped_event_name != None:
                    expected_value['ai_at'] = expected_value = {'ai_at':{'value':{'CORBA::String':mapped_event_name}}}
                    test.info("check 'AI_VS_ALARM_TYPE',the nbi data result is " + str(nbi_value) + ",and the expected result is " + str(expected_value))
                    compare_data(nbi_value,expected_value)
            else:
                test.failed("get 'ai_at' from Base Server Failed")
                
        elif "f"  == a:
            if dict_nbi_info.has_key("f"):
                nbi_value["f"] = dict_nbi_info["f"]
                alarm_id = dict_nbi_info["f"]["value"]["CORBA::String"].replace('"','')
                #sqltext = ("SELECT id from alarms where id = %s"%alarm_id)
                #is_unique=check_unique_id(sqltext,mysqlInst)
                is_unique = base_clint_for_selenium.is_alarm_id_unic(server_info["host"],7070,'xoambaseserver',alarm_id)
                if is_unique == 0:
                    test.failed("alarmId of " + alarm_id + " not existed in database")
                elif is_unique == 1:
                    test.passed("the alarmId of " + alarm_id + " is unique in database")
                elif is_unique > 1:
                    test.failed("more than one alarmId of " + alarm_id + "found in database")
            else:
                test.failed("get 'f' from Base Server Failed")
        
        elif "kk" == a:
            if dict_nbi_info.has_key("kk"):
                nbi_value["kk"] = dict_nbi_info["kk"]
                mapped_event_time = mappingInstance.convert_event_time(alarm_trap["timeStamp"])
                if mapped_event_time!= None:
                    expected_value = {'kk':{'value':{'TimeBase::UtcT':{'none':{'time':mapped_event_time,'inacclo':'0','inacchi':'0','tdf':'480'}}}}}
                    test.info("check 'alarm raised time',the nbi data result is " + str(nbi_value) + ",and the expected result is " + str(expected_value))
                    compare_data(nbi_value, expected_value)
            else:
                test.failed("get 'kk' from Base Server Failed")
                
        elif "i" == a:
            if netype in ('OCGAS','GMLC'):
                mapped_specific_problem = mappingInstance.convert_specific_problem(alarmtype)
            else:
                if alarm_trap.has_key("specificProblem"):
                    mapped_specific_problem = alarm_trap["specificProblem"]
                else:
                    test.failed("get specificProblem from trap Failed")
            if mapped_specific_problem != None:
                expected_value = {'i':{'value':{'CORBA::String':'"' + mapped_specific_problem + '"'}}}
                check_common_accuracy('i', dict_nbi_info, expected_value)
        
        elif "n" == a:
            expected_value = {'n':{'value':{'CORBA::Short':2}}}
            check_common_accuracy('n', dict_nbi_info, expected_value)
        
        elif "y" == a:
            expected_value = {'y':{'value':{'CORBA::String':'"AUTO"'}}}
            check_common_accuracy('y', dict_nbi_info, expected_value)
            
        elif "z" == a:
            expected_value = {'z':{'value':{'CORBA::String':'"' + nename + '"'}}}
            check_common_accuracy('z', dict_nbi_info, expected_value)
            
        elif "ll" == a:
            if dict_nbi_info.has_key("ll"):
                nbi_value["ll"] = dict_nbi_info["ll"]
                if alarm_trap.has_key("clearTime"):
                    mapped_event_time = mappingInstance.convert_event_time(alarm_trap["clearTime"])
                    if mapped_event_time!= None:
                        expected_value = {'ll':{'value':{'TimeBase::UtcT':{'none':{'time':mapped_event_time,'inacclo':'0','inacchi':'0','tdf':'480'}}}}}
                        test.info("check 'clearTime',the nbi result is " + str(nbi_value) + ",and the expected result is " + str(expected_value))
                        compare_data(nbi_value, expected_value)
                else:
                    test.info("get 'clearTime' from sourceTrap Failed")
            else:
                test.failed("get 'll' from Base Server Failed")
        
        elif "mm" == a:
            if dict_nbi_info.has_key("mm"):
                nbi_value["mm"] = dict_nbi_info["mm"]
                if alarm_trap.has_key("changeTime"):
                    mapped_event_time = mappingInstance.convert_event_time(alarm_trap["changeTime"])
                    if mapped_event_time!= None:
                        expected_value = {'mm':{'value':{'TimeBase::UtcT':{'none':{'time':mapped_event_time,'inacclo':'0','inacchi':'0','tdf':'480'}}}}}
                        test.info("check 'changeTime',the nbi result is " + str(nbi_value) + ",and the expected result is " + str(expected_value))
                        compare_data(nbi_value, expected_value)
                else:
                    test.info("get 'changeTime' from source trap Failed")
            else:
                test.failed("get 'mm' from Base Server Failed")

        elif "t" == a:
            expected_value = {'t':{'value':{'AlarmIRPConstDefs::AttributeChangeSet':{'none':{'none':{'attribute_name':'""','old_value':{'CORBA::String':'""'},'new_value':{'CORBA::String':'""'}}}}}}}
            check_common_accuracy('t',dict_nbi_info,expected_value)
                 
def check_notify_accuracy(ne_info_cfg,server_info_cfg,mapping_info_cfg):
    dict_ne_info,dict_server_info,dict_browser_chrome = data_init(ne_info_cfg,server_info_cfg)
    server_info = Properties(server_info_cfg)
    driver = CommonStatic.login_rsnms(dict_browser_chrome,dict_server_info["host"],dict_server_info["username"],dict_server_info["password"],dict_server_info["port"],dict_server_info["url"])
    if driver:
        try:
            NeCommon.to_ne_management_page_by_url(driver,server_info)
            new_ne_info=NeCommon.check_and_add_ne(driver,dict_ne_info)
            ne_name = new_ne_info["ne_name"]
            #ne_name = 'IMSHSS-9A8ACC8039B1B283'
            quitDriver(driver)

            mappingInstance = AlarmMapping.alarmMapping(mapping_info_cfg)
            #nodeid = get_nodeid_by_nename(ne_name,mysqlInst)

            nodeid = base_clint_for_selenium.get_nodeid_by_nename(dict_server_info["host"],7070,'xoambaseserver',ne_name)
            time.sleep(30)
            if nodeid == False:
                test.error("update nodeid Failure")
                
            if dict_ne_info["ne_type"] in ("IMSHSS","LTEHSS","MSC","HLR","GGSN","SGSN"):
                snmp_auth_info = []
                snmp_auth_info.append(dict_ne_info["usm_user"])
                snmp_auth_info.append(dict_ne_info["auth_password"])
                snmp_auth_info.append(dict_ne_info["priv_password"])
            else:
                snmp_auth_info = None

            alarmtypes = mappingInstance.dict_mapping_info["alarm_types"]
            alarm_type_list = []
            if type(alarmtypes) is types.StringType:
                alarm_type_list.append(alarmtypes)
            else:
                alarm_type_list = alarmtypes

            for alarm_type in alarm_type_list:
                test.info("send and get NBI data for " + dict_ne_info["ne_type"] + ":" + alarm_type + "...")
                #alarm_raw = getNBINotification(dict_ne_info["ne_ip"], 7070, 'xoambaseserver',dict_ne_info["ne_type"],alarm_type,dict_server_info["host"],snmp_auth_info)
                alarm_raw = base_clint_for_selenium.get_notification_trap(dict_ne_info["ne_ip"],7070,'xoambaseserver',dict_ne_info["ne_type"],alarm_type,dict_server_info["host"],snmp_auth_info,ne_name,nodeid)
                error_code = int(alarm_raw["code"])
                if error_code==1:
                    alarm_trap = alarm_raw["trap"]
                    nbi_notif = alarm_raw["nbi"]
                    test.info("get TrapInfo is:" + str(alarm_trap) + " and NotifInfo is:" + str(nbi_notif))
                    test.info("start to check " + alarm_type)
                    check_notif_items = mappingInstance.get_property("notif_attr_names")
                    attr_list = mappingInstance.dict_mapping_info["alarm_types"]
                    alarm_type_list = []
                    if type(check_notif_items) is types.StringType:
                        attr_list.append(check_notif_items)
                    else:
                        attr_list = check_notif_items
                    check_attr_accuracy(mappingInstance,alarm_trap,nbi_notif,ne_name,dict_ne_info["ne_type"],alarm_type,nodeid,attr_list,dict_server_info)
                else:
                    test.failed(dict_ne_info["ne_type"] + ":" + alarm_type + " accuracy test failed, reason:sending alarm trap failed, the error msg is:" + alarm_raw["msg"])

        except TimeoutException:
            test.error("find widget timeout")
        except Exception as e:
            test.error(str(e))

