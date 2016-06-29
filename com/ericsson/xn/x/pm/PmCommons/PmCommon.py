# -*- coding: utf-8 -*-


import time
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from com.ericsson.xn.commons.funcutils import find_single_widget, find_all_widgets, \
    ne_category_by_ne_type, get_widget_ignore_refrence_error
from com.ericsson.xn.commons import test_logger as test
from com.ericsson.xn.commons.selfutils import compare_lists


def to_pm_management_page(driver):
    '''
    This function has been abandoned.
    :param driver:
    :return:
    '''
    test.info('To the PmManagement page...')

    identifier = (By.XPATH, "//div[@class='ebLayout-Navigation']/div/div[1]/span")
    find_single_widget(driver, 10, identifier).click()

    identifier = (By.XPATH, "//div[@class='ebBreadcrumbs-list']/ul/li[3]/a")
    find_single_widget(driver, 10, identifier).click()


def check_in_correct_pm_page(driver):
    '''
    This function works on the beginning editions and has been abandoned.
    :param driver:
    :return:
    '''
    id_search_btn = (By.ID, "idBtn-search")
    b_validate = False
    try:
        find_single_widget(driver, 10, id_search_btn)
        b_validate = True
    except TimeoutException as e:
        # page not loaded
        return False
    if b_validate:
        # check if in the correct page
        # id_navi = identifier = (By.XPATH, "//div[@class='ebLayout-Navigation']/div")
        # navi = find_single_widget(driver, 10, id_navi)
        id_divs = identifier = (By.XPATH, "//div[@class='ebLayout-Navigation']/div/div")
        children_divs = find_all_widgets(driver, 20, id_divs)
        str_last_navi = find_single_widget(children_divs[-1], 10, (By.XPATH, ".//a")).get_attribute('innerHTML').\
            encode('utf-8').strip()
        # logger.info(children_divs[-2].get_attribute('innerHTML').encode('utf-8'))
        lis = find_all_widgets(children_divs[-2], 10, (By.XPATH, ".//div/ul/li"))
        for li in lis:
            str_a_li = find_single_widget(li, 10, (By.XPATH, ".//a")).get_attribute('innerHTML').encode('utf-8').strip()
            if str_last_navi == str_a_li:
                return True
        # current page not in parent navigation
        return False


def to_pm_management_page_by_url(driver, ne_type, server_info, to_url_pre='#network-overview/pm-management/'):
    test.info('Will Navigate to the PMManagement page...')
    base_url = 'http://' + server_info.getProperty('host') + ':' + str(server_info.getProperty('port')) + \
               server_info.getProperty('preurl')
    test.info('Base URL is: ' + base_url)
    to_url = base_url + (to_url_pre + 'pm-' + ne_category_by_ne_type(ne_type) + '/' + 'pm-' + ne_type).lower()
    test.info('To URL: ' + to_url)
    driver.get(to_url)
    make_sure_in_pm_page(driver)


def make_sure_in_pm_page(driver):
    # btn id: ebBtnSearch
    id_btn_interface = (By.ID, 'ebBtnSearch')
    try:
        find_single_widget(driver, 5, id_btn_interface)
        test.error('Page redirect to the interface management page, critical error!')
    except TimeoutException:
        id_query_btn = (By.ID, "idBtn-search")
        try:
            pm_query_btn = find_single_widget(driver, 10, id_query_btn)
            if pm_query_btn:
                test.passed('Found the query button of PM Management page, check passed.')
        except TimeoutException:
            test.failed('Cannot find the query button of PM Management page.')


def make_in_correct_tab(driver, prefix, postfix):
    id_tabs = (By.XPATH, "//div[@class='ebTabs']/div[1]/div[2]/div")
    tabs = find_all_widgets(driver, 10, id_tabs)
    for tab in tabs:
        if prefix + postfix == tab.get_attribute('innerHTML').encode('utf-8').strip():
            if not tab.get_attribute('class').encode('utf-8').find('ebTabs-tabItem_selected_true') > -1:
                tab.click()
                wait_noti_widget_show(driver)
                test.info('Now in TAB: ' + prefix + postfix)


def wait_noti_widget_show(driver, wait_time=10):
    id_div = (By.XPATH, "//div[@class='noti']/div")
    try:
        find_single_widget(driver, wait_time, id_div)
        test.info('Query result notification shown up.')
    except TimeoutException:
        test.warning('Query result notification did not shown up, case may or may not fail later.')


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


