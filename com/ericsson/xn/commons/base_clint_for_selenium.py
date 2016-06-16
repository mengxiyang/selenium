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


def send_trap(ip, port, passwd, ne_type, alarm, target_ip,auth_info=None, trap_port=None):
    mgr = start_session(ip, port, passwd)
    return mgr.send_trap(ne_type, alarm, target_ip,auth_info, trap_port)._getvalue()


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


def close_session(mgr):
    pass


BaseManager.register('get_alarm_list_trap')


def get_alarm_list_trap(ip, port, passwd, ne_type, alarm, host, auth_info, ne_name, n_port = None):
    mgr = start_session(ip, port, passwd)
    return mgr.get_alarm_list_trap(ne_type, alarm, host, auth_info, ne_name, n_port)._getvalue()


# print datetime.now().strftime('%H:%M:%S:%f')
#print send_trap('10.184.74.67', 7070,'xoambaseserver', 'OCGAS', 'monitorTargetsExceedThreshold', '10.184.74.68', [])
# print datetime.now().strftime('%H:%M:%S:%f')
'''
from datetime import datetime
print datetime.now().strftime('%H:%M:%S:%f')
print send_trap_nbi('10.184.74.68', 7070, 'xoambaseserver', 'LTEHSS', 'COMMUNICATIONFAULT_NEW', '10.184.74.68', ['privUser1', 'authUser1', 'privUser1'], LTEHSS)
print datetime.now().strftime('%H:%M:%S:%f')
'''
#print get_nodeid_by_nename('10.184.73.76', 7070, 'xoambaseserver','OCGAS-6E8DD56B5C655707')
#print get_alarm_list_trap('10.184.73.76', 7070, 'xoambaseserver', 'GMLC', 'cpuUnilizationRatioExceedThresholdAlarm_NEW', '10.184.73.76', ['privUser1', 'authUser1', 'privUser1'], "IMSHSS-7203C3FBC7C0CCA0")
#print get_alarm_list_trap('10.184.73.76', 7070, 'xoambaseserver', 'GMLC', 'A21ExceedThresholdAlarm_NEW', '10.184.73.76', None, "GMLC-13EFDD7B6A24DB45")