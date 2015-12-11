# encoding=utf-8
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
import logging, time
from __builtin__ import str
from selenium.common.exceptions import TimeoutException

logCommon = logging.getLogger('selenium.common')


def loginToInterface(isMac, chrome, driver, host, port=8686, username='admin', password='Admin!@#123'):
    logCommon.info('Will start web browser and perform test case.')
    chromeDriver = os.path.normpath(driver)
    logCommon.info('Browser driver path: ' + str(chromeDriver))
    os.environ["webdriver.chrome.driver"] = chromeDriver
    opts = Options()
    if (not isMac):
        opts = Options()
        opts.binary_location = os.path.normpath(chrome)
    else:
        opts.add_argument("--start-maximized")
    driver = webdriver.Chrome(chromeDriver, chrome_options=opts)
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


def toAlarmManagement(driver):
    logCommon.info('To the AlarmManagement page...')
    # driver.find_element_by_xpath("//span[@class='ebBreadcrumbs-arrow']").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='ebBreadcrumbs-arrow']"))).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='ebBreadcrumbs-list']/ul/li[4]/a"))).click()
    time.sleep(10)


def queryUnAcked(driver):
    # i_ack_status
    btnList = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='i_ack_status']/div/button")))
    btnList.click()
    checkUnAck = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='i_ack_status']/div/div/div[2]/label/input")))
    if (not checkUnAck.is_selected()):
        checkUnAck.click()
        btnList.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idBtn-search"))).click()


def toAlarmSyncPage(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='ebBreadcrumbs']/div[2]/span"))).click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='ebBreadcrumbs']/div[2]/div/ul/li[2]"))).click()


# 0 == 未清除
# 1 == 已清除
# 2 == 未确认
# 3 == 已确认
def findLineOfCertainStatus(driver, status):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='table']/div/div/table/tbody")))
    except TimeoutException as e:
        logCommon.error('None unacked records in the table.')
    tbody = driver.find_element_by_xpath("//div[@class='table']/div/div/table/tbody")
    trs = WebDriverWait(tbody, 10).until(EC.presence_of_all_elements_located((By.XPATH, ".//tr")))
    # trs = tbody.find_elements_by_xpath(".//tr")
    for tr in trs:
        # tds = tr.find_elements_by_xpath(".//td")
        tds = WebDriverWait(tr, 10).until(EC.presence_of_all_elements_located((By.XPATH, ".//td")))
        if (0 == status):
            if ("未清除" == tds[5].get_attribute("innerHTML").encode('utf-8').strip()):
                print "告警代码：" + tds[1].get_attribute("innerHTML").encode('utf-8') + " 未清除"
                return tr
        elif (2 == status):
            if ("未确认" == tds[6].get_attribute("innerHTML").encode('utf-8').strip()):
                # print "告警代码：" + tds[1].get_attribute("innerHTML").encode('utf-8') + " 未确认"
                logCommon.info("ID: " + str(tds[1].get_attribute("innerHTML").encode('utf-8')) + " not acked")
                return tr
        elif (4 == status):
            if ("未确认" == tds[6].get_attribute("innerHTML").encode('utf-8').strip() and "未清除" == tds[5].get_attribute(
                    "innerHTML").encode('utf-8').strip()):
                print "告警代码：" + tds[1].get_attribute("innerHTML").encode('utf-8') + " 未确认并且未清除"
                return tr
    return False


def clickTheCheckboxOftheTR(tr):
    logCommon.info('Check the CheckBox...')
    if (not tr.find_element_by_xpath(".//td[1]/div/input").is_selected()):
        tr.find_element_by_xpath(".//td[1]/div/input").click()