def init_and_search(driver, ne_name, end_time=None, start_time=None):
    # select the given nename
    select_given_ne_name(driver, ne_name)

    # select the correct time
    if end_time is not  None:
        test.info('Query end time point set to: ' + end_time.strftime('%H%M%S'))
        id_end_time = (By.XPATH, "//div[@class='endtime']/div/span/input")
        find_single_widget(driver, 10, id_end_time).click()
        set_time_for_query(driver, end_time)

    if start_time is not None:
        test.info('Query start time point set to: ' + start_time.strftime('%H%M%S'))
        id_start_time = (By.XPATH, "//div[@class='starttime']/div/span/input")
        find_single_widget(driver, 10, id_start_time).click()
        set_time_for_query(driver, start_time)

    # click the query button
    id_query_btn = (By.ID, "idBtn-search")
    find_single_widget(driver, 10, id_query_btn).click()

    # wait for the notification, maximum 20 seconds
    id_body_date = (By.XPATH, "//div[@class='ebTabs']/div[2]/div/div/div/div/table/tbody")
    find_single_widget(driver, 20, id_body_date)


def wait_until_pm_date_show_up(driver, ne_name, wait_time=720):
    select_given_ne_name(driver, ne_name)
    end_time = datetime.now() + timedelta(seconds=wait_time)
    while datetime.now() < end_time:
        id_query_btn = (By.ID, "idBtn-search")
        find_single_widget(driver, 10, id_query_btn).click()
        id_body_date = (By.XPATH, "//div[@class='ebTabs']/div[2]/div/div/div/div/table/tbody")
        try:
            find_single_widget(driver, 10, id_body_date)
            test.passed('Successfully found the counters data.')
            return
        except TimeoutException:
            pass
    test.error('Wait for ' + str(wait_time) + ' seconds but cannot find any PM datas.')


def select_given_ne_name(driver, ne_name):
    identifier = (By.XPATH, "//div[@class='pmcommonarea']/div/div[2]/div[1]/div[2]/input")
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


