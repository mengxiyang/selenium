import xml.sax
from decimal import *

class PMNBIHander(xml.sax.ContentHandler):
    def __init__(self):

        xml.sax.ContentHandler.__init__(self)

        self.node = {}

        self.lics = {}

        self.mes = {}

        self.isHeader = False

        self.headerPara = {}

        self.isPmName = False

        self.isPMData = False

        self.isName = False

        self.lic_names = {}

        self.me_names = {}

        self.pmdata = {}

        self.isDN = False

        self.isValue = False

        self.lic_values = {}

        self.me_values = {}

        self.value_index = ""

        self.name_index = ""

        self.isObjectType = False

        self.isLic = False

        self.isME = False

        self.counter = ""

        self.isObjectType = False

        self.isME = False

        self.isPmName = False

        self.key = None
        
        self.hasValue = False

        self.dn = ""

        self.isMeasurement = False



    def startElement(self, name, attrs):

        if (name == "FileHeader"):
            self.isHeader = True

        elif(name == "Measurements"):
            self.isMeasurement = True

        elif(name == "ObjectType"):
            self.isObjectType = True

        elif(name == "PmName"):
            self.isPmName = True
        
        elif(name == "N"):
            self.isName = True
            self.name_index = attrs["i"].strip().encode('utf-8')

        elif(name == "PmData"):
            self.isPMData = True

        elif (name == "Pm"):
            self.isDN = True
            self.dn = attrs["Dn"].strip().encode('utf-8')

        elif (name == "V"):
            self.isValue = True
            self.value_index = attrs["i"].strip().encode('utf-8')


        self.key = name.strip().encode('utf-8')

    def characters(self, content):

        content = content.strip().encode('utf-8')


        if (self.isHeader):
            if (self.key != 'FileHeader' and self.key != 'BeginTime' and self.key != 'EndTime'):
                if (self.key is not None):
                    self.headerPara[self.key] = content

        elif (self.isObjectType and self.key is not None):
            if content == "ME":
                self.isME = True
            elif content == "L":
                self.isLic = True

        elif (self.isPmName and self.isName and self.isLic):
            if(self.key == "N" and self.key is not None):
                self.lic_names[self.name_index] = content

        elif (self.isPmName and self.isName and self.isME):
            if(self.key == "N" and self.key is not None):
                self.me_names[self.name_index] = content

        elif (self.isDN and self.isValue and self.isLic):
            if (self.key == 'V' and self.key is not None):
                if (content.find(".")==-1):
                    self.lic_values[self.value_index] = int(content)
                else:
                    self.lic_values[self.value_index] = Decimal(content)

                self.hasValue = True

        elif (self.isDN and self.isValue and self.isME):
            if (self.key == "V" and self.key is not None):
                if (content.find(".")==-1):
                    self.me_values[self.value_index] = int(content)
                else:
                    self.me_values[self.value_index] = Decimal(content)

                self.hasValue = True


    def endElement(self, name):

        if (name == self.key):
            self.key = None

        if(name == "Measurements"):
            self.isMeasurement = False
            if(self.isLic):
                self.isLic = False
            elif(self.isME):
                self.isME = False

        if(name == "ObjectType"):
            self.isObjectType = False

        if (name == 'FileHeader'):
            self.isHeader = False

        if (name == 'PmName'):
            self.isPmName = False

        if (name == 'Pm'):
            self.isDN = False
            if(self.isLic):
                self.lics[self.dn] = self.lic_values
                self.lic_values = {}
            elif(self.isME):
                self.mes[self.dn] = self.me_values
                self.me_values={}

        if (name == 'V'):
            self.isValue = False
            if(self.hasValue == False):
                if(self.isLic):
                    self.lic_values[self.value_index]=""
                elif(self.isME):
                    self.me_values[self.value_index]=""
            self.hasValue = False

        if (name == "N"):
            self.isName = False

        if(name == "PmData"):
            self.isPMData = False
            if(self.isLic):
                for DN, counters in self.lics.items():
                    for counter_index, counter_value in counters.items():
                        if(self.lic_names.has_key(counter_index)):
                            del self.lics[DN][counter_index]
                            self.lics[DN].update({self.lic_names[counter_index]:counter_value})
                self.pmdata.update(self.lics)
                self.lics={}
            elif(self.isME):
                for DN, counters in self.mes.items():
                    for counter_index,counter_value in counters.items():
                        if(self.me_names.has_key(counter_index)):
                            del self.mes[DN][counter_index]
                            self.mes[DN].update({self.me_names[counter_index]:counter_value})
                self.pmdata.update(self.mes)
                self.mes={}

                

    def endDocument(self):

        self.node["FileHeader"] = self.headerPara

        self.node["PMData"] = self.pmdata



def parse_xml_file(xmlpath):
    parser = xml.sax.make_parser()

    handler = PMNBIHander()

    parser.setContentHandler(handler)

    parser.parse(open(xmlpath, 'r'))

    return handler.node