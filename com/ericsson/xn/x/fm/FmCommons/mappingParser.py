
import xml.etree.ElementTree as ET
import os


root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__))).split('com' + os.sep + 'ericsson' + os.sep + 'xn' + os.sep + 'x' + os.sep + 'fm' + os.sep + 'FmCommons')[0]
mapping_cfg = root_dir + os.sep + 'x' + os.sep + 'fm' + os.sep + 'nbi_mapping' + os.sep + 'ne_new_alarm.cfg'


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


def get_element_map(tree,name):
	node = tree.find(name)
	if node != None:
		c_dict = get_children_element(node,{},[],[])
		dict = {}
		dict[name] = c_dict
		return dict
	else:
		print "the attribute" + name + "not exist"



if __name__ == '__main__':
	tree = ET.parse(mapping_cfg)
	dict_event_name = get_element_map(tree,"event_name")
	dict_event_time= get_element_map(tree,"b")
	dict_w = get_element_map(tree,"w")
	dict_e = get_element_map(tree,"e")

	print dict_event_name, dict_event_time,dict_w,dict_e
