# -*- coding: utf-8 -*-

import os
import sys
# import glob
# import logging
sep = os.path.sep
root_dir = os.path.dirname(os.path.abspath(__file__)).split('x' + sep + 'pm' + sep + 'test_cases')[0]
sys.path.insert(0, root_dir)
'''
logger = logging.getLogger('Streaming Log')
log_formatter = logging.Formatter('%(message)s')
log_stream = logging.StreamHandler()
log_stream.setLevel(50)
log_stream.setFormatter(log_formatter)
logger.addHandler(log_stream)
logger.setLevel(50)

gui_dir = os.path.normpath(root_dir + sep + 'logs' + sep + 'pm_automation')
nbi_dir = os.path.normpath(root_dir + sep + 'logs' + sep + 'nbi_pm_automation')
'''
import case_main_imshss_pm_and_me
# log = max(glob.iglob(os.path.join(gui_dir, '*.result')), key=os.path.getctime)
# logger.critical(open(log, 'r+').readlines()[-1].strip())

import case_main_imshss_nbi
# log = max(glob.iglob(os.path.join(nbi_dir, '*.result')), key=os.path.getctime)
# logger.critical(open(log, 'r+').readlines()[-1].strip())