def wait_until_rounds_ok(driver, rows, rows_of_page, rows_each_period):
    '''
    This function will check the number of rows that we need to check the PM.
    :param driver:
    :param rows:
    :param rows_of_page:
    :param dict_additional:
    :param ne_type:
    :return: None
    '''
    id_tbdoy_trs = (By.XPATH, "//div[@class='ebTabs']/div[2]/div/div/div/div/table/tbody/tr")
    # if dict_additional.has_key('check_rows'):
    #    rows = dict_additional['check_rows']

    # if not 0 == rows % dict_additional['number_of_lic']:
    #    test.error('Number of checked rows should be integer multiples of number of LICs.')
    t_start = datetime.now()
    # Note that most of the PM need T2-T1, for Node like SBC, we may wait 5 minutes more since SBC don't need T2-T1
    # t_end = t_start + timedelta(minutes=5 * (rows // dict_additional['number_of_lic'] + 1) + 2)
    t_end = t_start + timedelta(minutes=5 * (rows // rows_each_period + 1) + 2)
    while datetime.now() < t_end:
        # click the query button
        id_query_btn = (By.ID, "idBtn-search")
        find_single_widget(driver, 10, id_query_btn).click()
        time.sleep(.1)
        try:
            i_page = rows / rows_of_page
            tgt_page_number = i_page if 0 == rows % rows_of_page else i_page + 1
            id_tgt_pager = (By.XPATH, ("//div[@class='page']/ul/li[2]/ul/li[" + str(tgt_page_number) + "]"))
            time.sleep(.1)
            tgt_pager = get_widget_ignore_refrence_error(driver, id_tgt_pager)
            if not tgt_pager.get_attribute('class').find('ebPagination-entryAnchor_current') > -1:
                tgt_pager.click()
                trs = find_all_widgets(driver, 20, id_tbdoy_trs)
                if rows % rows_of_page <= len(trs):
                    test.passed('All the data that we need are ready now.')
                    return
        except TimeoutException:
            pass
        time.sleep(.5)
    test.failed('It seems that the the data we need has not been collected as expectes, case may fail later steps.')


def check_pm_rows_updated(driver, ne_type, dict_counters, rows_of_page, dict_additional, counter_types):
    '''
    The main function that check the PM Data accurate, it will first check the data of each row,
    then check the GUI time's minutes is multiple of 5,
    then check the Lics if the node has many LICs.
    :param ne_type: the ne's type
    :param dict_counters: the base counter values in dictionary
    :param rows_of_page: how many rows each page has on the GUI, default is 10
    :param dict_additional: additional information that used for special nodes, (number_of_lic: how many lics of a no
    de), (check_rows: how many rows that will be checked, if this value exist, will only check this number of rows,
    otherwise the number of rows will checked is equal the size of dict_counters)
    :return: None
    '''
    check_rounds = dict_additional['check_rounds']
    number_of_rows_be_checked = check_rounds * dict_additional['number_of_lic']
    wait_until_rounds_ok(driver, number_of_rows_be_checked, 10, dict_additional['number_of_lic'])
    is_m_lics = True if dict_additional['number_of_lic'] > 1 else False
    list_returns = []
    id_table = (By.XPATH, "//div[@class='ebTabs']/div[2]/div/div/div/div/table")

    id_header_trs = (By.XPATH, "//div[@class='ebTabs']/div[2]/div/div/div/div/table/thead/tr/th")
    ths = find_all_widgets(driver, 20, id_header_trs)
    list_headers = []
    for th in ths:
        list_headers.append(th.get_attribute('innerHTML').encode('utf-8').strip())
    # if not 0 == number_of_rows_be_checked % dict_additional['number_of_lic']:
    #    test.error('Number of checked rows should be integer multiples of number of LICs.')
    for row_index in range(1, number_of_rows_be_checked + 1):
        # check_pm_by_row returns [gui_datettime, lic_name] in List
        list_returns.append(check_pm_by_row(driver, id_table, row_index, ne_type, dict_counters, rows_of_page,
                                            list_headers, is_m_lics, counter_types))
    # check GUI time and lic_name
    lic_from_gui = []
    if number_of_rows_be_checked != len(list_returns):
        test.failed('Number of rows need to be checked mis-match with the number we expected.')
    else:
        number_of_lic = dict_additional['number_of_lic']
        for i in range(0, len(list_returns), number_of_lic):
            for j in range(number_of_lic):
                lic_from_gui.append(list_returns[i + j][1])
                gui_time_and_lic_name = list_returns[i + j]
                if gui_time_and_lic_name[0] is not None and 0 == gui_time_and_lic_name[0].minute % 5:
                    test.passed('Row ' + str(i + j) + ' GUI time is correct, is: ' +
                                gui_time_and_lic_name[0].strftime('%Y-%m-%d %H:%M'))
                else:
                    test.failed('Row ' + str(i + j) + ' GUI time is not multiple of 5, is: ' +
                                gui_time_and_lic_name[0].strftime('%Y-%m-%d %H:%M'))
                if is_m_lics:
                    msg = 'Node has more than one LIC, '
                    if list_returns[i][0] == list_returns[i + j][0]:
                        msg += ' different LICs have the same report time.'
                        test.passed(msg)
                    else:
                        msg += ' different LICs don\'t have the same report time.'
                        test.failed(msg)
            if i + number_of_lic < len(list_returns):
                # the pre-condition of this check point is: GUI list data decent by datetime
                if 300 == (list_returns[i][0] - list_returns[i + number_of_lic][0]).seconds:
                    test.passed('Report delta time is 5 minutes.')
                else:
                    test.failed('Report delta time is not 5 minutes.')
    # if checked 1 hour PM and node has many LICs, will check the LIC
    if 12 == int(number_of_rows_be_checked / dict_additional['number_of_lic']):
        if is_m_lics:
            expected_lic = [t.split('-', 1)[1].strip() for t in sorted(dict_counters)]
            if compare_lists(expected_lic, lic_from_gui):
                test.passed('Lic check passed.')
            else:
                test.failed('Lic check failed, E: ' + str(expected_lic) + ', G: ' + str(lic_from_gui))
        # else will check single LIC node, will not cover this edition


def check_me_counters(driver, ne_type, counters_expected, rows_of_page, dict_me_add, me_types):
    '''
    This function will check the ME counters, the first edition suspect that only one record each 5 minutes.
    :param ne_type the type of the node
    :param counters_expected: node ME counters that will check with the counters on GUI
    :param dict_me_add: additional information, (check_rounds: how many rounds that will be checked), (
    rows_each_period: how many rows each period, default is 1, this parameter is for extending later.)
    :return: None: the function is for automation testing, critical errors will case program to exit immediately
    '''
    checked_rounds = dict_me_add['check_rounds']
    number_of_rows_be_checked = checked_rounds * dict_me_add['rows_each_period']
    wait_until_rounds_ok(driver, number_of_rows_be_checked, 10, dict_me_add['rows_each_period'])
    list_returns = []
    id_table = (By.XPATH, "//div[@class='ebTabs']/div[2]/div/div/div/div/table")

    id_header_trs = (By.XPATH, "//div[@class='ebTabs']/div[2]/div/div/div/div/table/thead/tr/th")
    ths = find_all_widgets(driver, 20, id_header_trs)
    list_headers = []
    for th in ths:
        list_headers.append(th.get_attribute('innerHTML').encode('utf-8').strip())
    # number_of_rows_be_checked = len(counters_expected)
    # if dict_me_add.has_key('check_rounds'):
    # if not 0 == number_of_rows_be_checked % dict_me_add['number_of_lic']:
    #    test.error('Number of checked rows should be integer multiples of number of LICs.')
    for row_index in range(1, number_of_rows_be_checked + 1):
        # check_pm_by_row returns [gui_datettime, lic_name] in List
        time_of_gui = check_me_single_row(driver, id_table, row_index, ne_type, counters_expected,
                                          rows_of_page, list_headers, me_types)
        list_returns.append(time_of_gui)

    if number_of_rows_be_checked != len(list_returns):
        test.failed('Number of rows have been checked mis-match with the number we expected.')
    else:
        for i in range(len(list_returns)):
            if list_returns[i] is not None and 0 == list_returns[i].minute % 5:
                test.passed('Row ' + str(i) + ' GUI time is correct, is: ' +
                            list_returns[i].strftime('%Y-%m-%d %H:%M'))
            else:
                test.failed('Row ' + str(i) + ' GUI time is correct, is: ' +
                            list_returns[i].strftime('%Y-%m-%d %H:%M'))
            if i + 1 < len(list_returns):
                if 300 == (list_returns[i] - list_returns[i + 1]).seconds:
                    test.passed('Report delta time is 5 minutes.')
                else:
                    test.failed('Report delta time is not 5 minutes.')


def check_pm_rows(driver, logger, ne_type, dict_counters, rows_of_page, dict_additional):
    bool_overall = True
    list_time = []
    id_table = (By.XPATH, "//div[@class='ebTabs']/div[2]/div/div/div/div/table")

    id_header_trs = (By.XPATH, "//div[@class='ebTabs']/div[2]/div/div/div/div/table/thead/tr/th")
    ths = find_all_widgets(driver, 20, id_header_trs)
    list_headers = []
    for th in ths:
        list_headers.append(th.get_attribute('innerHTML').encode('utf-8').strip())
    # table = find_single_widget(driver, 10, id_table)

    rounds = len(dict_counters)
    if 'SBC' == ne_type:
        if dict_additional.has_key('rounds'):
            rounds = dict_additional['rounds']

    for i in range(1, rounds + 1):
        bool_row, gui_time = check_pm_by_row(driver, id_table, logger, i, ne_type, dict_counters, rows_of_page, list_headers)
        list_time.append(gui_time)
        if not bool_row:
            bool_overall = False
            logger.error('Row ' + str(i) + " check FAILED. Check the log for detailed information.")
        else:
            logger.info('Row ' + str(i) + " check PASSED.")

    if bool_overall:
        if len(list_time) < 1:
            bool_overall = False
            logger.error('Failed: 0 rounds of PM checked, this does not make any sense.')
        elif len(list_time) < 2:
            if 'OCGAS' == ne_type:
                bool_overall = False
                logger.error('Failed: Node OCGAS is supposed to have two LICs, there is only one record of PM Data.')
            elif list_time[0] is None:
                bool_overall = False
                logger.error('Failed: Fail to get the PM data time.')
            else:
                if 0 != list_time[0].minute % 5:
                    bool_overall = False
                    logger.error('Failed: PM Data time is not multiples of 5.')
        else:
            if ne_type in ['SGW', 'PGW', 'SGSN', 'MME', 'SBC']:
                for i in range(0, len(list_time) - 1):
                    if list_time[i] is None or list_time[i + 1] is None:
                        bool_overall = False
                        logger.error('Failed: Fail to get the PM data time.')
                        break
                    else:
                        if 0 != list_time[i].minute % 5 or 0 != list_time[i + 1].minute % 5:
                            bool_overall = False
                            logger.error('Failed: PM Data time is not multiples of 5.')
                            break
                        if 300 != abs((list_time[i] - list_time[i + 1]).seconds):
                            bool_overall = False
                            logger.error('Failed: PM period is not 5 minutes.')
                            break
            elif 'OCGAS' == ne_type:
                for i in range(0, len(list_time), 2):
                    if i != len(list_time) - 2:
                        if list_time[i] is None or list_time[i + 1] is None or list_time[i + 2] is None:
                            bool_overall = False
                            logger.error('Failed: Fail to get the PM data time.')
                            break
                        else:
                            if list_time[i] != list_time[i + 1]:
                                bool_overall = False
                                logger.error('Failed: Two LICs of Node OCGAS should be the same.')
                                break
                            else:
                                if 0 != list_time[i].minute % 5 or 0 != list_time[i + 2].minute % 5:
                                    bool_overall = False
                                    logger.error('Failed: PM Data time is not multiples of 5.')
                                    break
                                elif 300 != abs((list_time[i] - list_time[i + 2]).seconds):
                                    bool_overall = False
                                    logger.error('Failed: PM period is not 5 minutes. ' + str(list_time[i]) + ' '
                                                 + str(list_time[i + 2]))
                                    break
    logger.info('GUI times: ' + ', '.join([str(t) for t in list_time]))
    if bool_overall:
        logger.info("Overall PASSED.")
    else:
        logger.error("Overall FAILED.")


def check_pm_by_row(driver, id_table, index_row, ne_type, dict_counters, rows_of_page, list_headers, is_m_lics,
                    counter_types):
    test.info('Start to check row: ' + str(index_row))

    make_sure_is_correct_page(driver, index_row, rows_of_page)
    try:
        gui_index_row = rows_of_page if 0 == index_row % rows_of_page else index_row % rows_of_page
        id_tr = (By.XPATH, ".//tbody/tr[" + str(gui_index_row) + "]")
        table = find_single_widget(driver, 10, id_table)
        time.sleep(.5)
        tr = find_single_widget(table, 10, id_tr)
        gui_str_time = find_single_widget(tr, 10, (By.XPATH, ".//td[2]")).get_attribute('innerHTML').encode('utf-8')
        gui_time = datetime.strptime(gui_str_time.strip(), "%Y-%m-%d %H:%M")
        except_counter_id = str(gui_time.minute)

        id_lic_name = (By.XPATH, ".//td[3]")
        lic_name = find_single_widget(tr, 5, id_lic_name).get_attribute('innerHTML').encode('utf-8')
        if is_m_lics:
            except_counter_id = str(gui_time.minute) + '-' + lic_name
        list_row = dict_counters[except_counter_id].split(',')
        list_types = counter_types['li_counter_types'].split(',')
        for i in range(len(list_row)):
            try:
                id_counter = (By.XPATH, ".//td[" + str(i + 4) + "]")
                gui_counter = find_single_widget(tr, 5, id_counter).get_attribute('innerHTML').encode('utf-8')
                if 'int' == list_types[i].lower().strip():
                    i_exp = int(list_row[i].strip())
                    i_gui = int(gui_counter)
                elif 'float' == list_types[i].lower().strip():
                    i_exp = float(list_row[i].strip())
                    i_gui = float(gui_counter)
                else:
                    test.error('Unknown counter type of li counters.')
            except Exception as e:
                i_gui = None

            if i_exp == i_gui:
                msg = list_headers[1] + ": " + gui_str_time.strip() + ",\t" + list_headers[2] + ": " + lic_name + "; " \
                      + list_headers[i + 3] + ", GUI is " + str(i_gui) + ",\tExpected is " + str(i_exp) \
                      + "."

                test.passed(msg)
            else:
                msg = list_headers[1] + ": " + gui_str_time.strip() + ",\t" + list_headers[2] + ": " + lic_name + "; " \
                      + list_headers[i + 3] + ", GUI is " + str(i_gui) + ",\tExpected is " + str(i_exp) \
                      + "."

                test.failed(msg)
        return [gui_time, lic_name]
    except Exception as e:
        test.error("Test failed, ERROR: " + str(e))


def check_me_single_row(driver, id_table, index_row, ne_type, dict_counters, rows_of_page, list_headers, me_types):
    test.info('Start to check ME row: ' + str(index_row))

    make_sure_is_correct_page(driver, index_row, rows_of_page)
    try:
        gui_index_row = rows_of_page if 0 == index_row % rows_of_page else index_row % rows_of_page
        id_tr = (By.XPATH, ".//tbody/tr[" + str(gui_index_row) + "]")
        table = find_single_widget(driver, 10, id_table)
        time.sleep(.5)
        tr = find_single_widget(table, 10, id_tr)
        gui_str_time = find_single_widget(tr, 10, (By.XPATH, ".//td[2]")).get_attribute('innerHTML').encode('utf-8')
        gui_time = datetime.strptime(gui_str_time.strip(), "%Y-%m-%d %H:%M")
        except_counter_id = str(gui_time.minute)

        # id_lic_name = (By.XPATH, ".//td[3]")
        # lic_name = find_single_widget(tr, 5, id_lic_name).get_attribute('innerHTML').encode('utf-8')

        list_row = dict_counters[except_counter_id].split(',')
        list_types = me_types['me_counter_types'].split(',')
        for i in range(len(list_row)):
            try:
                id_counter = (By.XPATH, ".//td[" + str(i + 3) + "]")
                gui_counter = find_single_widget(tr, 5, id_counter).get_attribute('innerHTML').encode('utf-8')
                # i_gui_counter = int(gui_counter) if 'int' == list_types[i].lower().strip()
                if 'int' == list_types[i].lower().strip():
                    i_gui_counter = int(gui_counter)
                    i_expected = int(list_row[i].strip())
                elif 'float' == list_types[i].lower().strip():
                    i_gui_counter = float(gui_counter)
                    i_expected = float(list_row[i].strip())
                else:
                    test.error('Unknown counter type of me counters.')
            except Exception as e:
                i_gui_counter = None
            if i_expected == i_gui_counter:
                msg = list_headers[1] + ": " + gui_str_time.strip() + ",\t" + "; " + list_headers[i + 2] + ", GUI is " \
                      + str(i_gui_counter) + ",\tExpected is " + str(list_row[i]) + "."

                test.passed(msg)
            else:
                msg = list_headers[1] + ": " + gui_str_time.strip() + ",\t" + "; " + list_headers[i + 2] + ", GUI is " \
                      + str(i_gui_counter) + ",\tExpected is " + str(list_row[i]) + "."

                test.failed(msg)
        return gui_time
    except Exception as e:
        test.error("Test failed, ERROR: " + str(e))


def to_second_page(driver, logger):
    id_next_page = (By.XPATH, "//div[@class='page']/ul/li[3]")
    pager = find_single_widget(driver, 10, id_next_page)
    # driver.execute_script("arguments[0].scrollIntoView(true);", tds[12])
    driver.execute_script("arguments[0].scrollIntoView(true);", pager)
    pager.click()
    # wait for the notification, maximum 10 seconds
    id_body_date = (By.XPATH, "//div[@class='ebTabs']/div[2]/div/div/div/div/table/tbody")
    find_single_widget(driver, 10, id_body_date)
    # time.sleep(2.0)


def make_sure_is_correct_page(driver, row_index, rows_of_page):
    """
    This function handle the situation that we need to paginate to different to check the PM datas.
    :param rows_of_page: how many rows each page has
    :param driver: selenium instance
    :param row_index: row index of the GUI
    :return: None
    """
    i_page = row_index / rows_of_page
    tgt_page_number = i_page if 0 == row_index % rows_of_page else i_page + 1
    id_tgt_pager = (By.XPATH, ("//div[@class='page']/ul/li[2]/ul/li[" + str(tgt_page_number) + "]"))
    tgt_pager = find_single_widget(driver, 10, id_tgt_pager)
    if not tgt_pager.get_attribute('class').find('ebPagination-entryAnchor_current') > -1:
        tgt_pager.click()
        # wait for the notification, maximum 10 seconds
        id_body_date = (By.XPATH, "//div[@class='ebTabs']/div[2]/div/div/div/div/table/tbody")
        find_single_widget(driver, 10, id_body_date)
        test.info('Now in page ' + str(tgt_page_number) + '.')


def set_time_for_query(driver, date_time):
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
