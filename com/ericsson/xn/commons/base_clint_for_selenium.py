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


def send_trap(ip, port, passwd, ne_type, alarm, target_ip, trap_port=None):
    mgr = start_session(ip, port, passwd)
    return mgr.send_trap(ne_type, alarm, target_ip, trap_port)._getvalue()


BaseManager.register('send_trap_nbi')


def send_trap_nbi(ip, port, passwd, ne_type, alarm, host,
                  auth_info=None, nbi_raw='/opt/LINBI/TestTool_CMCC_N13A/bin/raw_catch.log', t_port=None):
    mgr = start_session(ip, port, passwd)
    return mgr.send_trap_nbi(ne_type, alarm, host, auth_info, nbi_raw, t_port)._getvalue()


def start_session(ip, port, passwd):
    mgr = BaseManager(address=(ip, port), authkey=passwd)
    mgr.connect()
    return mgr


def close_session(mgr):
    pass

# print datetime.now().strftime('%H:%M:%S:%f')
# print send_trap('10.184.74.67', 7070, 'xoambaseserver', 'OCGAS', 'monitorTargetExceedThreshold', '127.0.0.1')
# print datetime.now().strftime('%H:%M:%S:%f')
'''
from datetime import datetime
print datetime.now().strftime('%H:%M:%S:%f')
print send_trap_nbi('127.0.0.1', 7070, 'xoambaseserver', 'LTEHSS', 'SoftwareProgramError-1', '127.0.0.1', ['privUser1', 'authUser1', 'privUser1'], '/Users/lowitty/temp/x.txt', 11162)
print datetime.now().strftime('%H:%M:%S:%f')
'''