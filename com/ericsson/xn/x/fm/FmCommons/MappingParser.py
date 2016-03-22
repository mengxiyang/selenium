
import xml.etree.ElementTree as ET
from com.ericsson.xn.commons import test_logger as test
import os


root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__))).split('com' + os.sep + 'ericsson' + os.sep + 'xn' + os.sep + 'x' + os.sep + 'fm' + os.sep + 'FmCommons')[0]
mapping_cfg = root_dir + os.sep + 'x' + os.sep + 'fm' + os.sep + 'nbi_mapping' + os.sep + 'ne_new_alarm.cfg'


class MappingParser():
	def __init__(self,mapping_cfg):
		if not os.path.exists(mapping_cfg):
			test.error("the mapping.cfg:" + mapping_cfg + " not exist")
		self.dict_mapping_info = 
	
	
	

	   def get_children_element(node,map,keys,values):
	if len(node) == 0:
		map[node.get("name")] = node.text
		return map
	else:
		continue_nodes=[]
		for c in node:
			keys.append(c.get("name"))
			values.append(c.text)
			if len(c) != 0:
				continue_nodes.append(c)
		map = dict(zip(keys,values))
		if len(continue_nodes) != 0:
			for c_c in continue_nodes:
				map[c_c.get("name")] = get_children_element(c_c,{},[],[])
		return map


def get_element_mapping(tree,names):
	dict = {}
	for name in names:
		node = tree.find(name)
		if node != None:
			c_dict = get_children_element(node,{},[],[])
			dict[name] = c_dict
		else:
			test.info("the attribute:" + name + " can't be found in mapping.cfg")
	return dict



if __name__ == '__main__':
	tree = ET.parse(mapping_cfg)
	notif_name = ('event_name','b','w','e')
	dict_notif = get_element_mapping(tree,notif_name)
	print dict_notif