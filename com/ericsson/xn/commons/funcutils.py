# -*- coding: utf-8 -*-
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


def find_single_widget(driver, wait_time, list_identifier):
    return WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(list_identifier))


def find_all_widgets(driver, wait_time, list_identifier):
    return WebDriverWait(driver, wait_time).until(EC.presence_of_all_elements_located(list_identifier))


def wait_until_text_shown_up(driver, wait_time, list_identifier, text):
    return WebDriverWait(driver, wait_time).until(EC.text_to_be_present_in_element_value(list_identifier, text))


def get_widget_ignore_refrence_error(driver, list_identifier, sleep_time=.5, wait_time=10):
    try:
        return WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(list_identifier))
    except StaleElementReferenceException:
        # this exception happens when widget distroyed and re-build again, sleep while will OK
        sleep(sleep_time)
        return WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(list_identifier))


def is_pair_nes(ne, cne):
    # list_EPG = ["SGW", "PGW"]
    # list_MME = ["SGSN", "MME"]
    # list_HSS = ["IMSHSS","LTEHSS"]
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

    if "LTEHSS" == ne and "IMSHSS" == cne:
        return True

    if "IMSHSS" == ne and "LTEHSS" == cne:
        return True

    return False


def ne_type_index_add_ne_page(ne_type):
    dic = {
        "3GSGSN": 1,
        "GGSN": 2,
        "GMLC": 3,
        "HLR": 4,
        "IMSHSS": 5,
        "LTEHSS": 6,
        "MME": 7,
        "MSC": 8,
        "MTAS": 9,
        "OCGAS": 10,
        "PCSCF": 11,
        "SGW": 12,
        "PGW": 13,
        "SBC": 14,
        "SGSN": 15
    }
    if dic.has_key(ne_type):
        return dic[ne_type]
    return None


def ne_category_by_ne_type(ne_type):
    category = {
        'SGW': '4G',
        'PGW': '4G',
        'SGSN': '3G',
        'MME': '4G',
        'SBC': 'IMS',
        'OCGAS': 'IMS',
        'IMSHSS': 'IMS',
        'LTEHSS': '4G',
        'GMLC': '3G',
        '3GSGSN': '3G'
    }
    return category[ne_type]


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
