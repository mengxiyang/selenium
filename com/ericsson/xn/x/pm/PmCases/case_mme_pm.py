# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
from com.ericsson.xn.x.pm.PmCommons import PmCaseBase


def pm_mme_func():
    sep = os.sep
    root_dir = os.path.dirname(os.path.abspath(__file__)).split(sep + 'com' + sep + 'ericsson' +
                                                                sep + 'xn' + sep + 'x' + sep + 'pm')[0]
    ne_info_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'nes' + sep + 'mme.cfg')
    counter_info_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'counters' + sep + 'mme.cfg')
    server_info_path = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'execute_conf.cfg')
    t_now = datetime.now()
    end_time = t_now + timedelta(minutes=-(t_now.minute % 5 + 14))
    str_end_time = end_time.strftime('%Y-%m-%d %H:%M') + ":00"
    PmCaseBase.check_pm_accurate_lic(ne_info_cfg, counter_info_cfg, server_info_path, str_end_time)