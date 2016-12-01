from com.ericsson.xn.x.pm.NBIPmCases import case_imshss_pm
from com.ericsson.xn.x.pm.NBIPmCases import case_ltehss_pm
from com.ericsson.xn.x.pm.NBIPmCases import case_mme_pm
from com.ericsson.xn.x.pm.NBIPmCases import case_sgsn_pm
from com.ericsson.xn.x.pm.NBIPmCases import case_pgw_pm
from com.ericsson.xn.x.pm.NBIPmCases import case_sgw_pm
from com.ericsson.xn.x.pm.NBIPmCases import case_ocgas_pm
from com.ericsson.xn.x.pm.NBIPmCases import case_gmlc_pm
from com.ericsson.xn.x.pm.NBIPmCases import  case_hlr_pm
from com.ericsson.xn.x.pm.NBIPmCases import  case_msc_pm
from com.ericsson.xn.x.pm.NBIPmCases import  case_3gsgsn_pm
from  com.ericsson.xn.x.pm.NBIPmCases import  case_ggsn_pm


if __name__ == '__main__':  
    case_imshss_pm.check_pm_imshss()
    case_ltehss_pm.check_pm_ltehss()
    case_mme_pm.check_pm_mme()
    case_sgsn_pm.check_pm_sgsn()
    case_pgw_pm.check_pm_pgw()
    case_sgw_pm.check_pm_sgw()
    case_ocgas_pm.check_pm_as()
    case_gmlc_pm.check_pm_gmlc()
    case_hlr_pm.check_pm_hlr()
    case_msc_pm.check_pm_msc()
    case_3gsgsn_pm.check_pm_3gsgsn()
    case_ggsn_pm.check_pm_ggsn()