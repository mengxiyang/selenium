# encoding=utf-8
'''
Created on Dec 2, 2015

@author: lowitty
'''
import os, platform, subprocess
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from com.ericsson.xn.commons import test_logger as logCommon
from com.ericsson.xn.commons.funcutils import find_single_widget, find_all_widgets
import datetime as pydate
import time
from com.ericsson.xn.commons.PyProperties import Properties

def data_init(ne_info_cfg,server_info_cfg):
    server_info = Properties(server_info_cfg)
    dict_browser_chrome = {
        "browser_type": server_info.getProperty('browser_type'),
        "browser_path": server_info.getProperty('browser_path'),
        "driver_path": server_info.getProperty('driver_path')
    }
    
    dict_server_info = {                
    "host":server_info.getProperty("host"),
    "username": server_info.getProperty("username"),
    "password": server_info.getProperty("password"),
    "port" : server_info.getProperty("port"),
    "url" : server_info.getProperty("url"),
    "preurl" : server_info.getProperty("preurl")
    }
    
    ne_info = Properties(ne_info_cfg)
    dict_ne_info  = {
        "ne_name": ne_info.getProperty("ne_name"),
        "ne_user": ne_info.getProperty("ne_user"),
        "ne_type": ne_info.getProperty("ne_type"),
        "ne_ip" : ne_info.getProperty("ne_ip"),
        "ne_password" : ne_info.getProperty("ne_password"),
        "pm_path": ne_info.getProperty("pm_path"),
        "log_path": ne_info.getProperty("log_path"),
        "alarm_path": ne_info.getProperty("alarm_path"),
        "ne_port": ne_info.getProperty("ne_port"),
        "sftp_port": ne_info.getProperty("sftp_port"),
        "sftp_user": ne_info.getProperty("sftp_user"),
        "sftp_password": ne_info.getProperty("sftp_password"),
        "snmp_port": ne_info.getProperty("snmp_port"),
        "usm_user": ne_info.getProperty("usm_user"),
        "auth_password": ne_info.getProperty("auth_password"),
        "priv_password": ne_info.getProperty("priv_password"),
        "app_user": ne_info.getProperty("app_user"),
        "app_password": ne_info.getProperty("app_password"),
        "li_pwd": ne_info.getProperty("li_pwd"),
        "fro_id": ne_info.getProperty("fro_id"),
        "engine_id":ne_info.getProperty("engineId")
    }

    return dict_ne_info,dict_server_info,dict_browser_chrome
    


def toAlarmManagement(driver):
    logCommon.info('To the AlarmManagement page...')
    # driver.find_element_by_xpath("//span[@class='ebBreadcrumbs-arrow']").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='ebBreadcrumbs-arrow']"))).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='ebBreadcrumbs-list']/ul/li[4]/a"))).click()
    time.sleep(10)

def toAlarmManagement_by_url(driver,server_info,url_add = "#network-overview/fault-mgt/fault-management"):
    logCommon.info("To the AlarmManagement page...")
    url="http://" + server_info.getProperty("host") + ":" + str(server_info.getProperty("port")) + server_info.getProperty("preurl") + url_add
    logCommon.info("The AlarmMgt URL is: " + url)
    driver.get(url)
    logCommon.info("Login AlarmManagement page successfully")


def init_and_search(driver,nename):
    logCommon.info("Query alarm for NE: " + nename + "...")
    selected_given_nename(driver,nename)
    search_btn = find_single_widget(driver, 10, (By.XPATH,"//button[@id='idBtn-search']"))
    search_btn.click()
    tips = find_single_widget(driver,10,(By.XPATH,"//div[@class='tip']")).get_attribute('innerHTML').encode('utf-8')
    if tips:
        logCommon.info("Alarm queried successfully")

def send_an_alarm(host,ne_type,alarm_type):
    logCommon.info("Send alarm: " + ne_type + ":" + alarm_type)
    return {"alarmLevel":2,"timeStamp":"2016-03-04 16:18:58","alarmSource":"licId01","alarmCategory":3,"alarmDescription":"Cannot connect to X2 remote address. remote ip [192.168.20.10] port [7790]. errno [67] error description [Address already in use]"}


def fetch_alarm_on_gui(driver,ne_type,alarm_trap,mappingInstance,alarm_type):
    nowtime=pydate.datetime.now()
    endtime=nowtime + pydate.timedelta(seconds=30)
    id_button=(By.XPATH,"//button[@id='idBtn-search']")
    search_button=find_single_widget(driver,10,id_button)
    while(pydate.datetime.now()< endtime):
        search_button.click()
        try:
            alarm_data=get_1st_row_on_gui(driver)
        except TimeoutException:
            time.sleep(5)
            continue

        if ne_type in  ('OCGAS','GMLC'):
            specific_problem = mappingInstance.get_property("specific_problem")[alarm_type]
        else:
            specific_problem = alarm_trap["specificProblem"]
        if(specific_problem == alarm_data["问题描述"]):
            logCommon.info("alarm received on GUI:" + alarm_type)
            return alarm_data
        else:
            time.sleep(10)
    return None


def query_alarm(driver):
    search_btn = find_single_widget(driver, 10, (By.XPATH,"//button[@id='idBtn-search']"))
    search_btn.click()


