#! /usr/bin/python
# -*- coding: utf-8 -*-
# from datetime import datetime
from multiprocessing.managers import BaseManager

BaseManager.register('platform_info')


def platform_info(ip, port, passwd):
    mgr = start_session(ip, port, passwd)
    return mgr.platform_info()._getvalue()


BaseManager.register('server_time')


def server_time(ip, port, passwd):
    mgr = start_session(ip, port, passwd)
    return mgr.server_time()._getvalue()


BaseManager.register('send_trap')


def send_trap(ip, port, passwd, ne_type, alarm, target_ip,auth_info=None,engine_id=None,trap_port=None,client_ip=None):
    mgr = start_session(ip, port, passwd)
    return mgr.send_trap(ne_type, alarm, target_ip,auth_info,engine_id,trap_port,client_ip)._getvalue()


BaseManager.register('send_trap_nbi')


def send_trap_nbi(ip, port, passwd, ne_type, alarm, host,
                  auth_info=None, nbi_raw='/opt/LINBI/TestTool_CMCC_N13A/bin/raw_catch.log', t_port=None):
    mgr = start_session(ip, port, passwd)
    return mgr.send_trap_nbi(ne_type, alarm, host, auth_info, nbi_raw, t_port)._getvalue()


BaseManager.register('get_nodeid_by_nename')


def get_nodeid_by_nename(ip, port, password, ne_name):
    mgr = start_session(ip, port, password)
    return mgr.get_nodeid_by_nename(ne_name)._getvalue()


BaseManager.register('is_alarm_id_unic')


def is_alarm_id_unic(ip, port, password, id):
    mgr = start_session(ip, port, password)
    return mgr.is_alarm_id_unic(id)._getvalue()


BaseManager.register('is_notification_id_unic')


def is_notification_id_unic(ip, port, password, id):
    mgr = start_session(ip, port, password)
    return mgr.is_notification_id_unic(id)._getvalue()


def start_session(ip, port, passwd):
    mgr = BaseManager(address=(ip, port), authkey=passwd)
    mgr.connect()
    return mgr


def get_notification_trap(ip, b_port, passwd, ne_type, alarm, host, auth_info=None, ne_name=None, node_id=None, engine_id=None,port=11162,client_ip=None):
    mgr = start_session(ip, b_port, passwd)
    return mgr.get_notification_trap(ne_type, alarm, host, auth_info, ne_name, node_id, engine_id, port,client_ip)._getvalue()

BaseManager.register('get_notification_trap')


def close_session(mgr):
    pass


BaseManager.register('get_alarm_list_trap')


def get_alarm_list_trap(ip, port, passwd, ne_type, alarm, host, auth_info=None, ne_name=None, engine_id=None,n_port = 11162,client_ip=None):
    mgr = start_session(ip, port, passwd)
    return mgr.get_alarm_list_trap(ne_type, alarm, host, auth_info, ne_name, engine_id, n_port,client_ip)._getvalue()


# print datetime.now().strftime('%H:%M:%S:%f')
#print send_trap('10.184.74.67', 7070,'xoambaseserver', 'OCGAS', 'monitorTargetsExceedThreshold', '10.184.74.68', [])
# print datetime.now().strftime('%H:%M:%S:%f')
#print send_trap('10.184.73.102', 7070, 'xoambaseserver', 'IMSHSS', 'COMMUNICATIONFAULT_NEW', '10.184.73.77', auth_info=['privUser1', 'authUser1', 'privUser1'], engine_id='8000000001020302',client_ip='10.184.73.102')
#print send_trap('10.184.73.108', 7070, 'xoambaseserver', 'OCGAS', 'monitorTargetsExceedThreshold_NEW', '10.184.73.77',auth_info=None,engine_id=None,client_ip='10.184.73.108')
'''
from datetime import datetime
print datetime.now().strftime('%H:%M:%S:%f')
print send_trap_nbi('10.184.74.68', 7070, 'xoambaseserver', 'LTEHSS', 'COMMUNICATIONFAULT_NEW', '10.184.74.68', ['privUser1', 'authUser1', 'privUser1'], LTEHSS)
print datetime.now().strftime('%H:%M:%S:%f')
'''

#print get_nodeid_by_nename('10.184.73.77', 7070, 'xoambaseserver','MSC-1238BE4F3473717C')
#print get_alarm_list_trap('10.184.73.102', 7070, 'xoambaseserver', 'IMSHSS', 'COMMUNICATIONFAULT_NEW', '10.184.73.77', ['privUser1', 'authUser1', 'privUser1'], "IMSHSS-D5A3FFB4203B3C83",'8000000001020302','10.184.73.102')
#print get_notification_trap('10.184.73.102', 7070, 'xoambaseserver', 'IMSHSS', 'COMMUNICATIONFAULT_NEW', '10.184.73.77', ['privUser1', 'authUser1', 'privUser1'], "IMSHSS-D5A3FFB4203B3C83",'NodeIdIMSHSS-D5A3FFB4203B3C83','8000000001020302','10.184.73.102')
#print get_notification_trap('10.184.73.107', 7070, 'xoambaseserver', 'GMLC', 'CpuUnilizationRatioExceedThresholdAlarm_NEW', '10.184.73.77', auth_info=None,ne_name="GMLC-C6F681629B9A2427",node_id='NodeIdGMLC-C6F681629B9A2427',engine_id=None,client_ip='10.184.73.107')
