# encoding=utf-8

"""
Created on Dec 11, 2015

@author: EJLNOQC
"""

import os
import platform
import logging

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

log_common = logging.getLogger('selenium.CommonStatic')

"""
The function mainly init the browser driver, return the instance of the selenium driver.
@list_browser: Map, should contain browser type, browser path and driver path.
"""


def login_rsnms(list_browser, host, port=8686):
    """
    The function mainly init the browser driver, return the instance of the selenium driver.
    :param list_browser: A Dict that contains the browser information, type, path, driver_path
    :param host: The host of the URL that try to open.
    :param port: The port number of the URL that try to open.
    :return: return the selenium driver instance so that can used in followed test steps.
    """
    log_common.info('Will start the web browser and perform test case.')


    logCommon.info('Will start web browser and perform test case.')
    chromedriver = os.path.normpath(driver)
    logCommon.info('Browser driver path: ' + str(chromedriver))
    os.environ["webdriver.chrome.driver"] = chromedriver
    opts = Options()
    if (not isMac):
        opts = Options()
        opts.binary_location = os.path.normpath(chrome)
    else:
        opts.add_argument("--start-maximized")
    driver = webdriver.Chrome(chromedriver, chrome_options=opts)
    # options.add_argument("--start-maximized")
    # driver.set_window_size(1024, 600)
    driver.maximize_window()
    # go to the google home page
    index = 'http://' + str(host) + ':' + str(port) + '/XOAM/login/index.html'
    logCommon.info('Web page: ' + str(index))
    driver.get(index)
    driver.find_element_by_id('loginUsername').clear()
    driver.find_element_by_id('loginUsername').send_keys(username)
    driver.find_element_by_id('loginPassword').clear()
    driver.find_element_by_id('loginPassword').send_keys(password)
    driver.find_element_by_id('submit').click()
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "ebBtnSearch")))
        logCommon.info('Login to the InterfaceManagement page successfully.')
    except Exception as e:
        logCommon.error('Login to the InterfaceManagement page failed.')
        return False
    return driver
