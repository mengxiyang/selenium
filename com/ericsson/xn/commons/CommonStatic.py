# encoding=utf-8

"""
Created on Dec 11, 2015

@author: EJLNOQC
"""

import os
import platform

import subprocess
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from . import osutils
from com.ericsson.xn.commons import test_logger as test


def login_rsnms(dict_browser, host, username='admin', password='Admin!@#123', port=8686,
                url='/XOAM/login/index.html'):
    """
    The function mainly init the browser driver, return the instance of the selenium driver.
    :param password: the password of the RSNMS system.
    :param username: the username of the RSNMS system.
    :param dict_browser: A Dict that contains the browser information, type, path, driver_path.
    :param host: The host of the URL that try to open.
    :param port: The port number of the URL that try to open.
    :return: return the selenium driver instance so that can used in followed test steps.
    """
    test.info('Will start the web browser and perform test case.')
    # first edition only support the chrome on windows platform
    if 'Windows' == osutils.get_os_type():
        if 'chrome' == dict_browser['browser_type']:
            return windows_chrome_login_rsnms(dict_browser['browser_path'], dict_browser['driver_path'], host,
                                              username, password, port, url)
        elif 'firefox' == dict_browser['browser_type']:
            return windows_firefox_login_rsnms(dict_browser['browser_path'], dict_browser['driver_path'], host,
                                               username, password, port, url)


def windows_firefox_login_rsnms(browser_path, driver_path, host, username, password, port, url):
    browser_path = os.path.normpath(browser_path)
    test.info('Browser path: ' + str(browser_path))
    firfox_bin = webdriver.firefox.firefox_binary.FirefoxBinary(browser_path)
    driver = webdriver.Firefox(firefox_binary=firfox_bin)
    driver.maximize_window()
    login_first_page(driver, host, username, password, port)
    return driver


def windows_chrome_login_rsnms(browser_path, driver_path, host, username, password, port, url):
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
    test.info('Browser driver path: ' + str(chrome_driver))
    os.environ["webdriver.chrome.driver"] = chrome_driver
    opts = Options()
    opts.binary_location = os.path.normpath(browser_path)
    test.info('Browser path: ' + str(browser_path))
    driver = webdriver.Chrome(chrome_driver, chrome_options=opts)
    # driver.set_window_size(1024, 600)
    driver.maximize_window()
    login_first_page(driver, host, username, password, port, url)
    return driver


def login_first_page(driver, host, username, password, port, url):
    index = 'http://' + str(host) + ':' + str(port) + url
    test.info('Web page: ' + str(index))
    driver.get(index)
    driver.find_element_by_id('loginUsername').clear()
    driver.find_element_by_id('loginUsername').send_keys(username)
    driver.find_element_by_id('loginPassword').clear()
    driver.find_element_by_id('loginPassword').send_keys(password)
    driver.find_element_by_id('submit').click()
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ebBtnSearch")))
        test.info('Login to the InterfaceManagement page successfully.')
    except Exception as e:
        test.error('Login to the InterfaceManagement page failed. ERROR: ' + str(e))
        return None


def logout_rsnms(driver):
    id_logout_btn = (By.CLASS_NAME, "eaContainer-LogoutButton")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(id_logout_btn)).click()

    id_conform_btn = (By.XPATH, "//div[@class='ebDialogBox']/div[2]/button")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(id_conform_btn)).click()


def quite_driver(driver):
    try:
        driver.close()
    finally:
        pass
