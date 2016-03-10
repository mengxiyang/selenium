#! -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager

BaseManager.register('platform_info')


def platform_info(ip, port, passwd):
    mgr = start_session(ip, port, passwd)
    return mgr.platform_info()


BaseManager.register('server_time')


def server_time(ip, port, passwd):
    mgr = start_session(ip, port, passwd)
    return mgr.server_time()


BaseManager.register('send_trap')


def send_trap(ip, port, passwd, ne_type, alarm, target_ip):
    mgr = start_session(ip, port, passwd)
    return mgr.send_trap(ne_type, alarm, target_ip)


def start_session(ip, port, passwd):
    mgr = BaseManager(address=(ip, port), authkey=passwd)
    mgr.connect()
    return mgr


def close_session(mgr):
    pass
