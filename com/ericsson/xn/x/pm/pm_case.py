# -*- coding: utf-8 -*-

import logging
import os
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from com.ericsson.xn.commons.osutils import get_ne_info_from_cfg, get_pm_counters_map
from com.ericsson.xn.commons.PyProperties import Properties
from com.ericsson.xn.commons import CommonStatic
from com.ericsson.xn.x.ne import NeCommon
from com.ericsson.xn.x.pm import PmCommon


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


def check_pm_accurate():
    global sep
    ne_info_pgw = get_ne_info_from_cfg(os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep +
                                                        'nes' + sep + 'pgw.cfg'))
    counters_pm = get_pm_counters_map(os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep +
                                                       'counters' + sep + 'pgw.cfg'))
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

    driver = CommonStatic.login_rsnms(dict_browser_chrome, '10.184.73.77', logger_pm)
    if driver:
        NeCommon.to_ne_management_page(driver, logger_pm)
        dict_ne_info = NeCommon.check_and_add_ne(driver, logger_pm, ne_info_pgw)

        PmCommon.to_pm_management_page(driver, logger_pm)
        # PmCommon.to_second_page(driver, logger_pm)
        PmCommon.to_tab_by_ne_type(driver, dict_ne_info['ne_type'], logger_pm)
        if PmCommon.wait_until_pm_date_show_up(driver, logger_pm, 300, dict_ne_info['ne_name']):
            t_now = datetime.now()
            minute_delta = t_now.minute % 5
            end_time = t_now + timedelta(minutes=-(9 + minute_delta))
            start_time = end_time + timedelta(hours=-1)
            PmCommon.init_and_search(driver, logger_pm, dict_ne_info['ne_name'], end_time, start_time)
            PmCommon.check_pm_rows(driver, logger_pm, 12, dict_ne_info['ne_type'], counters_pm)
        CommonStatic.logout_rsnms(driver)
        CommonStatic.quite_driver(driver)