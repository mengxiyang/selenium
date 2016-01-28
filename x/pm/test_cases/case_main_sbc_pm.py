# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
from com.ericsson.xn.commons import caseutils
from com.ericsson.xn.x.pm.PmCommons import PmBaseFunc

sep = os.sep
module_name = os.path.split(os.path.abspath(__file__))[1][:-3]
# Pre of the test case
caseutils.pre_test_case(module_name, 'pm_automation')

root_dir = os.path.dirname(os.path.abspath(__file__)).split('x' + sep + 'pm' + sep + 'test_cases', 1)[0]
ne_info_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'nes' + sep + 'sbc.cfg')
counter_info_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'counters' + sep + 'sbc.cfg')
# me_counter_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'me_counters' + sep + 'ltehss.cfg')
server_info_path = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'execute_conf.cfg')
PmBaseFunc.check_sbc_pm(ne_info_cfg, counter_info_cfg, server_info_path, 1, 3)

# Post of the test case
caseutils.post_test_case()
