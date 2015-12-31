# -*- coding: utf-8 -*-


import time
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from com.ericsson.xn.commons.funcutils import find_single_widget


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
    try:
        identifier = (By.XPATH, "//div[@class='noti']/div")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(identifier))
    except TimeoutException:
        pass


def init_and_search(driver, logger, ne_name, end_time, start_time=None):
    # select the given nename
    select_given_ne_name(driver, logger, ne_name)

    # select the correct time
    id_end_time = (By.XPATH, "//div[@class='endtime']/div/span/input")
    find_single_widget(driver, 10, id_end_time).click()
    set_time_for_query(driver, logger, end_time)

    if start_time is not None:
        id_start_time = (By.XPATH, "//div[@class='starttime']/div/span/input")
        find_single_widget(driver, 10, id_start_time).click()
        set_time_for_query(driver, logger, start_time)

    # click the query button
    id_query_btn = (By.ID, "idBtn-search")
    find_single_widget(driver, 10, id_query_btn).click()

    # wait for the notification, maximum 20 seconds
    id_body_date = (By.XPATH, "//div[@class='ebTabs']/div[2]/div/div/div/div/table/tbody")
    find_single_widget(driver, 20, id_body_date)


def wait_until_pm_date_show_up(driver, logger, wait_time, ne_name, interval=1):
    select_given_ne_name(driver, logger, ne_name)
    end_time = datetime.now() + timedelta(seconds=wait_time)
    while datetime.now() < end_time:
        id_query_btn = (By.ID, "idBtn-search")
        find_single_widget(driver, 10, id_query_btn).click()
        id_body_date = (By.XPATH, "//div[@class='ebTabs']/div[2]/div/div/div/div/table/tbody")
        try:
            find_single_widget(driver, 10, id_body_date)
            return True
        except TimeoutException:
            pass
    return False


def select_given_ne_name(driver, logger, ne_name):
    identifier = (By.XPATH, "//div[@class='eaContainer-applicationHolder']/div[1]/div[3]/div[2]/div[1]/div[2]/input")
    input_ne_name = find_single_widget(driver, 10, identifier)
    if not '' == input_ne_name.get_attribute('value').strip():
        input_ne_name.click()
        find_single_widget(driver, 10, (By.ID, "btnAllLeft")).click()
    else:
        input_ne_name.click()

    id_table_candidate = (By.XPATH, "//div[@class='ebLayout-candidateEnbs']/div[2]/div/div[3]/div/div/div/table")
    table_candidate = find_single_widget(driver, 20, id_table_candidate)

    id_input_search = (By.XPATH, ".//thead/tr[2]/th[2]/input")
    candi_input = find_single_widget(table_candidate, 10, id_input_search)
    candi_input.clear()
    candi_input.send_keys(ne_name.strip())
    time.sleep(1.0)

    id_checkbox = (By.XPATH, ".//tbody/tr[1]/td[1]/div/div/input")
    left_checkbox = find_single_widget(table_candidate, 10, id_checkbox)
    if not left_checkbox.is_selected():
        left_checkbox.click()

    # select to right
    id_arrow_to_right = (By.ID, "btnRight")
    find_single_widget(driver, 10, id_arrow_to_right).click()
    # time.sleep(5.0)

    # close select ne dialog
    id_btn_choose_ne = (By.CLASS_NAME, "choose")
    find_single_widget(driver, 10, id_btn_choose_ne).click()
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable(id_btn_choose_ne))


def check_pm_rows(driver, logger, num_rows, ne_type, dict_counters, rows_of_page=10):
    bool_overall = True
    id_table = (By.XPATH, "//div[@class='ebTabs']/div[2]/div/div/div/div/table")
    # table = find_single_widget(driver, 10, id_table)
    for i in range(1, num_rows + 1):
        bool_row = check_pm_by_row(driver, id_table, logger, i, ne_type, dict_counters, rows_of_page)
        if not bool_row:
            bool_overall = False
            logger.error('Row ' + str(i) + " check FAILED. Check the log for detailed information.")
        else:
            logger.info('Row ' + str(i) + " check PASSED.")

    if bool_overall:
        logger.info("Overall PASSED.")
    else:
        logger.error("Overall FAILED.")


