# -*- coding: utf-8 -*-

import os
from . import pm_case


def pm_mme_func():
    sep = os.sep
    root_dir = os.path.dirname(os.path.abspath(__file__)).split(sep + 'com' + sep + 'ericsson' +
                                                                sep + 'xn' + sep + 'x' + sep + 'pm')[0]
    ne_info_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'nes' + sep + 'mme.cfg')
    counter_info_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'counters' + sep + 'mme.cfg')
    tgt_server = '10.184.73.77'
    pm_case.check_pm_accurate(ne_info_cfg, counter_info_cfg, tgt_server, '2015-01-04 01:01:00')