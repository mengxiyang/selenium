# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from com.ericsson.xn.x.pm import case_pm_ocgas

if __name__ == '__main__':
    # case_pm_sgw.pm_sgw_func()
    # case_pm_sgsn.pm_sgsn_func()
    # case_pm_mme.pm_mme_func()
    case_pm_ocgas.pm_ocgas_func()