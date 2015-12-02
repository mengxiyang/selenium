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
fmManArrow = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ebBreadcrumbs']/div[2]/span")))
fmManArrow.click()
fmMan = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ebBreadcrumbs']/div[2]/div/ul/li[2]")))
fmMan.click()
manualSyncBtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idBtn-manual")))
manualSyncBtn.click()
confirmBtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ebDialogBox-actionBlock']/button[1]")))
confirmBtn.click()
driver.close()
try:
    driver.quit()
except Exception as e:
    try:
        killCmd = "TASKKILL /IM chromedriver.exe /F"
        p = subprocess.Popen(killCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        p.kill()
    finally:
        pass
    

#ul.click()
#driver.find_element_by_link_text(u"告警管理").click()

#driver.get("http://10.184.73.75:8686/XOAM/login/index.html#network-overview/fault-mgt/fault-sync")
#WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idBtn-manual")))
#driver.find_element_by_id('idBtn-manual').click()


'''# the page is ajaxy so the title is originally this:
print driver.title

# find the element that's name attribute is q (the google search box)
inputElement = driver.find_element_by_name("q")

# type in the search
inputElement.send_keys("cheese!")

# submit the form (although google automatically searches now without submitting)
inputElement.submit()

try:
    # we have to wait for the page to refresh, the last thing that seems to be updated is the title
    WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))

    # You should see "cheese! - Google Search"
    print driver.title

finally:
    driver.quit()'''