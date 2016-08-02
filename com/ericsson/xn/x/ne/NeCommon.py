# -*- coding: utf-8 -*-

import sys
from time import sleep
import os
import time
import binascii
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from com.ericsson.xn.commons.funcutils import find_single_widget, find_all_widgets, wait_until_text_shown_up, \
    is_pair_nes
from com.ericsson.xn.commons import test_logger as test
from com.ericsson.xn.x.fm.FmCommons import FmCommon


def to_ne_management_page(driver, logger):
    logger.info('To the NeManagement page...')

    identifier = (By.XPATH, "//div[@class='ebLayout-Navigation']/div/div[1]/span")
    find_single_widget(driver, 10, identifier).click()

    identifier = (By.XPATH, "//div[@class='ebBreadcrumbs-list']/ul/li[1]/a")
    find_single_widget(driver, 10, identifier).click()

    id_new_btn = (By.ID, "idBtn-create")
    find_single_widget(driver, 10, id_new_btn)


def to_ne_management_page_by_url(driver, server_info, url_add='#network-overview/ne-management'):
    test.info("To the NE Management page...")
    base_url = 'https://' + server_info.getProperty('host') + ':' + str(server_info.getProperty('port')) + \
               server_info.getProperty('preurl')
    test.info('NeMgt URL is: ' + base_url + url_add)
    driver.get(base_url + url_add)
    test.info("Login to the NeManagement page successfully")


def check_and_add_ne(driver, dict_ne_info):
    ne_exist, ne_name = check_ne_exist_by_type(driver, dict_ne_info["ne_type"],
                                               dict_ne_info["ne_ip"],dict_ne_info.get('engine_id'))
    if 2 == ne_exist:
        FmCommon.quitDriver(driver)
        test.error('A ne already exist with the given IP or engineId named: ' + ne_name)
    elif 1 == ne_exist:
        test.info("NE already exist, reuse the old NE named: " + ne_name)
        dict_ne_info["ne_name"] = ne_name
    elif 0 == ne_exist:
        test.info("Paired NE, add a new one")
        ne_name = add_new_ne(driver,dict_ne_info)
        dict_ne_info["ne_name"] = ne_name
    elif -1 == ne_exist or -2 == ne_exist:
        test.info("NE not exist, add a new one")
        ne_name = add_new_ne(driver, dict_ne_info)
        dict_ne_info["ne_name"] = ne_name

    refresh_ne_management_page(driver)
    test.info("NE:" + ne_name + " added successfully")
    return dict_ne_info


def refresh_ne_management_page(driver):
    driver.refresh()
    # check page loaded
    find_single_widget(driver, 10, (By.ID, "idBtn-create"))


def add_new_ne(driver, dict_ne_info):
    find_single_widget(driver, 10, (By.ID, "idBtn-create")).click()
    sleep(.5)
    # choose the correct ne_type
    id_select_ne_type = (By.XPATH, "//div[@id='i_netype']/div/button")
    find_single_widget(driver, 10, id_select_ne_type).click()

    # id_ne_type_list = (By.XPATH, "//div[@id='i_netype']/div/div/div[" +
    #                  str(ne_type_index_add_ne_page(dict_ne_info["ne_type"])) + "]")
    ne_type = dict_ne_info["ne_type"]
    id_ne_type_list = (By.XPATH, "//div[@id='i_netype']/div/div/div[@title='" + ne_type + "']")
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
    
    #add for HSS and IMS
    id_snmp_port = (By.ID,"i_snmpport")
    id_usmusername = (By.ID,"i_usmusername")
    id_i_authpwd = (By.ID,"i_authpwd")
    id_i_privpwd = (By.ID,"i_privpwd")
    id_i_appuser = (By.ID,"i_serviceusername")
    id_i_apppwd = (By.ID,"i_servicepwd")
    id_i_engineid = (By.ID,"i_engineid")
    id_sftp_user = (By.ID, "i_nesftpuser")
    id_sftp_password = (By.ID,"i_nesftppassword")

    ne_name = dict_ne_info["ne_type"] + "-" + str(binascii.hexlify(os.urandom(8))).upper()
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
        
        if dict_ne_info["ne_type"] in ("IMSHSS","LTEHSS","MSC","HLR","3GSGSN","GGSN"):
            w_snmp_port = find_single_widget(driver, 10, id_snmp_port)
            w_snmp_port.clear()
            w_snmp_port.send_keys(dict_ne_info["snmp_port"])
        
            w_usm_user = find_single_widget(driver, 10, id_usmusername)
            w_usm_user.clear()
            w_usm_user.send_keys(dict_ne_info["usm_user"])
        
            w_auth_pwd = find_single_widget(driver, 10, id_i_authpwd)
            w_auth_pwd.clear()
            w_auth_pwd.send_keys(dict_ne_info["auth_password"])
        
            w_priv_pwd = find_single_widget(driver, 10, id_i_privpwd)
            w_priv_pwd.clear()
            w_priv_pwd.send_keys(dict_ne_info["priv_password"])
            
        
            w_app_user = find_single_widget(driver, 10, id_i_appuser)
            w_app_user.clear()
            w_app_user.send_keys(dict_ne_info["app_user"])
            
            w_app_pwd = find_single_widget(driver, 10, id_i_apppwd)
            w_app_pwd.clear()
            w_app_pwd.send_keys(dict_ne_info["app_password"])

            w_engine_id = find_single_widget(driver,10,id_i_engineid)
            w_engine_id.clear()
            w_engine_id.send_keys(dict_ne_info["engine_id"])


            w_sftp_user = find_single_widget(driver,10,id_sftp_user)
            w_sftp_user.clear()
            w_sftp_user.send_keys(dict_ne_info["sftp_user"])

            w_sftp_password = find_single_widget(driver,10,id_sftp_password)
            w_sftp_password.clear()
            w_sftp_password.send_keys(dict_ne_info["sftp_password"])
    
        elif dict_ne_info["ne_type"] in ("GMLC","OCGAS"):
            w_alarm_path = find_single_widget(driver, 10, id_alarm_path)
            w_alarm_path.clear()
            w_alarm_path.send_keys(dict_ne_info["alarm_path"])

    id_submit_btn = (By.ID, "idBtn-save")
    find_single_widget(driver, 10, id_submit_btn).click()
    try:
        id_dialog_confirm = (By.XPATH, "//div[@class='ebDialogBox-actionBlock']/button[1]")
        find_single_widget(driver, 10,id_dialog_confirm).click()
    except Exception as e:
        test.info('There is no duplicated NEs.')
    test.info('Successfully added an NE: ' + str(ne_name))
    return ne_name


