# -*- coding: utf-8 -*-
import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

logger_instance = None


class LoggerInstance:

    def __init__(self, file_name, sub_dir=None):
        file_name = file_name.strip()
        self.case_name = file_name
        sep = os.path.sep
        _module_path = os.path.dirname(os.path.abspath(__file__))
        root_dir = _module_path.split('com' + sep + 'ericsson' + sep + 'xn' + sep + 'commons')[0]
        log_dir = os.path.normpath(root_dir + sep + 'logs')
        if sub_dir:
            log_dir = log_dir + sep + sub_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.normpath(log_dir + sep + file_name + '-' + datetime.now().strftime('%Y%m%d%H%M%S') +
                                    '.result')
        self.logger_instance = logging.getLogger(file_name)
        log_handler = RotatingFileHandler(log_file, mode='a', maxBytes=1024 * 1024 * 10, backupCount=10,
                                          encoding='utf-8', delay=0)
        # custom log format here
        # ('%(asctime)s [%(levelname)s] %(module)s %(funcName)s(%(lineno)d) %(message)s')
        log_formatter = logging.Formatter('%(message)s')
        log_handler.setFormatter(log_formatter)
        # set to debug level
        log_handler.setLevel(10)
        self.logger_instance.setLevel(10)
        self.logger_instance.addHandler(log_handler)
        # print the console log by default
        '''
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(50)
        stream_handler.setFormatter(log_formatter)
        self.logger_instance.addHandler(stream_handler)
        '''
        self.step = 0
        self.failed_step = 0
        self.error_step = 0
        self.warning_step = 0
        self.log_init_information()

    def log_sth(self, result, additional):
        self.step += 1
        msg = 'Step ' + str(self.step) + ',\t' + result + ': ' + additional
        self.logger_instance.info(self._encode_msg(msg))
        if 'Error' == result:
            sys.exit(0)

    def log_info(self, additional):
        self.logger_instance.info(self._encode_msg('Info: ' + additional))

    def log_passed(self, msg):
        self.step += 1
        self.logger_instance.info(self._encode_msg('Step ' + str(self.step) + ', Passed: ' + msg))

    def log_failed(self, msg):
        self.step += 1
        self.failed_step += 1
        self.logger_instance.info(self._encode_msg('Step ' + str(self.step) + ', Failed: ' + msg))

    def log_warning(self, msg):
        self.warning_step += 1
        self.step += 1
        self.logger_instance.info(self._encode_msg('Step ' + str(self.step) + ', Warning: ' + msg))

    def log_error(self, msg):
        self.step += 1
        self.error_step += 1
        self.logger_instance.info(self._encode_msg('Step ' + str(self.step) + ', Failed: ' + msg))
        self.logger_instance.info(self._encode_msg('Error occurred, test case will exit soon.'))
        self.log_overall_result()
        sys.exit(0)

    def log_init_information(self):
        self.logger_instance.info('Test case: ' + self.case_name + ' started.')

    def log_overall_result(self):
        pass_steps = self.step - self.failed_step - self.error_step
        overall_result = 'Failed' if self.failed_step > 0 or self.error_step > 0 else 'Passed'
        msg = 'Test case: ' + self.case_name + ' ' + overall_result + '. Total steps: ' + str(self.step) + \
              ', Passed steps: ' + str(pass_steps) + ', Error steps: ' + str(self.error_step) + ', Failed steps: ' \
              + str(self.failed_step) + ', Warning steps: ' + str(self.warning_step)
        self.logger_instance.critical(self._encode_msg(msg))

    def _encode_msg(self, msg):
        return msg.encode('utf-8')


def init_logger_instance(file_name, sub_dir):
    global logger_instance
    if not logger_instance:
        logger_instance = LoggerInstance(file_name, sub_dir)


def log_test_step(result, additional):
    global logger_instance
    if logger_instance:
        if 'Info' == result:
            logger_instance.log_info(additional)
        elif 'Passed' == result:
            logger_instance.log_passed(additional)
        elif 'Failed' == result:
            logger_instance.log_failed(additional)
        elif 'Error' == result:
            logger_instance.log_error(additional)


def finish_test_steps():
    global logger_instance
    if logger_instance:
        logger_instance.log_overall_result()


init = lambda x, y: init_logger_instance(x, y)
passed = lambda y: log_test_step('Passed', y)
failed = lambda y: log_test_step('Failed', y)
error = lambda y: log_test_step('Error', y)
info = lambda y: log_test_step('Info', y)
warning = lambda y: log_test_step('Warning', y)
finish = lambda: finish_test_steps()


