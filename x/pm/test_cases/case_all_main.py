# -*- coding: utf-8 -*-

import os
import sys
# import glob
# import logging
sep = os.path.sep
root_dir = os.path.dirname(os.path.abspath(__file__)).split('x' + sep + 'pm' + sep + 'test_cases')[0]
sys.path.insert(0, root_dir)

import case_main_3gsgsn_lic_and_me
import case_main_ggsn_lic_and_me
import case_main_gmlc_lic_and_me
import case_main_hlr_lic_and_me
import case_main_imshss_lic_and_me
import case_main_ltehss_lic_and_me
import case_main_msc_lic_and_me
import case_main_ocgas_lic_and_me
import case_main_pgw_lic_and_me
import case_main_sgw_lic_and_me


if __name__ == '__main__':
    case_main_3gsgsn_lic_and_me
    case_main_ggsn_lic_and_me
    case_main_gmlc_lic_and_me
    case_main_hlr_lic_and_me
    case_main_imshss_lic_and_me
    case_main_ltehss_lic_and_me
    case_main_msc_lic_and_me
    case_main_ocgas_lic_and_me
    case_main_pgw_lic_and_me
    case_main_sgw_lic_and_me
