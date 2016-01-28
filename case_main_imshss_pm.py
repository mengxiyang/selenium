# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
from com.ericsson.xn.commons import caseutils
from com.ericsson.xn.x.pm.PmCommons import PmBaseFunc

sep = os.sep
module_name = os.path.split(os.path.abspath(__file__))[1][:-3]
# Pre of the test case
caseutils.pre_test_case(module_name, 'pm_automation')

root_dir = os.path.dirname(os.path.abspath(__file__))
ne_info_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'nes' + sep + 'imshss.cfg')
counter_info_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'counters' + sep + 'imshss.cfg')
me_counter_cfg = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'me_counters' + sep + 'imshss.cfg')
server_info_path = os.path.normpath(root_dir + sep + 'x' + sep + 'pm' + sep + 'execute_conf.cfg')
t_now = datetime.now()
end_time = t_now + timedelta(minutes=-(t_now.minute % 5 + 14))
str_end_time = end_time.strftime('%Y-%m-%d %H:%M') + ":00"
PmBaseFunc.check_pm_accurate(ne_info_cfg, counter_info_cfg, server_info_path, str_end_time, me_counter_cfg)

# Post of the test case
caseutils.post_test_case()
