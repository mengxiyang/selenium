# -*- coding: utf-8 -*-

import os
from com.ericsson.xn.x.pm.PmCommons import PmCaseBase


def pm_sbc_func_2rounds():
    sep = os.sep
    root_dir = os.path.dirname(os.path.abspath(__file__)).split(sep + 'com' + sep + 'ericsson' + sep + 'xn' + sep
                                                                + 'x' + sep + 'pm' + sep + 'PmCases')[0]
    ne_info_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'nes' + sep + 'sbc.cfg')
    counter_info_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'counters' + sep + 'sbc.cfg')
    tgt_server = '10.184.73.77'
    PmCaseBase.check_pm_accurate_sbc(ne_info_cfg, counter_info_cfg, tgt_server, 2)