# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
from com.ericsson.xn.x.pm.PmCommons import PmCaseBase


def check_pm_all_nes():
    sep = os.sep
    root_dir = os.path.dirname(os.path.abspath(__file__)).split(sep + 'com' + sep + 'ericsson' +
                                                                sep + 'xn' + sep + 'x' + sep + 'pm')[0]
    ne_dir = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'nes')
    ct_dir = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'counters')

    # ne_info_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'nes' + sep + 'mme.cfg')
    # counter_info_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'counters' + sep + 'mme.cfg')

    server_info_path = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'execute_conf.cfg')
    t_now = datetime.now()
    end_time = t_now + timedelta(minutes=-(t_now.minute % 5 + 14))
    str_end_time = end_time.strftime('%Y-%m-%d %H:%M') + ":00"

    dict_all_nes_infos = {
        "SBC": {
            "ne_cfg": os.path.normpath(ne_dir + sep + 'sbc.cfg'),
            "ct_cfg": os.path.normpath(ct_dir + sep + 'sbc.cfg'),
            "rounds": 3
        },
        "OCGAS": {
            "ne_cfg": os.path.normpath(ne_dir + sep + 'ocgas.cfg'),
            "ct_cfg": os.path.normpath(ct_dir + sep + 'ocgas.cfg'),
            "end_time": str_end_time
        },
        "SGW": {
            "ne_cfg": os.path.normpath(ne_dir + sep + 'sgw.cfg'),
            "ct_cfg": os.path.normpath(ct_dir + sep + 'sgw.cfg'),
            "end_time": str_end_time
        },
        "PGW": {
            "ne_cfg": os.path.normpath(ne_dir + sep + 'pgw.cfg'),
            "ct_cfg": os.path.normpath(ct_dir + sep + 'pgw.cfg'),
            "end_time": str_end_time
        },
        "SGSN": {
            "ne_cfg": os.path.normpath(ne_dir + sep + 'sgsn.cfg'),
            "ct_cfg": os.path.normpath(ct_dir + sep + 'sgsn.cfg'),
            "end_time": str_end_time
        },
        "MME": {
            "ne_cfg": os.path.normpath(ne_dir + sep + 'mme.cfg'),
            "ct_cfg": os.path.normpath(ct_dir + sep + 'mme.cfg'),
            "end_time": str_end_time
        }
    }

    PmCaseBase.check_pm_accurate_all_ne(dict_all_nes_infos, server_info_path)