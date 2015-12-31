# -*- coding: utf-8 -*-

import sys
from time import sleep
import os
import binascii
from selenium.webdriver.common.by import By
from com.ericsson.xn.commons.funcutils import find_single_widget, find_all_widgets, wait_until_text_shown_up, \
    is_pair_nes, ne_type_index_add_ne_page


def to_ne_management_page(driver, logger):
    logger.info('To the PmManagement page...')

    identifier = (By.XPATH, "//div[@class='ebLayout-Navigation']/div/div[1]/span")
    find_single_widget(driver, 10, identifier).click()

    identifier = (By.XPATH, "//div[@class='ebBreadcrumbs-list']/ul/li[1]/a")
    find_single_widget(driver, 10, identifier).click()

    id_new_btn = (By.ID, "idBtn-create")
    find_single_widget(driver, 10, id_new_btn)


def check_and_add_ne(driver, logger, dict_ne_info):
    ne_exist, ne_name = check_ne_exist(driver, logger, dict_ne_info["ne_type"], dict_ne_info["ne_ip"])
    if 2 == ne_exist:
        logger.critical('A ne with the given IP named: ' + ne_name + ' already exist.')
        sys.exit(0)
    elif 1 == ne_exist:
        dict_ne_info["ne_name"] = ne_name
    elif 1 > ne_exist:
        dict_ne_info["ne_name"] = add_new_ne(driver, logger, dict_ne_info)
    return dict_ne_info


def add_new_ne(driver, logger, dict_ne_info):
    find_single_widget(driver, 10, (By.ID, "idBtn-create")).click()
    sleep(.5)
    # choose the correct ne_type
    id_select_ne_type = (By.XPATH, "//div[@id='i_netype']/div/button")
    find_single_widget(driver, 10, id_select_ne_type).click()

    id_ne_type_list = (By.XPATH, "//div[@id='i_netype']/div/div/div[" +
                       str(ne_type_index_add_ne_page(dict_ne_info["ne_type"])) + "]")
    find_single_widget(driver, 10, id_ne_type_list).click()
    sleep(.5)

    # insert the common part
    id_ne_name = (By.ID, "i_nename")
    id_ne_ip = (By.ID, "i_neip")
    id_ne_user = (By.ID, "i_neuser")
    id_password = (By.ID, "i_nepassword")
    id_ne_port = (By.ID, "i_neport")

    id_sftp_port = (By.ID, "i_nesftpport")

    id_pm_path = (By.ID, "i_nepmfilepath")
    id_log_path = (By.ID, "i_nelogfilepath")
    id_alarm_path = (By.ID, "i_nefmfilepath")

    id_li_pwd = (By.ID, "i_nelipwd")
    id_fro_id = (By.ID, "i_nefroid")

    ne_name = dict_ne_info["ne_type"] + "-" + str(binascii.hexlify(os.urandom(8)))
    w_ne_name = find_single_widget(driver, 10, id_ne_name)
    w_ne_name.clear()
    w_ne_name.send_keys(ne_name)

    w_ne_ip = find_single_widget(driver, 10, id_ne_ip)
    w_ne_ip.clear()
    w_ne_ip.send_keys(dict_ne_info["ne_ip"])

    w_ne_user = find_single_widget(driver, 10, id_ne_user)
    w_ne_user.clear()
    w_ne_user.send_keys(dict_ne_info["ne_user"])

    w_ne_password = find_single_widget(driver, 10, id_password)
    w_ne_password.clear()
    w_ne_password.send_keys(dict_ne_info["ne_password"])

    w_ne_port = find_single_widget(driver, 10, id_ne_port)
    w_ne_port.clear()
    w_ne_port.send_keys(dict_ne_info["ne_port"])

    if 'SBC' == dict_ne_info["ne_type"]:
        w_li_pwd = find_single_widget(driver, 10, id_li_pwd)
        w_li_pwd.clear()
        w_li_pwd.send_keys(dict_ne_info["li_pwd"])

        w_fro_id = find_single_widget(driver, 10, id_fro_id)
        w_fro_id.clear()
        w_fro_id.send_keys(dict_ne_info["fro_id"])
    else:
        w_sftp_port = find_single_widget(driver, 10, id_sftp_port)
        w_sftp_port.clear()
        w_sftp_port.send_keys(dict_ne_info["sftp_port"])

        w_pm_path = find_single_widget(driver, 10, id_pm_path)
        w_pm_path.clear()
        w_pm_path.send_keys(dict_ne_info["pm_path"])

        w_log_path = find_single_widget(driver, 10, id_log_path)
        w_log_path.clear()
        w_log_path.send_keys(dict_ne_info["log_path"])

        if 'OCGAS' == dict_ne_info["ne_type"]:
            w_alarm_path = find_single_widget(driver, 10, id_alarm_path)
            w_alarm_path.clear()
            w_alarm_path.send_keys(dict_ne_info["alarm_path"])

    id_submit_btn = (By.ID, "idBtn-save")
    find_single_widget(driver, 10, id_submit_btn).click()
    return ne_name


def check_ne_exist(driver, logger, ne_type, ne_ip):
    # note there is another way to check if NE with certain IP exist, that is connect to the server's database and
    # check the NES data table
    id_table = (By.XPATH, "//div[@id='dv1']/div[2]/div/div/div[3]/div/div/div/table")
    table = find_single_widget(driver, 10, id_table)

    id_trs = (By.XPATH, ".//tbody/tr")
    trs = find_all_widgets(table, 20, id_trs)

    for tr in trs:
        # gui_type = tr.get_attribute('innerHTML').encode('utf-8')
        gui_ne_name = find_single_widget(tr, 10, (By.XPATH, ".//td[1]")).get_attribute('innerHTML').encode('utf-8')
        gui_ne_type = find_single_widget(tr, 10, (By.XPATH, ".//td[2]")).get_attribute('innerHTML').encode('utf-8')

        tr.click()
        if wait_until_text_shown_up(driver, 10, (By.ID, "i_nename"), gui_ne_name):
            gui_ip = find_single_widget(driver, 10, (By.ID, "i_neip"))
            if ne_ip == gui_ip.get_attribute('value').encode('utf-8').strip():
                if ne_type == gui_ne_type:
                    # NE with same ip and same type exit
                    return 1, gui_ne_name
                else:
                    if is_pair_nes(gui_ne_type.upper(), ne_type.upper()):
                        # this means that there is a pair NE with same IP exist, but we can still add a NE
                        return 0, None
                    else:
                        # this means a NE with different type but the same IP already exist.
                        return 2, gui_ne_name
    # the ip that we want to add does not exist
    return -1, None
