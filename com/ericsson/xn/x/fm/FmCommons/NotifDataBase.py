'''
Created on Mar 22, 2016

@author: eyyylll
'''

from com.ericsson.xn.x.fm.FmCommons import MappingParser
import xml.etree.ElementTree as ET
from com.ericsson.xn.commons.PyProperties import Properties
import os
from com.ericsson.xn.commons import test_logger as test



class notifMapping():
    def __init__(self,common_cfg,nbi_mapping_cfg):
        if not os.path.exists(common_cfg):
            test.error("mapping cfg file:" + common_cfg + " not exist")
        elif not os.path.exists(nbi_mapping_cfg):
            test.error("mapping cfg file:" + nbi_mapping_cfg + " not exist")
        
        common_mapping_info = Properties(common_cfg)
        notif_mapping_info = MappingParser(nbi_mapping_cfg)
        
            
    