def check_pm_by_row(driver, id_table, logger, index_row, ne_type, dict_counters, rows_of_page):
    logger.info('Start to check row: ' + str(index_row))
    if index_row > rows_of_page:
        to_second_page(driver, logger)

    bool_row = True
    try:
        if index_row > rows_of_page:
            gui_index_row = index_row - rows_of_page
        else:
            gui_index_row = index_row
        id_tr = (By.XPATH, ".//tbody/tr[" + str(gui_index_row) + "]")
        table = find_single_widget(driver, 10, id_table)
        tr = find_single_widget(table, 10, id_tr)
        gui_str_time = find_single_widget(tr, 10, (By.XPATH, ".//td[2]")).get_attribute('innerHTML').encode('utf-8')
        gui_time = datetime.strptime(gui_str_time.strip(), "%Y-%m-%d %H:%M")
        list_row = dict_counters[str(gui_time.minute)].split(',')
        for i in range(len(list_row)):
            try:
                id_counter = (By.XPATH, ".//td[" + str(i + 4) + "]")
                gui_counter = find_single_widget(tr, 5, id_counter).get_attribute('innerHTML').encode('utf-8')
                i_gui_counter = int(gui_counter)
            except Exception as e:
                i_gui_counter = None
            if int(list_row[i]) == i_gui_counter:
                logger.info("Row " + str(index_row) + ", GUI Time: " + gui_str_time.strip() + ", Counter " + str(i + 1)
                            + " is: " + str(i_gui_counter) + ", PASSED.")
            else:
                bool_row = False
                logger.error("Row " + str(index_row) + ", GUI Time: " + gui_str_time.strip() + ", Counter " + str(i + 1)
                             + ", FAILED. Expected: " + str(list_row[i]) + ", GUI is: " + str(gui_counter))

    except Exception as e:
        logger.error("Test failed, ERROR: " + str(e))
        bool_row = False
    return bool_row


def to_second_page(driver, logger):
    id_next_page = (By.XPATH, "//div[@class='page']/ul/li[3]")
    pager = find_single_widget(driver, 10, id_next_page)
    # driver.execute_script("arguments[0].scrollIntoView(true);", tds[12])
    driver.execute_script("arguments[0].scrollIntoView(true);", pager)
    pager.click()
    # wait for the notification, maximum 10 seconds
    id_body_date = (By.XPATH, "//div[@class='ebTabs']/div[2]/div/div/div/div/table/tbody")
    find_single_widget(driver, 10, id_body_date)


def set_time_for_query(driver, logger, date_time):
    # first edition will only set the time part
    id_time_holder = (By.XPATH, "//div[@data-namespace='ebTimePicker']")
    time_holder = find_single_widget(driver, 10, id_time_holder)

    id_hour = (By.XPATH, ".//table[1]/tbody/tr/td[2]/div[2]/input")
    hour_input = find_single_widget(time_holder, 10, id_hour)
    hour_input.clear()
    hour_input.send_keys(date_time.hour)

    id_minute = (By.XPATH, ".//table[2]/tbody/tr/td[2]/div[2]/input")
    minute_input = find_single_widget(time_holder, 10, id_minute)
    minute_input.clear()
    minute_input.send_keys(date_time.minute)

    id_second = (By.XPATH, ".//table[3]/tbody/tr/td[2]/div[2]/input")
    second_input = find_single_widget(time_holder, 10, id_second)
    second_input.clear()
    # second_input.send_keys(date_time.second)
    second_input.send_keys(0)

    id_ok_btn = (By.XPATH, "//div[@class='ebDialogBox-actionBlock']/button[1]")
    find_single_widget(driver, 10, id_ok_btn).click()
