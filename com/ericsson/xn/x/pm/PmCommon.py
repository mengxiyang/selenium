# -*- coding: utf-8 -*-


import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def find_single_widget(driver, wait_time, list_identifier):
    return WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(list_identifier))


def to_pm_management_page(driver, logger):
    logger.info('To the PmManagement page...')

    identifier = (By.XPATH, "//div[@class='ebLayout-Navigation']/div/div[1]/span")
    find_single_widget(driver, 10, identifier).click()

    identifier = (By.XPATH, "//div[@class='ebBreadcrumbs-list']/ul/li[3]/a")
    find_single_widget(driver, 10, identifier).click()


def to_tab_by_ne_type(driver, ne_type, logger):
    ne_type = ne_type.strip().upper()
    tab_index = 1
    if 'PGW' == ne_type:
        tab_index = 1
    elif 'SGW' == ne_type:
        tab_index = 2
    elif 'SGSN' == ne_type:
        tab_index = 3
    elif 'MME' == ne_type:
        tab_index = 4
    elif 'SBC' == ne_type:
        tab_index = 5
    elif 'OCGAS' == ne_type:
        tab_index = 6

    identifier = (By.XPATH, "//div[@class='ebTabs-tabArea']/div[" + str(tab_index) + "]")
    find_single_widget(driver, 10, identifier).click()

    # wait for the notification, maximum 10 seconds
    identifier = (By.XPATH, "//div[@class='noti']/div")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(identifier))


def init_and_search(driver, logger, ne_name, end_time, start_time=None):
    # select the given nename
    identifier = (By.XPATH, "//div[@class='eaContainer-applicationHolder']/div[1]/div[2]/div[1]/div[2]/input")
    find_single_widget(driver, 10, identifier).click()

    id_table_candidate = (By.XPATH, "//div[@class='ebLayout-candidateEnbs'/div[2]/div/div[3]/div/div/div/table")
    table_candidate = find_single_widget(driver, 10, id_table_candidate)

    id_input_search = (By.XPATH, ".//thead/tr[2]/th[2]/input")
    find_single_widget(table_candidate, 10, id_input_search).send_keys(ne_name.strip())
    time.sleep(1.0)

    id_checkbox = (By.XPATH, ".//tbody/tr[1]/td[1]/div/div/input")
    left_checkbox = find_single_widget(table_candidate, 10, id_checkbox)
    if not left_checkbox.is_selected():
        left_checkbox.click()

    # select to right
    id_arrow_to_right = (By.ID, "btnRight")
    find_single_widget(driver, 10, id_arrow_to_right).click()
    time.sleep(1.0)

    # close select ne dialog
    id_btn_choose_ne = (By.CLASS_NAME, "choose")
    find_single_widget(driver, 10, id_btn_choose_ne).click()

    # select the correct time
    id_end_time = (By.XPATH, "//div[@class='endtime']/div/span/input")
    find_single_widget(driver, 10, id_end_time).click()
    set_time_for_query(driver, logger, end_time)

    if start_time is not None:
        id_start_time = (By.XPATH, "//div[@class='starttime']/div/span/input")

    # click the query button
    id_query_btn = (By.ID, "idBtn-search")
    find_single_widget(driver, 10, id_query_btn).click()

    # wait for the notification, maximum 20 seconds
    identifier = (By.XPATH, "//div[@class='noti']/div")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(identifier))


def check_pm_rows(driver, logger, num_rows, ne_type, dict_counters, rows_of_page=10):
    id_table = (By.XPATH, "//div[@class='ebTabs']/div[2]/div/div/div/div/table")
    table = find_single_widget(driver, 10, id_table)
    for i in range(1, num_rows + 1):
        check_pm_by_row(driver, table, logger, i, ne_type, dict_counters, rows_of_page)


def check_pm_by_row(driver, table, logger, index_row, ne_type, dict_counters, rows_of_page):
    logger.info('Start to check row: ' + str(index_row))
    bool_row = True
    try:
        id_tr = (By.XPATH, ".//tbody/tr[" + str(index_row) + "]")
        tr = find_single_widget(table, 10, id_tr)

    except Exception as e:
        logger.error("Test failed, ERROR: " + str(e))
        bool_row = False
    return bool_row


def set_time_for_query(driver, logger, date_time):
    # first edition will only set the time part
    id_time_holder = (By.CLASS_NAME, "ebTimePicker")
    time_holder = find_single_widget(driver, 10, id_time_holder)

    id_hour = (By.XPATH, ".//table[1]/tbody/tr/td[2]/div[2]/input")
    find_single_widget(time_holder, 10, id_hour).send_keys(date_time.hour)

    id_minute = (By.XPATH, ".//table[2]/tbody/tr/td[2]/div[2]/input")
    find_single_widget(time_holder, 10, id_minute).send_keys(date_time.minute)

    id_second = (By.XPATH, ".//table[3]/tbody/tr/td[2]/div[2]/input")
    find_single_widget(time_holder, 10, id_second).send_keys(date_time.second)

    id_ok_btn = (By.XPATH, "//div[@class='ebDialogBox-actionBlock']/button[1]")
    find_single_widget(driver, 10, id_ok_btn).click()
