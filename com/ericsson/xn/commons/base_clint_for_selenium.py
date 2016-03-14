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


def send_trap(ip, port, passwd, ne_type, alarm, target_ip, trap_port=162):
    mgr = start_session(ip, port, passwd)
    return mgr.send_trap(ne_type, alarm, target_ip, trap_port)._getvalue()


def start_session(ip, port, passwd):
    mgr = BaseManager(address=(ip, port), authkey=passwd)
    mgr.connect()
    return mgr


def close_session(mgr):
    pass

# print datetime.now().strftime('%H:%M:%S:%f')
# print send_trap('10.184.74.67', 7070, 'xoambaseserver', 'OCGAS', 'monitorTargetExceedThreshold', '127.0.0.1')
# print datetime.now().strftime('%H:%M:%S:%f')