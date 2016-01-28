# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from com.ericsson.xn.commons import CommonStatic
from com.ericsson.xn.commons.PyProperties import Properties
from com.ericsson.xn.commons.osutils import get_ne_info_from_cfg, get_pm_counters_map
from com.ericsson.xn.x.ne import NeCommon
from com.ericsson.xn.x.pm.PmCommons import PmCommon
from com.ericsson.xn.commons import test_logger as test


def check_pm_accurate(ne_info_cfg, counter_info_cfg, server_info_path, str_end_time, me_counter_cfg=None):
    ne_info = get_ne_info_from_cfg(ne_info_cfg)
    counters_pm = get_pm_counters_map(counter_info_cfg)
    server_info = Properties(server_info_path)
    dict_browser_chrome = {
        "browser_type": server_info.getProperty('browser_type'),
        "browser_path": server_info.getProperty('browser_path'),
        "driver_path": server_info.getProperty('driver_path')
    }

    host = server_info.getProperty('host')
    username = server_info.getProperty('username')
    password = server_info.getProperty('password')
    port = server_info.getProperty('port')
    url = server_info.getProperty('url')
    dict_additinal = {
        'number_of_lic': 4
    }

    driver = CommonStatic.login_rsnms(dict_browser_chrome, host, username, password, port, url)
    if driver:
        try:
            NeCommon.to_ne_management_page_by_url(driver, server_info)
            dict_ne_info = NeCommon.check_and_add_ne(driver, ne_info)

            PmCommon.to_pm_management_page_by_url(driver, ne_info['ne_type'], server_info)
            PmCommon.make_in_correct_tab(driver, ne_info['tab_pre'], '')
            PmCommon.wait_until_pm_date_show_up(driver, dict_ne_info['ne_name'])

            end_time = datetime.strptime(str_end_time, '%Y-%m-%d %H:%M:%S')
            if 0 != len(counters_pm) % dict_additinal['number_of_lic']:
                test.error('Expected couters config file mismatch with the lic number.')
            else:
                start_time = end_time + timedelta(minutes=-5 * len(counters_pm) / dict_additinal['number_of_lic'])
                PmCommon.init_and_search(driver, dict_ne_info['ne_name'], end_time, start_time)
                PmCommon.wait_until_rounds_ok(driver, len(counters_pm), 10, dict_additinal)
                PmCommon.check_pm_rows_updated(driver, dict_ne_info['ne_type'], counters_pm, 10, dict_additinal)

                if ne_info.has_key('tab_me') and me_counter_cfg is not None:
                    test.info('Found ME Tab infomation, will check ME counters.')
                    me_counters = get_pm_counters_map(me_counter_cfg)
                    PmCommon.make_in_correct_tab(driver, ne_info['tab_me'], '')
                    PmCommon.wait_until_pm_date_show_up(driver, dict_ne_info['ne_name'])

                    dict_me_add = {
                        'number_of_lic': 1
                    }
                    PmCommon.init_and_search(driver, dict_ne_info['ne_name'], end_time, start_time)
                    PmCommon.wait_until_rounds_ok(driver, len(counters_pm), 10, dict_me_add)
                    PmCommon.check_me_counters(driver, dict_ne_info['ne_name'], me_counters, 10, dict_me_add)

                CommonStatic.logout_rsnms(driver)
        finally:
            CommonStatic.quite_driver(driver)