def check_ne_exist_by_type(driver, ne_type, ne_ip, engine_id, page_no=20):
    # note there is another way to check if NE with certain IP exist, that is connect to the server's database and
    # check the NES data table
    id_table = (By.XPATH, "//div[@id='dv1']/div[2]/div/div/div[3]/div/div/div/table")
    table = find_single_widget(driver, 10, id_table)

    id_page = (By.XPATH, "//div[@id='dv1']/div[2]/div/div/div[2]/div/input")
    pages = find_single_widget(driver, 10, id_page)
    pages.clear()
    pages.send_keys(page_no)
    ActionChains(driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

    '''
    id_netype_filter = (By.XPATH,".//thead/tr[2]/th[2]/input")
    netype_filter = find_single_widget(table,10,id_netype_filter)
    netype_filter.clear()
    netype_filter.send_keys(ne_type)
    '''

    # set ne type
    # id_type = (By.XPATH, "//div[@id='dv1']/div[2]/div/div/div[3]/div/div/div/table/thead/tr[2]/th[2]/input")
    # w_ne_type = find_single_widget(driver, 10, id_type)
    # w_ne_type.clear()
    # w_ne_type.send_keys(ne_type)

    id_trs = (By.XPATH, ".//tbody/tr")
    try:
        trs = find_all_widgets(table, 20, id_trs)
    except Exception as e:
        return -2,None

    try:
        is_has_pair_nes = False
        for tr in trs:
            # gui_type = tr.get_attribute('innerHTML').encode('utf-8')
            gui_ne_name = find_single_widget(tr, 10, (By.XPATH, ".//td[1]")).get_attribute('innerHTML').encode('utf-8')
            gui_ne_type = find_single_widget(tr, 10, (By.XPATH, ".//td[2]")).get_attribute('innerHTML').encode('utf-8')
            tr.click()
            if wait_until_text_shown_up(driver, 10, (By.ID, "i_nename"), gui_ne_name):
                gui_ip = find_single_widget(driver, 10, (By.ID, "i_neip")).get_attribute('value').encode('utf-8').strip()
                if ne_type in ("IMSHSS","LTEHSS","3GSGSN","GGSN","MSC","HLR"):
                    if gui_ne_type in ("IMSHSS","LTEHSS","3GSGSN","GGSN","MSC","HLR"):
                        gui_engineid = find_single_widget(driver,10,(By.ID,"i_engineid")).get_attribute('value').encode('utf-8').strip()
                        if engine_id != None:
                            if engine_id == gui_engineid or ne_ip == gui_ip:
                                if is_pair_nes(ne_type.upper(),gui_ne_type.upper()):
                                    is_has_pair_nes = True
                                elif ne_type == gui_ne_type and ne_ip == gui_ip:
                                    return 1,gui_ne_name
                                else:
                                    return 2,gui_ne_name
                        else:
                            FmCommon.quitDriver(driver)
                            test.error("engine_id not configured for " + ne_type)

                if ne_ip == gui_ip:
                    if ne_type == gui_ne_type:
                        # NE with same ip and same type exit
                        return 1, gui_ne_name
                    else:
                        if is_pair_nes(gui_ne_type.upper(), ne_type.upper()):
                            # this means that there is a pair NE with same IP exist, but we can still add a NE
                            # but will check if NE with the same type & same IP exist
                            is_has_pair_nes = True
                        else:
                            # this means a NE with different type but the same IP already exist.
                            return 2, gui_ne_name
        if is_has_pair_nes:
            return 0, None
        # the ip that we want to add does not exist
        return -1, None
    except Exception as e:
        # exceptions
        FmCommon.quitDriver(driver)
        test.error(str(e))

def check_ne_exist(driver, ne_type, ne_ip):
    # note there is another way to check if NE with certain IP exist, that is connect to the server's database and
    # check the NES data table
    id_table = (By.XPATH, "//div[@id='dv1']/div[2]/div/div/div[3]/div/div/div/table")
    table = find_single_widget(driver, 10, id_table)

    id_trs = (By.XPATH, ".//tbody/tr")
    try:
        trs = find_all_widgets(table, 20, id_trs)
        is_has_pair_nes = False
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
                            # but will check if NE with the same type & same IP exist
                            is_has_pair_nes = True
                        else:
                            # this means a NE with different type but the same IP already exist.
                            return 2, gui_ne_name
        if is_has_pair_nes:
            return 0, None
        # the ip that we want to add does not exist
        return -1, None
    except Exception as e:
        # the ip that we want to add does not exist
        return -2, None
