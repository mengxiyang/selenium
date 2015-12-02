#encoding=utf-8
'''
Created on Nov 30, 2015

@author: lowitty
'''
import logging
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
import os, time, subprocess

# Create a new instance of the Firefox driver
#driver = webdriver.Firefox()
#C:\Users\EJLNOQC\Desktop\chromedriver
chromeDriver = os.path.normpath("C:\Users\EJLNOQC\Desktop\chromedriver.exe")
opts = Options()
opts.binary_location = "C:\\installed\\chrome\\chrome.exe"
os.environ["webdriver.chrome.driver"] = chromeDriver
driver = webdriver.Chrome(chromeDriver, chrome_options=opts)

driver.maximize_window()
# go to the google home page
driver.get("http://10.184.73.75:8686/XOAM/login/index.html")
driver.find_element_by_id('loginUsername').clear()
driver.find_element_by_id('loginUsername').send_keys('admin')
driver.find_element_by_id('loginPassword').clear()
driver.find_element_by_id('loginPassword').send_keys('Admin!@#123')
driver.find_element_by_id('submit').click()
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "ebBtnSearch")))


#ul = driver.find_element_by_xpath("//div[@class='ebBreadcrumbs-list']/ul/li[4]/a")
driver.find_element_by_xpath("//span[@class='ebBreadcrumbs-arrow']").click()
fm = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ebBreadcrumbs-list']/ul/li[4]/a")))
fm.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='table']/div/div/table/tbody")))
tbody = driver.find_element_by_xpath("//div[@class='table']/div/div/table/tbody")
trs = tbody.find_elements_by_xpath(".//tr")
trs = tbody.find_elements_by_xpath(".//tr")
for tr in trs:
    tds = tr.find_elements_by_xpath(".//td")
    if("未清除" == tds[5].get_attribute("innerHTML").encode('utf-8')):
        print "告警代码：" + tds[1].get_attribute("innerHTML").encode('utf-8') + " 未清除" 
#print len(trs)
#td = trs[0].find_elements_by_xpath(".//td")
#td0 = trs[0].find_element_by_xpath(".//td[1]")
#trs = tbody.find_elements_by_xpath(".//*")
#trs = tbody.find_elements_by_css_selector("*")
#print len(trs)
i = 1
'''fmManArrow = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ebBreadcrumbs']/div[2]/span")))
fmManArrow.click()
fmMan = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ebBreadcrumbs']/div[2]/div/ul/li[2]")))
fmMan.click()
manualSyncBtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idBtn-manual")))
manualSyncBtn.click()
confirmBtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ebDialogBox-actionBlock']/button[1]")))
confirmBtn.click()
driver.quit()'''
'''try:
    driver.quit()
except Exception as e:
    try:
        killCmd = "TASKKILL /IM chromedriver.exe /F"
        p = subprocess.Popen(killCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        p.kill()
    finally:
        pass'''