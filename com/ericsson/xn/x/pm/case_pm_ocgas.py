# -*- coding: utf-8 -*-

import os
from com.ericsson.xn.x.pm.PmCommons import PmCaseBase


def pm_ocgas_func():
    sep = os.sep
    root_dir = os.path.dirname(os.path.abspath(__file__)).split(sep + 'com' + sep + 'ericsson' +
                                                                sep + 'xn' + sep + 'x' + sep + 'pm')[0]
    ne_info_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'nes' + sep + 'ocgas.cfg')
    counter_info_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'counters' + sep + 'ocgas.cfg')
    tgt_server = '10.184.73.77'
    PmCaseBase.check_pm_accurate(ne_info_cfg, counter_info_cfg, tgt_server, '2015-01-04 01:01:00')