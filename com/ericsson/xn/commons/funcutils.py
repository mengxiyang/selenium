# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def find_single_widget(driver, wait_time, list_identifier):
    return WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(list_identifier))


def find_all_widgets(driver, wait_time, list_identifier):
    return WebDriverWait(driver, wait_time).until(EC.presence_of_all_elements_located(list_identifier))


def wait_until_text_shown_up(driver, wait_time, list_identifier, text):
    return WebDriverWait(driver, wait_time).until(EC.text_to_be_present_in_element_value(list_identifier, text))


def is_pair_nes(ne, cne):
    # list_EPG = ["SGW", "PGW"]
    # list_MME = ["SGSN", "MME"]
    if ne == cne:
        return False

    if "MME" == ne and "SGSN" == cne:
        return True

    if "SGSN" == ne and "MME" == cne:
        return True

    if "SGW" == ne and "PGW" == cne:
        return True

    if "PGW" == ne and "SGW" == cne:
        return True

    return False


def ne_type_index_add_ne_page(ne_type):
    dic = {
        "MME": 1,
        "OCGAS": 2,
        "PGW": 3,
        "SBC": 4,
        "SGSN": 5,
        "SGW": 6
    }
    if dic.has_key(ne_type):
        return dic[ne_type]
    return None


"""
def wait_until_text_is_not_none(widget, timeout, interval=.25):
    end_time = datetime.now() + timedelta(seconds=timeout)
    while datetime.now() < end_time:
        text = widget.get_attribute('innerHTML').encode('utf-8').strip()
        if not '' == text:
            return text
        time.sleep(interval)
    return None
"""