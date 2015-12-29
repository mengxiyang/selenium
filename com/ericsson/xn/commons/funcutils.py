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


def wait_until_text_is_not_none(widget, timeout, interval=.25):
    end_time = datetime.now() + timedelta(seconds = timeout)
    while datetime.now() < end_time:
        text = widget.get_attribute('innerHTML').encode('utf-8').strip()
        if not '' == text:
            return text
        time.sleep(interval)
    return None