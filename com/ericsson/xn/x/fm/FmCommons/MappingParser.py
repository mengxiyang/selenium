
import xml.etree.ElementTree as ET
from com.ericsson.xn.commons import test_logger as test
import os


root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__))).split('com' + os.sep + 'ericsson' + os.sep + 'xn' + os.sep + 'x' + os.sep + 'fm' + os.sep + 'FmCommons')[0]
mapping_cfg = root_dir + os.sep + 'x' + os.sep + 'fm' + os.sep + 'nbi_mapping' + os.sep + 'ne_new_alarm.cfg'


class MappingParser():
	
	
	

