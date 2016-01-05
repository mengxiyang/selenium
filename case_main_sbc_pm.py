# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from com.ericsson.xn.x.pm.PmCases import case_sbc_pm


if __name__ == '__main__':
    case_sbc_pm.pm_sbc_func_2rounds()