# 0 == 查询
# 1 == 确认
# 2 == 清除
# 3 == SYNC
def findBtnReturnComfirmBtn(driver, btnClick):
    if (0 == btnClick):
        # btnClickEle = driver.find_element_by_id("idBtn-search")
        btnClickEle = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idBtn-search")))
        return btnClickEle
    elif (1 == btnClick):
        # btnClickEle = driver.find_element_by_id("idBtn-ack")
        logCommon.info('Click ACK button')
        btnClickEle = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idBtn-ack")))
        btnClickEle.click()
        # ebDialogBox-actionBlock
        btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='ebDialogBox-actionBlock']/button[1]")))
        logCommon.info('Found the confirm button and will click next.')
        return btn
    elif (2 == btnClick):
        # btnClickEle = driver.find_element_by_id("idBtn-clear")
        btnClickEle = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idBtn-clear")))
        btnClickEle.click()
        # ebDialogBox-actionBlock
        btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='ebDialogBox-actionBlock']/button[1]")))
        return btn
    elif (3 == btnClick):
        # idBtn-manual
        # btnClickEle = driver.find_element_by_id("idBtn-manual")
        btnClickEle = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idBtn-manual")))
        btnClickEle.click()
        # ebDialogBox-actionBlock
        btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='ebDialogBox-actionBlock']/button[1]")))
        return btn


def clickButton(btn):
    btn.click()


def checkAcked(tr, dt, driver, filePath):
    time.sleep(5)
    # tds = tr.find_elements_by_xpath(".//td")
    tds = WebDriverWait(tr, 10).until(EC.presence_of_all_elements_located((By.XPATH, ".//td")))
    # tds[5].get_attribute("innerHTML").encode('utf-8').strip()
    if ("已确认" == tds[6].get_attribute("innerHTML").encode('utf-8').strip()):
        logCommon.info('Success: ACK the alarm successfully, ID: ' + tds[1].get_attribute("innerHTML").encode(
            'utf-8') + ', ACK time: ' + tds[12].get_attribute("innerHTML").encode('utf-8'))
    else:
        logCommon.critical('Failed: ACK the alarm failed.')

    '''logCommon.info(filePath + 'acked_0.png')
    if(os.path.isfile(filePath + 'acked_0.png')):
        os.remove(filePath + 'acked_0.png')
    driver.save_screenshot(filePath + 'acked_0.png')'''

    snap_1 = os.path.normpath(filePath + os.path.sep + 'acked_1.png')
    driver.execute_script("arguments[0].scrollIntoView(true);", tds[12])
    if (os.path.isfile(snap_1)):
        os.remove(snap_1)
    driver.save_screenshot(snap_1)


def alarmSync(isMac, chrome, driver, host, port=8686, username='admin', password='Admin!@#123'):
    driver = loginToInterface(isMac, chrome, driver, host, port, username, password)
    toAlarmManagement(driver)
    toAlarmSyncPage(driver)
    btn = findBtnReturnComfirmBtn(driver, 3)
    return btn
    # clickButton(btn)
    # quitDriver(driver)


def alarmQuery(isMac, chrome, driver, host, port=8686, username='admin', password='Admin!@#123'):
    driver = loginToInterface(isMac, chrome, driver, host, port, username, password)
    toAlarmManagement(driver)
    btn = findBtnReturnComfirmBtn(driver, 0)
    return btn


def alarmClear(isMac, chrome, driver, host, port=8686, username='admin', password='Admin!@#123'):
    driver = loginToInterface(isMac, chrome, driver, host, port, username, password)
    toAlarmManagement(driver)
    tr = findLineOfCertainStatus(driver, 4)
    clickTheCheckboxOftheTR(tr)
    btn = findBtnReturnComfirmBtn(driver, 2)
    return btn


def alarmAck(isMac, chrome, driver, host, port=8686, username='admin', password='Admin!@#123'):
    driver = loginToInterface(isMac, chrome, driver, host, port, username, password)
    toAlarmManagement(driver)
    tr = findLineOfCertainStatus(driver, 4)
    # tr = findLineOfCertainStatus(driver, 0)
    clickTheCheckboxOftheTR(tr)
    btn = findBtnReturnComfirmBtn(driver, 1)
    return btn


def foo(func, argv):
    func(argv)


def quitDriver(driver):
    try:
        driver.close()
        cmd = ''
        if ('Windows' == platform.system()):
            cmd = 'TASKKILL /IM chromedriver.exe /F'
        elif ('Darwin' == platform.system()):
            cmd = 'pkill chromedriver'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        p.kill()
    finally:
        pass
