#encoding=utf-8
'''
Created on Aug 24, 2015

@author: lowitty
'''
import os
import re
from com.ericsson.xn.commons import test_logger


class Properties():
    
    def __init__(self, propertyFile):
        self.path = os.path.normpath(propertyFile)
        if(not os.path.isfile(self.path)):
            raise IOError("The path that you specified is not a file.")
        else:
            self.file = open(self.path, 'rb')
            lines = self.file.readlines()
            self.mappings = {}
            for line in lines:
                keyValue = line.split('=',1)
                if(len(keyValue) > 1):
                    self.mappings[keyValue[0]] = keyValue[1].strip()
            self.file.close()
                    
    def getProperty(self, key):
        if(self.mappings.has_key(key)):
            if(len(re.findall(r"(.+:(?!\\).+)",self.mappings[key]))>=1):
                dict_values={}
                for item in re.findall(r"(.+:(?!\\).+)",self.mappings[key])[0].split(","):
                    dict_values[item.split(":")[0]]=item.split(":")[1]
                return dict_values
            elif(len(re.findall(r".+,",self.mappings[key]))>=1):
                list_values=[]
                for item in self.mappings[key].split(","):
                    list_values.append(item)
                return  list_values
            else:
                return self.mappings[key]
        else:
            return None
        
    def setProperty(self, key, value):
        if(self.mappings.has_key(key)):
            self.mappings[key] = value

    def dict_info(self):
        return self.mappings
            
    def store(self):
        if(not os.path.isfile(self.path)):
            raise IOError("The path that you specified is not a file.")
        else:
            lKeyValue = []
            for key, value in self.mappings.iteritems():
                lKeyValue.append(key + '=' + value + '\n')
            f = open(self.path, 'wb')
            f.writelines(lKeyValue)
            f.flush()
            f.close()
                    

class TrimableProps:
    def __init__(self, prop_file, is_strip=True, str_split='='):
        self.path = os.path.normpath(prop_file)
        if not os.path.isfile(self.path):
            raise IOError("The path that you specified is not a file.")
        else:
            self.file = open(self.path, 'r+')
            lines = self.file.readlines()
            self.mappings = {}
            for line in lines:
                if not line.lstrip().startswith('#'):
                    key_value = line.split(str_split, 1)
                    if 1 < len(key_value):
                        if is_strip:
                            self.mappings[key_value[0].strip()] = key_value[1].strip()
                        else:
                            self.mappings[key_value[0]] = key_value[1]
            self.file.close()

    def getProperty(self, key):
        if self.mappings.has_key(key):
            return self.mappings[key]
        else:
            return None

    def setProperty(self, key, value):
        if self.mappings.has_key(key):
            self.mappings[key] = value

    def store(self):
        if not os.path.isfile(self.path):
            raise IOError("The path that you specified is not a file.")
        else:
            lkey_value = []
            for key, value in self.mappings.iteritems():
                lkey_value.append(key + '=' + value + '\n')
            f = open(self.path, 'wb')
            f.writelines(lkey_value)
            f.flush()
            f.close()

    def get_map(self):
        return self.mappings

    def dict_info(self):
        return self.mappings