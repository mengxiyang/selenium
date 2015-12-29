# -*- coding: utf-8 -*-

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from com.ericsson.xn.commons.funcutils import find_single_widget, find_all_widgets


def _to_ne_management_page(driver, logger):
    logger.info('To the PmManagement page...')

    identifier = (By.XPATH, "//div[@class='ebLayout-Navigation']/div/div[1]/span")
    find_single_widget(driver, 10, identifier).click()

    identifier = (By.XPATH, "//div[@class='ebBreadcrumbs-list']/ul/li[1]/a")
    find_single_widget(driver, 10, identifier).click()

    id_new_btn = (By.ID, "idBtn-create")
    find_single_widget(driver, 10, id_new_btn)


def _add_new_ne(driver, logger, list_ne_info):

    pass


def _check_ne_exist(driver, logger, ne_type, ne_ip):
    # note there is another way to check if NE with certain IP exist, that is connect to the server's database and
    # check the NES data table
    id_table = (By.XPATH, "//div[@class='dv1']/div[2]/div/div/div[3]/div/div/div/table")
    table = find_single_widget(driver, 10, id_table)

    id_trs = (By.XPATH, ".//tbody/tr")
    trs = find_all_widgets(table, 20, id_trs)

    for tr in trs:
        # gui_type = tr.get_attribute('innerHTML').encode('utf-8')
        gui_ne_name = find_single_widget(tr, 10, (By.XPATH, ".//td[1]")).get_attribute('innerHTML').encode('utf-8')
        gui_ne_type = find_single_widget(tr, 10, (By.XPATH, ".//td[2]")).get_attribute('innerHTML').encode('utf-8')

        tr.click()
