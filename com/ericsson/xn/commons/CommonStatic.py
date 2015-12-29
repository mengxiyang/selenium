# encoding=utf-8

"""
Created on Dec 11, 2015

@author: EJLNOQC
"""

import os
import logging
import platform

import subprocess
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from . import osutils
from selenium.common.exceptions import TimeoutException

log_common = logging.getLogger('selenium.CommonStatic')


def login_rsnms(list_browser, host, username='admin', password='Admin!@#123', port=8686):
    """
    The function mainly init the browser driver, return the instance of the selenium driver.
    :param password: the password of the RSNMS system.
    :param username: the username of the RSNMS system.
    :param list_browser: A Dict that contains the browser information, type, path, driver_path.
    :param host: The host of the URL that try to open.
    :param port: The port number of the URL that try to open.
    :return: return the selenium driver instance so that can used in followed test steps.
    """
    log_common.info('Will start the web browser and perform test case.')
    # first edition only support the chrome on windows platform
    if 'Windows' == osutils.get_os_type():
        if 'chrome' == list_browser['browser_type']:
            windows_chrome_login_rsnms(list_browser['browser_path'], list_browser['driver_path'],
                                       host, username, password, port)


def windows_chrome_login_rsnms(browser_path, driver_path, host, username, password, port):
    """
    init selenium driver for chrome on windows platform.
    :param browser_path: chrome installation path
    :param driver_path: selenium path
    :param host: host ip of target rsnms server
    :param username: username that to login to the rsnms server
    :param password: password that to login to the rsnms server
    :param port: port number of target url
    :return: the driver instance of the selenium
    """
    chrome_driver = os.path.normpath(driver_path)
    log_common.info('Browser driver path: ' + str(chrome_driver))
    os.environ["webdriver.chrome.driver"] = chrome_driver
    opts = Options()
    opts.binary_location = os.path.normpath(browser_path)
    log_common.info('Browser path: ' + str(browser_path))
    driver = webdriver.Chrome(chrome_driver, chrome_options=opts)
    # driver.set_window_size(1024, 600)
    driver.maximize_window()
    login_first_page(driver, host, username, password, port)


def login_first_page(driver, host, username, password, port):
    index = 'http://' + str(host) + ':' + str(port) + '/XOAM/login/index.html'
    log_common.info('Web page: ' + str(index))
    driver.get(index)
    driver.find_element_by_id('loginUsername').clear()
    driver.find_element_by_id('loginUsername').send_keys(username)
    driver.find_element_by_id('loginPassword').clear()
    driver.find_element_by_id('loginPassword').send_keys(password)
    driver.find_element_by_id('submit').click()
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "ebBtnSearch")))
        log_common.info('Login to the InterfaceManagement page successfully.')
    except Exception as e:
        log_common.error('Login to the InterfaceManagement page failed. ERROR: ' + str(e))
        return None
    return driver


def quite_driver(driver):
    try:
        driver.close()
        cmd = ''
        if 'Windows' == platform.system():
            cmd = 'TASKKILL /IM chromedriver.exe /F'
        elif 'Darwin' == platform.system():
            cmd = 'pkill chromedriver'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        p.kill()
    finally:
        pass
