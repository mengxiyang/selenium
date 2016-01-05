# -*- coding: utf-8 -*-

import os
from . import pm_case


def pm_sgw_func():
    sep = os.sep
    root_dir = os.path.dirname(os.path.abspath(__file__)).split(sep + 'com' + sep + 'ericsson' +
                                                                sep + 'xn' + sep + 'x' + sep + 'pm')[0]
    ne_info_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'nes' + sep + 'sgw.cfg')
    counter_info_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'counters' + sep + 'sgw.cfg')
    tgt_server = '10.184.73.77'
    pm_case.check_pm_accurate(ne_info_cfg, counter_info_cfg, tgt_server)