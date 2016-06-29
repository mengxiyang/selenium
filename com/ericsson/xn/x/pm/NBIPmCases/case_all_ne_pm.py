from com.ericsson.xn.x.pm.PmCommons import NBIPmFunc
from com.ericsson.xn.commons import test_logger
from com.ericsson.xn.commons import caseutils
from com.ericsson.xn.x.pm.NBIPmCases import case_imshss_pm, case_ltehss_pm,\
    case_mme_pm, case_pgw_pm, case_sgw_pm, case_sgsn_pm, case_ocgas_pm


def check_pm_all_nes():
    case_imshss_pm.check_pm_imshss()
    case_ltehss_pm.check_pm_ltehss()
    case_mme_pm.check_pm_mme()
    case_sgsn_pm.check_pm_sgsn()
    case_pgw_pm.check_pm_pgw()
    case_sgw_pm.check_pm_sgw()
    case_ocgas_pm.check_pm_as()

    
    