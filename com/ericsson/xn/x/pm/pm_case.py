# -*- coding: utf-8 -*-

import logging
import os
from logging.handlers import RotatingFileHandler
from com.ericsson.xn.commons.osutils import get_ne_info_from_cfg, get_pm_counters_map
from com.ericsson.xn.commons.PyProperties import Properties
from com.ericsson.xn.commons import CommonStatic
from com.ericsson.xn.x.ne import NeCommon
from com.ericsson.xn.x.pm import PmCommon


sep = os.sep
root_dir = os.path.dirname(os.path.abspath(__file__)).split(sep + 'com' + sep +
                                                            'ericsson' + sep + 'xn' + sep + 'x' + sep + 'pm')
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
    dict_browser = {
        "browser_type": '',
        "browser_path": '',
        "driver_path": ''
    }
    driver = CommonStatic.login_rsnms(dict_browser, '10.184.73.77')
    if driver:
        NeCommon.to_ne_management_page(driver, logger_pm)
        NeCommon.check_and_add_ne(driver, logger_pm, ne_info_pgw)

        CommonStatic.logout_rsnms(driver)
        CommonStatic.quite_driver(driver)