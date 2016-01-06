# -*- coding: utf-8 -*-

import logging
import os
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler

from com.ericsson.xn.commons import CommonStatic
from com.ericsson.xn.commons.PyProperties import Properties
from com.ericsson.xn.commons.osutils import get_ne_info_from_cfg, get_pm_counters_map
from com.ericsson.xn.x.ne import NeCommon
from com.ericsson.xn.x.pm.PmCommons import PmCommon

sep = os.sep
root_dir = os.path.dirname(os.path.abspath(__file__)).split(sep + 'com' + sep +
                                                            'ericsson' + sep + 'xn' + sep + 'x' + sep + 'pm')[0]
logger_pm = logging.getLogger('pm_accurate')
log_dir = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'logs')
if not os.path.isdir(log_dir):
    os.mkdir(log_dir)
log_cfg = Properties(os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'log_cfg.cfg'))
log_file = os.path.normpath(log_dir + sep + 'pm_accurate.log')
log_level = int(log_cfg.getProperty('log_level'))
log_formatter = logging.Formatter(('%(asctime)s [%(levelname)s] %(module)s %(funcName)s(%(lineno)d) %(message)s'))
log_handler = RotatingFileHandler(log_file, mode='a', maxBytes=1024 * 1024 * int(log_cfg.getProperty('log_maximum')),
                                  backupCount=10, encoding='utf-8', delay=0)
log_handler.setLevel(log_level)
log_handler.setFormatter(log_formatter)
logger_pm.setLevel(10)
logger_pm.addHandler(log_handler)

if 'YES' == log_cfg.getProperty('log_console').strip().upper():
    console_log = logging.StreamHandler()
    console_log.setLevel(log_level)
    console_log.setFormatter(log_formatter)
    logger_pm.addHandler(console_log)

logger_pm.info('Logger of PM part init successfully.')


def check_pm_accurate(ne_info_cfg, counter_info_cfg, tgt_server, str_end_time):
    global sep, logger_pm
    ne_info = get_ne_info_from_cfg(ne_info_cfg)
    counters_pm = get_pm_counters_map(counter_info_cfg)
    dict_browser_chrome = {
        "browser_type": 'chrome',
        "browser_path": 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        "driver_path": 'C:\Users\EJLNOQC\installed\chromedriver.exe'
    }

    dict_browser_firefox = {
        "browser_type": 'firefox',
        "browser_path": 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe',
        "driver_path": ''
    }

    driver = CommonStatic.login_rsnms(dict_browser_chrome, tgt_server, logger_pm)
    if driver:
        try:
            NeCommon.to_ne_management_page(driver, logger_pm)
            dict_ne_info = NeCommon.check_and_add_ne(driver, logger_pm, ne_info)

            PmCommon.to_pm_management_page(driver, logger_pm)
            # PmCommon.to_second_page(driver, logger_pm)
            PmCommon.to_tab_by_ne_type(driver, dict_ne_info['ne_type'], logger_pm)
            if PmCommon.wait_until_pm_date_show_up(driver, logger_pm, 300, dict_ne_info['ne_name']):
                t_now = datetime.now()
                # minute_delta = t_now.minute % 5
                # end_time = t_now + timedelta(minutes=-(delay_time + minute_delta))
                end_time = datetime.strptime(str_end_time, '%Y-%m-%d %H:%M:%S')
                pm_rounds = len(counters_pm)
                if 'OCGAS' == ne_info['ne_type']:
                    pm_rounds = len(counters_pm) / 2
                start_time = end_time + timedelta(minutes=-5 * pm_rounds)
                PmCommon.init_and_search(driver, logger_pm, dict_ne_info['ne_name'], end_time, start_time)
                ok = PmCommon.wait_until_rounds_ok(driver, logger_pm, len(counters_pm), 10, 5)
                if ok:
                    PmCommon.check_pm_rows(driver, logger_pm, dict_ne_info['ne_type'], counters_pm, 10, None)
                else:
                    logger_pm.error('Timeout ERROR.')
            CommonStatic.logout_rsnms(driver)
            # CommonStatic.quite_driver(driver)
        finally:
            CommonStatic.quite_driver(driver)


