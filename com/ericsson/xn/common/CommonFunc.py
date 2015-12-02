#encoding=utf-8
'''
Created on Dec 2, 2015

@author: lowitty
'''
import os, platform, subprocess
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
    print index
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

#0 == 未清除
#1 == 已清除
#2 == 未确认
#3 == 已确认
def findLineOfCertainStatus(driver, status):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='table']/div/div/table/tbody")))
    tbody = driver.find_element_by_xpath("//div[@class='table']/div/div/table/tbody")
    trs = tbody.find_elements_by_xpath(".//tr")
    for tr in trs:
        tds = tr.find_elements_by_xpath(".//td")
        if(0 == status):
            if("未清除" == tds[5].get_attribute("innerHTML").encode('utf-8').strip()):
                print "告警代码：" + tds[1].get_attribute("innerHTML").encode('utf-8') + " 未清除" 
                return tr
        elif(2 == status):
            if("未确认" == tds[6].get_attribute("innerHTML").encode('utf-8').strip()):
                print "告警代码：" + tds[1].get_attribute("innerHTML").encode('utf-8') + " 未确认" 
                return tr
    return False

def clickTheCheckboxOftheTR(tr):
    if(not tr.find_element_by_xpath(".//td[1]/div/input").is_selected()):
        tr.find_element_by_xpath(".//td[1]/div/input").click()

#0 == 查询
#1 == 确认
#2 == 清除
#3 == SYNC
def findBtnReturnComfirmBtn(driver, btnClick):
    if(0 == btnClick):
        btnClickEle = driver.find_element_by_id("idBtn-search")
        return btnClickEle
    elif(1 == btnClick):
        btnClickEle = driver.find_element_by_id("idBtn-ack")
        btnClickEle.click()
        #ebDialogBox-actionBlock
        btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ebDialogBox-actionBlock']/button[1]")))
        return btn
    elif(2 == btnClick):
        btnClickEle = driver.find_element_by_id("idBtn-clear")
        btnClickEle.click()
        #ebDialogBox-actionBlock
        btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ebDialogBox-actionBlock']/button[1]")))
        return btn
    elif(3 == btnClick):
        #idBtn-manual
        btnClickEle = driver.find_element_by_id("idBtn-manual")
        btnClickEle.click()
        #ebDialogBox-actionBlock
        btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ebDialogBox-actionBlock']/button[1]")))
        return btn

def clickButton(btn):
    btn.click()

def alarmSync(chrome, driver, host, port = 8686, username = 'admin', password = 'Admin!@#123'):
    driver = loginToInterface(chrome, driver, host, port, username, password)
    toAlarmManagement(driver)
    toAlarmSyncPage(driver)
    btn = findBtnReturnComfirmBtn(driver, 3)
    return btn
    #clickButton(btn)
    #quitDriver(driver)
    
def alarmQuery(chrome, driver, host, port = 8686, username = 'admin', password = 'Admin!@#123'):
    driver = loginToInterface(chrome, driver, host, port, username, password)
    toAlarmManagement(driver)
    btn = findBtnReturnComfirmBtn(driver, 0)
    return btn
    
def alarmClear(chrome, driver, host, port = 8686, username = 'admin', password = 'Admin!@#123'):
    driver = loginToInterface(chrome, driver, host, port, username, password)
    toAlarmManagement(driver)
    tr = findLineOfCertainStatus(driver, 0)
    clickTheCheckboxOftheTR(tr)
    btn = findBtnReturnComfirmBtn(driver, 2)
    return btn
    
def alarmAck(chrome, driver, host, port = 8686, username = 'admin', password = 'Admin!@#123'):
    driver = loginToInterface(chrome, driver, host, port, username, password)
    toAlarmManagement(driver)
    tr = findLineOfCertainStatus(driver, 2)
    clickTheCheckboxOftheTR(tr)
    btn = findBtnReturnComfirmBtn(driver, 1)
    return btn
    
def foo(func, argv):
    func(argv)
    

def quitDriver(driver):
    try:
        driver.close()
        cmd = ''
        if('Windows' == platform.system()):
            cmd = 'TASKKILL /IM chromedriver.exe /F'
        elif('Darwin' == platform.system()):
            cmd = 'pkill chromedriver'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        p.kill()
    finally:
        pass