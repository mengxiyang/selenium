
import xml.etree.ElementTree as ET
from com.ericsson.xn.commons import test_logger as test
import os





class XMLTree():
	def __init__(self,mapping_cfg):
		if not os.path.exists(mapping_cfg):
			test.error("the mapping.cfg:" + mapping_cfg + " not exist")
		self.tree = ET.parse(mapping_cfg)
	

	def get_children_element(self,node,map,keys,values):
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
					map[c_c.get("name")] = self.get_children_element(c_c,{},[],[])
			return map


	def get_element_hierachy(self,attr_name):
		dict = {}
		node = self.tree.find(attr_name)
		if node != None:
			c_dict = self.get_children_element(node,{},[],[])
			dict[attr_name] = c_dict
		else:
			test.info("the attribute:" + attr_name + " can't be found in mapping.cfg")
		return dict
	
	
	def get_children_tags(self):
		tags=[]
		root=self.tree.getroot()
		for element in root.getchildren():
			tags.append(element.tag)
		return tags