def check_pm_accurate_sbc(ne_info_cfg, counter_info_cfg, tgt_server, rounds):
    global sep, logger_pm
    ne_info = get_ne_info_from_cfg(ne_info_cfg)
    counters_pm = get_pm_counters_map(counter_info_cfg)
    dict_browser_chrome = {
        "browser_type": 'chrome',
        "browser_path": 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        "driver_path": 'C:\Users\EJLNOQC\installed\chromedriver.exe'
    }

    dict_browser_firefox = {
        "browser_type": 'firefox',
        "browser_path": 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe',
        "driver_path": ''
    }

    driver = CommonStatic.login_rsnms(dict_browser_chrome, tgt_server, logger_pm)
    if driver:
        try:
            NeCommon.to_ne_management_page(driver, logger_pm)
            dict_ne_info = NeCommon.check_and_add_ne(driver, logger_pm, ne_info)

            PmCommon.to_pm_management_page(driver, logger_pm)
            # PmCommon.to_second_page(driver, logger_pm)
            PmCommon.to_tab_by_ne_type(driver, dict_ne_info['ne_type'], logger_pm)
            if PmCommon.wait_until_pm_date_show_up(driver, logger_pm, 300, dict_ne_info['ne_name']):
                PmCommon.init_and_search(driver, logger_pm, dict_ne_info['ne_name'])

                dict_additional = {"rounds": rounds}

                ok = PmCommon.wait_until_rounds_ok(driver, logger_pm, dict_additional['rounds'], 10, None)
                if ok:
                    PmCommon.check_pm_rows(driver, logger_pm, dict_ne_info['ne_type'], counters_pm, 10, dict_additional)
                else:
                    logger_pm.error('FAILED: Wait for SBC PM timeout.')
            CommonStatic.logout_rsnms(driver)
            # CommonStatic.quite_driver(driver)
        finally:
            CommonStatic.quite_driver(driver)


def check_pm_accurate_all_ne(dict_all_nes, tgt_server):
    global sep, logger_pm
    dict_browser_chrome = {
        "browser_type": 'chrome',
        "browser_path": 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        "driver_path": 'C:\Users\EJLNOQC\installed\chromedriver.exe'
    }

    dict_browser_firefox = {
        "browser_type": 'firefox',
        "browser_path": 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe',
        "driver_path": ''
    }

    driver = CommonStatic.login_rsnms(dict_browser_chrome, tgt_server, logger_pm)
    if driver:
        try:
            # check the sbc
            logger_pm.info('******************** Start to check PM for SBC ************************')
            sbc_ne_dict = dict_all_nes['SBC']
            ne_info = get_ne_info_from_cfg(sbc_ne_dict['ne_cfg'])
            counters_pm = get_pm_counters_map(sbc_ne_dict['ct_cfg'])

            NeCommon.to_ne_management_page(driver, logger_pm)
            dict_ne_info = NeCommon.check_and_add_ne(driver, logger_pm, ne_info)

            PmCommon.to_pm_management_page(driver, logger_pm)
            # PmCommon.to_second_page(driver, logger_pm)
            PmCommon.to_tab_by_ne_type(driver, dict_ne_info['ne_type'], logger_pm)
            if PmCommon.wait_until_pm_date_show_up(driver, logger_pm, 300, dict_ne_info['ne_name']):
                PmCommon.init_and_search(driver, logger_pm, dict_ne_info['ne_name'])

                dict_additional = {"rounds": sbc_ne_dict['rounds']}

                ok = PmCommon.wait_until_rounds_ok(driver, logger_pm, dict_additional['rounds'], 10, None)
                if ok:
                    PmCommon.check_pm_rows(driver, logger_pm, dict_ne_info['ne_type'], counters_pm, 10, dict_additional)
                else:
                    logger_pm.error('FAILED: Wait for SBC PM timeout.')

            # check other 5 NEs
            for k, v in dict_all_nes.iteritems:
                if 'SBC' != k:
                    logger_pm.info('******************** Start to check PM for ' + str(k) + ' ************************')
                    ne_info = get_ne_info_from_cfg(v['ne_cfg'])
                    counters_pm = get_pm_counters_map(v['ct_cfg'])

                    NeCommon.to_ne_management_page(driver, logger_pm)
                    dict_ne_info = NeCommon.check_and_add_ne(driver, logger_pm, ne_info)
                    PmCommon.to_pm_management_page(driver, logger_pm)
                    # PmCommon.to_second_page(driver, logger_pm)
                    PmCommon.to_tab_by_ne_type(driver, dict_ne_info['ne_type'], logger_pm)
                    if PmCommon.wait_until_pm_date_show_up(driver, logger_pm, 300, dict_ne_info['ne_name']):
                        # t_now = datetime.now()
                        # minute_delta = t_now.minute % 5
                        # end_time = t_now + timedelta(minutes=-(delay_time + minute_delta))
                        end_time = datetime.strptime(v['end_time'], '%Y-%m-%d %H:%M:%S')
                        pm_rounds = len(counters_pm)
                        if 'OCGAS' == ne_info['ne_type']:
                            pm_rounds = len(counters_pm) / 2

                        check_rounds = len(counters_pm)
                        # if 'SGW' == ne_info['ne_type'] or 'PGW' == ne_info['ne_type']:
                        #    check_rounds = 4

                        start_time = end_time + timedelta(minutes=-5 * pm_rounds)
                        PmCommon.init_and_search(driver, logger_pm, dict_ne_info['ne_name'], end_time, start_time)
                        ok = PmCommon.wait_until_rounds_ok(driver, logger_pm, check_rounds, 10, 5)
                        if ok:
                            PmCommon.check_pm_rows(driver, logger_pm, dict_ne_info['ne_type'], counters_pm, 10, None)
                        else:
                            logger_pm.error('Timeout ERROR.')

            CommonStatic.logout_rsnms(driver)
            # CommonStatic.quite_driver(driver)
        finally:
            CommonStatic.quite_driver(driver)