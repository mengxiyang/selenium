# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from com.ericsson.xn.x.pm.PmCases import case_sgsn_pm


if __name__ == '__main__':
    case_sgsn_pm.pm_sgsn_func()