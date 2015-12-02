#endoing=utf-8
'''
Created on Dec 2, 2015

@author: lowitty
'''
import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def loginToInterface(chrome, driver, host, port = 8686, username = 'admin', password = 'Admin!@#123'):
    chromeDriver = os.path.normpath(driver)
    opts = Options()
    opts.binary_location = os.path.normpath(chrome)
    os.environ["webdriver.chrome.driver"] = chromeDriver
    driver = webdriver.Chrome(chromeDriver, chrome_options=opts)
    
    driver.maximize_window()
    # go to the google home page
    index = 'http://' + str(host) + ':' + str(port) + '/XOAM/login/index.html'
    driver.get(index)
    driver.find_element_by_id('loginUsername').clear()
    driver.find_element_by_id('loginUsername').send_keys(username)
    driver.find_element_by_id('loginPassword').clear()
    driver.find_element_by_id('loginPassword').send_keys(password)
    driver.find_element_by_id('submit').click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "ebBtnSearch")))
    return driver
    
def toAlarmManagement(driver):
    driver.find_element_by_xpath("//span[@class='ebBreadcrumbs-arrow']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ebBreadcrumbs-list']/ul/li[4]/a"))).click()
    
def toAlarmSyncPage(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ebBreadcrumbs']/div[2]/span"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ebBreadcrumbs']/div[2]/div/ul/li[2]"))).click()    
    