def get_1st_row_on_gui(driver):
    table_i = (By.XPATH,"//div[@class='table']/div/div/table[@class='ebTable elWidgets-Table-body']")
    table=find_single_widget(driver,10,table_i)

    name_i=(By.XPATH,"./thead/tr/th")
    column_name = find_all_widgets(table,10,name_i)

    value_i = (By.XPATH,"./tbody/tr[1]/td")
    find_single_widget(table,10,value_i).click()
    column_value = find_all_widgets(table,10,value_i)

    name_list=[]
    value_list=[]

    if(len(column_name) != len(column_value)):
        logCommon.error("Alarm data mismatched on gui")

    for name in column_name:
        alarm_name = name.text.encode('utf-8')
        name_list.append(alarm_name)
    del name_list[0]

    for value in column_value:
        filed_value = value.text.encode('utf-8')
        value_list.append(filed_value)
    del value_list[0]

    alarm_gui=dict(zip(name_list,value_list))
    del alarm_gui["告警代码"]
    del alarm_gui["类型代码"]
    del alarm_gui["类型编号"]
    return alarm_gui


def selected_given_nename(driver,nename):
    ne_param = find_single_widget(driver,10,(By.XPATH,"//input[@class='ebInputNe']"))
    if ne_param.get_attribute('value'):
        ne_param.click()
        find_single_widget(driver, 10, (By.XPATH,"//div[@id='btnAllLeft']")).click()
    else:
        ne_param.click()
        
    input_ne = find_single_widget(driver,10,(By.XPATH,"//table[@class='ebTable elWidgets-Table-body']/thead/tr[2]/th[2]/input"))
    input_ne.clear()
    input_ne.send_keys(nename)
    time.sleep(1)
    
    found_ne=find_single_widget(driver, 10, (By.XPATH,"//table[@class='ebTable elWidgets-Table-body']/tbody/tr"))
    
    if found_ne:
        ne_check_box = find_single_widget(found_ne, 10, (By.XPATH,"./td/div/div/input"))
        if not ne_check_box.is_selected():
            ne_check_box.click()
    else:
        logCommon.error("the given nename: " + nename + " not found")
    
    right_arrow = find_single_widget(driver, 10,(By.XPATH,"//div[@id='btnRight']"))
    right_arrow.click()
    
    confirm_btn = find_single_widget(driver,10,(By.XPATH,"//div[@class='choose']/button"))
    confirm_btn.click()



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


# 0 == ��???
# 1 == ?????
# 2 == ��???
# 3 == ?????
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
            if ("��???" == tds[5].get_attribute("innerHTML").encode('utf-8').strip()):
                print "?��????" + tds[1].get_attribute("innerHTML").encode('utf-8') + " ��???"
                return tr
        elif (2 == status):
            if ("��???" == tds[6].get_attribute("innerHTML").encode('utf-8').strip()):
                # print "?��????" + tds[1].get_attribute("innerHTML").encode('utf-8') + " ��???"
                logCommon.info("ID: " + str(tds[1].get_attribute("innerHTML").encode('utf-8')) + " not acked")
                return tr
        elif (4 == status):
            if ("��???" == tds[6].get_attribute("innerHTML").encode('utf-8').strip() and "��???" == tds[5].get_attribute(
                    "innerHTML").encode('utf-8').strip()):
                print "?��????" + tds[1].get_attribute("innerHTML").encode('utf-8') + " ��??????��???"
                return tr
    return False


def clickTheCheckboxOftheTR(tr):
    logCommon.info('Check the CheckBox...')
    if (not tr.find_element_by_xpath(".//td[1]/div/input").is_selected()):
        tr.find_element_by_xpath(".//td[1]/div/input").click()


# 0 == ???
# 1 == ???
# 2 == ???
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
    if ("?????" == tds[6].get_attribute("innerHTML").encode('utf-8').strip()):
        logCommon.info('Success: ACK the alarm successfully, ID: ' + tds[1].get_attribute("innerHTML").encode(
            'utf-8') + ', ACK time: ' + tds[12].get_attribute("innerHTML").encode('utf-8'))
    else:
        logCommon.error('Failed: ACK the alarm failed.')

    '''logCommon.info(filePath + 'acked_0.png')
    if(os.path.isfile(filePath + 'acked_0.png')):
        os.remove(filePath + 'acked_0.png')
    driver.save_screenshot(filePath + 'acked_0.png')'''

    snap_1 = os.path.normpath(filePath + os.path.sep + 'acked_1.png')
    driver.execute_script("arguments[0].scrollIntoView(true);", tds[12])
    if (os.path.isfile(snap_1)):
        os.remove(snap_1)
    driver.save_screenshot(snap_1)


def alarmSync(driver):
    toAlarmManagement(driver)
    toAlarmSyncPage(driver)
    btn = findBtnReturnComfirmBtn(driver, 3)
    return btn
    # clickButton(btn)
    # quitDriver(driver)


def alarmQuery(driver):
    toAlarmManagement(driver)
    btn = findBtnReturnComfirmBtn(driver, 0)
    return btn


def alarmClear(driver):
    toAlarmManagement(driver)
    tr = findLineOfCertainStatus(driver, 4)
    clickTheCheckboxOftheTR(tr)
    btn = findBtnReturnComfirmBtn(driver, 2)
    return btn


def alarmAck(driver):
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
