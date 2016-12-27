import datetime as pydatefrom com.ericsson.xn.x.pm.PmCommons import NBIPmParserfrom com.ericsson.xn.commons import test_loggerimport osimport xml.saximport refrom optparse import OptionParserfrom com.ericsson.xn.commons import PyPropertiesfrom decimal import *class PMCmpInstance:    def __init__(self,netype="",nename="",nodeid="",licid="",interval=15,time="",path=""):                  self.options={"ne_type":netype.lower(),"nename":nename,"nodeid":nodeid,"licid":licid,"interval":interval,"time":time}                 root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__))).split('com' + os.sep + 'ericsson' + os.sep + 'xn' + os.sep + 'x' + os.sep + 'pm' + os.sep + 'PmCommons')[0]            #self.npm_dir = root_dir + os.sep + "x" + os.sep + "pm_file" + os.sep + "ready" + os.sep + nodeid            if path=="":                self.npm_dir = root_dir + os.sep + "x" + os.sep + "pm_file" + os.sep + "ready" + os.sep + nodeid            else:                self.npm_dir=os.path.normpath(path)            self.npm_filelist = sorted(os.listdir(self.npm_dir),cmp)            self.lic_counters_dir = root_dir + "x" + os.sep + "pm_file" + os.sep + "conf" + os.sep + "lic_counters" + os.sep + netype.lower() + ".cfg"            self.me_counters_dir = root_dir  + "x" + os.sep + "pm_file" + os.sep + "conf" + os.sep + "me_counters" + os.sep + netype.lower() + ".cfg"            self.fileheader_counters_dir=root_dir  + "x" + os.sep + "pm_file" + os.sep + "conf" + os.sep + "lic_counters" + os.sep + "fileheader.cfg"            self.counter_properties_dir  = root_dir  + "x" + os.sep + "pm_file" + os.sep + "conf" + os.sep + "counter_properties" + os.sep + netype.lower() + ".cfg"                            #test_logger.init_logger_instance("check_nbi_pm_"+netype.lower()+"_rop="+str(interval)+"_cases", "nbi_pm_automation")                        if(not os.path.exists(self.npm_dir)):                test_logger.logger_instance.log_error("The NBI PM northbound folder:" + self.npm_dir_root + " not existed.")                        if(not os.path.exists(self.lic_counters_dir)):                test_logger.logger_instance.log_error("The configuration file:" + self.lic_counters_dir +" not existed.")                            if(not os.path.exists(self.me_counters_dir)):                test_logger.logger_instance.log_error("The configuration file:" + self.me_counters_dir + " not existed.")                        if(not os.path.exists(self.fileheader_counters_dir)):                test_logger.logger_instance.log_error("The configuration file:" + self.fileheader_counters_dir + " not existed.")                            if(not os.path.exists(self.counter_properties_dir)):                test_logger.logger_instance.log_error("The configuration file:" + self.counter_properties_dir  + " not existed.")                                        self.check_options()            self.counter_properties = self.load_counter_properties(self.counter_properties_dir)            self.pmdata_lic_5=self.get_pm_data_lic()            self.pmdata_me_5=self.get_pm_data_me()            self.pmdata_fileheader_5=self.get_fileheader_data()                   def load_counter_properties(self,path):        counter_properties = PyProperties.Properties(path).dict_info()        return counter_properties        def get_counter_multi_algorithm(self,counter_properties,counter_name,type):        if(type == "lic"):            return counter_properties["lic_multi_algorithm"].split(",")[counter_name]        elif(type == "me"):            return counter_properties["me_multi_algorithm"].split(",")[counter_name]        def get_counter_datatype(self,counter_properties,counter_name,type):        if(type == "lic"):            return counter_properties["lic_counter_datatype"].split(",")[counter_name]        elif(type == "me"):            return counter_properties["me_counter_datatype"].split(",")[counter_name]        def convert_datatype(self,data_type, data_value):        if data_value != "":            if data_type == "int":                data_value = int(data_value)            elif data_type == "float":                data_value = Decimal("%.2f"%data_value)        else:            data_value = ""        return data_value    def sum_counter(self,DN,counter_name,counter_value,time,datatype):        if(datatype=="lic"):            pmdata_5=self.pmdata_lic_5        elif(datatype=="me"):            pmdata_5=self.pmdata_me_5            round = self.options["interval"]/5        null_count = 0            for i in range(1,round):               nexttime=time+5            next_counter =  pmdata_5[nexttime][DN][counter_name]            if(nexttime==60):                nexttime=0            if counter_value == "":                null_count = null_count + 1                counter_value = 0            if next_counter == "":                next_counter = 0                null_count = null_count + 1            counter_value = counter_value + next_counter            time=time+5            i=i+1        if null_count == 3:            counter_value = ""        return counter_value        def avg_counter(self,DN,counter_name,counter_value,time,datatype):        sum_value = self.sum_counter(DN,counter_name,counter_value,time,datatype)        if sum_value != "":            round = self.options["interval"]/5            avg_value=sum_value/round            avg_value = Decimal("%.2f"%avg_value)        else:            avg_value = ""        return avg_value        def last_counter(self,DN,counter_name,counter_value,time,datatype):        if(datatype=="lic"):            pmdata_5=self.pmdata_lic_5        elif(datatype=="me"):            pmdata_5=self.pmdata_me_5        round=self.options["interval"]/5        for i in range(1,round):               nexttime=time+5            if(nexttime==60):                nexttime=0            new_value = pmdata_5[nexttime][DN][counter_name]            time=time+5            i=i+1        return new_value        def max_counter(self,DN,counter_name,counter_value,time,datatype):        if(datatype=="lic"):            pmdata_5=self.pmdata_lic_5        elif(datatype=="me"):            pmdata_5=self.pmdata_me_5                round=self.options["interval"]/5        null_count = 0        if counter_value == "":            counter_value = 0            null_count = null_count + 1        new_value = counter_value        for i in range(1,round):               nexttime=time+5            if(nexttime==60):                nexttime=0            if counter_value == "":                counter_value = 0                null_count = null_count + 1            next_counter = pmdata_5[nexttime][DN][counter_name]            if next_counter == "":                next_counter = 0                null_count = null_count + 1            if (counter_value < next_counter ):                new_value= next_counter            time=time+5            i=i+1        if null_count == 3:            new_value = ""        return new_value        def cmp(self,x, y):        stat_x = os.stat(self.npm_dir + os.sep + x)        stat_y = os.stat(self.npm_dir + os.sep + y)        if stat_x.st_ctime < stat_y.st_ctime:            return -1        elif stat_x.st_ctime > stat_y.st_ctime:            return 1        else:            return 0                    def find_xml_file(self,timestamp):        for i in self.npm_filelist:            if (i.find(timestamp) != -1):                return i        else:            print "pm file for " + timestamp + " missing!"            return "missing"        def get_file_list(self):        if self.options["time"] == "":            nowtime = pydate.datetime.now()        else:            pm_time = self.options["time"]            nowtime = pydate.datetime.strptime(pm_time, "%Y%m%d%H%M")        npm_interval = self.options["interval"]        round = 60 / npm_interval        timeshift = nowtime.minute % npm_interval        filelist = {}        npm_dir = self.npm_dir                        for i in range(1, round + 1):            time_delta = nowtime + pydate.timedelta(minutes=-timeshift)            pm_timestamp = time_delta.strftime("%Y%m%d") + "-" + time_delta.strftime("%H%M")            pm_file = self.find_xml_file(pm_timestamp)            if (pm_file != "missing"):                filelist[time_delta.minute] = npm_dir + "/" + pm_file            i = i + 1            timeshift += npm_interval        return filelist        def compare_data(self,srcfile,baseInfo):        srcInfo = NBIPmParser.parse_xml_file(srcfile)        for a, b in baseInfo.items():            if (a == "FileHeader"):                for c, d in b.items():                    if srcInfo[a].has_key(c) == True:                        if (str(srcInfo[a][c]) != str(baseInfo[a][c])):                                                    test_logger.logger_instance.log_failed("PM counter:" + a + "/" + c + " value is " + srcInfo[a][c] + ", and the expected result is:" + baseInfo[a][c])                                                    else:                            test_logger.logger_instance.log_passed("PM counter:" + a + "/" + c + " Passed. The NBI value is " + srcInfo[a][c] + ", and the expected result is " + baseInfo[a][c])                                                                        else:                        test_logger.logger_instance.log_failed("PM counter:" + a + "/" + c + " is missing.")            elif (a == "PMData"):                for i, j in b.items():                    if srcInfo[a].has_key(i) == True:                        for v1, v2 in j.items():                            if srcInfo[a][i].has_key(v1) == True:                                if str(srcInfo[a][i][v1]) != str(baseInfo[a][i][v1]):                                                                        test_logger.logger_instance.log_failed("PM counter:" + a + "/" + i + "/" + v1 + " value is " + str(srcInfo[a][i][v1]) + ", and the expected result is:" + str(baseInfo[a][i][v1]))                                else:                                    test_logger.logger_instance.log_passed("PM counter:" + a + "/" + i + "/" + v1 + " Passed. The NBI value is " + str(srcInfo[a][i][v1]) + ", and the expected result is " + str(baseInfo[a][i][v1]))                                                            else:                                test_logger.logger_instance.log_failed("PM counter:" + a + "/" + i + "/" + v1 + " is missing.")                                                else:                                            test_logger.logger_instance.log_failed("PM DN:" + a + "/" + i + " missing.")                            for a, b in srcInfo.items():            if (a == "FileHeader"):                for c, d in b.items():                    if baseInfo[a].has_key(c) == False:                                            test_logger.logger_instance.log_failed("Extra PM counter:" + a + "/" + c)            elif (a == "PMData"):                for i, j in b.items():                    if baseInfo[a].has_key(i) == False:                                            test_logger.logger_instance.log_failed("Extra PM DN:" + a + "/" + i)                                        else:                        for v1, v2 in j.items():                            if baseInfo[a][i].has_key(v1) == False:                                                            test_logger.logger_instance.log_failed("Extra PM counter:" + a + "/" + i + "/" + v1)    def addtwodimdict(self,thedict, key_a, key_b, val):        if key_a in thedict:            thedict[key_a].update({key_b: val})        else:            thedict.update({key_a: {key_b: val}})    def get_fileheader_data(self):        fileheader_path=self.fileheader_counters_dir        fileheader_data = PyProperties.Properties(fileheader_path).dict_info()        if(self.options["ne_type"]=="imshss" or self.options["ne_type"] == "ltehss"):            fileheader_data["InfoModelReferenced"] = "HSS" + "-PM-V1.0.0"        elif (self.options["ne_type"].lower() == "3gsgsn"):            fileheader_data["InfoModelReferenced"] = "SGSN" + "-PM-V1.0.0"        elif (self.options["ne_type"].lower() == "ocgas"):            fileheader_data["InfoModelReferenced"] = "AS" + "-PM-V1.0.0"        else:                 fileheader_data["InfoModelReferenced"] = self.options["ne_type"].upper() + "-PM-V1.0.0"        return fileheader_data    def get_pm_data_lic(self):        counter_properties = self.counter_properties        lic_counters= PyProperties.Properties(self.lic_counters_dir).dict_info()            netype = self.options["ne_type"]            counters = {}        pmdata_lic = {}            for key, value in lic_counters.items():            if netype in ("ocgas","imshss","ltehss","gmlc","msc","hlr","3gsgsn","ggsn"):                time, licid = key.split("-")                time = int(time)            else:                time = int(key)                licid = self.options["licid"]                    # get counters info            counter_value = value.split(",")            for index in range(0, len(counter_value)):                if(counter_value[index]=="\N" or counter_value[index] == "no traffic" ):                    counters[str(index + 1)] = ""                elif(self.get_counter_datatype(counter_properties, index, "lic").strip() == "int"):                    counters[str(index + 1)] = int(counter_value[index])                elif(self.get_counter_datatype(counter_properties, index, "lic") == "float"):                    #StrToFloat=float(counter_value[index])                    counters[str(index+1)] = Decimal("%.2f"%Decimal(counter_value[index]))                                index = index + 1            dn = "DC=Ericsson,SubNetwork=1,ManagedElement=" + self.options["nodeid"] + "|" + self.options["nename"] + ",L=" + licid            self.addtwodimdict(pmdata_lic, time, dn, counters)            counters = {}        return pmdata_lic    def get_pm_data_me(self):        counter_properties = self.counter_properties         me_counters = PyProperties.Properties(self.me_counters_dir).dict_info()        pmdata_me={}        counters = {}        counters_value = []            for time, value in me_counters.items():            time = int(time)            # get counters info            counter_value = value.split(",")            for index in range(0, len(counter_value)):                if(counter_value[index]=="\N" or counter_value[index] == "no traffic"):                    counters[str(index + 1)] = ""                elif(self.get_counter_datatype(counter_properties, index, "me") == "int"):                    counters[str(index + 1)] = int(counter_value[index])                elif(self.get_counter_datatype(counter_properties, index, "me") == "float"):                    counters[str(index+1)] = Decimal("%.2f"%Decimal(counter_value[index]))                                index = index + 1            dn = "DC=Ericsson,SubNetwork=1,ManagedElement=" + self.options["nodeid"] + "|" + self.options["nename"]            self.addtwodimdict(pmdata_me, time, dn, counters)            counters = {}        return pmdata_me    def get_counter_name_map(self,counter_properties,datatype):        counter_map={}        if(datatype == "lic"):            counter_name_list =counter_properties["lic_counter_name"].split(",")        elif(datatype == "me"):            counter_name_list = counter_properties["me_counter_name"].split(",")        if(datatype == "lic"):                    i=1            for counters in counter_name_list:                if counters.find('-')!=-1:                    name=counters.split("-")[0][0]                    start=int(counters.split("-")[0][1:])                    end=int(counters.split("-")[1][1:])                    for index in range(start,end+1):                        counter_map[str(i)]=name+str(index)                        index=index+1                        i=i+1                else:                    counter_map[str(i)]=counters                    i=i+1        elif(datatype == "me"):            i=1            for counter in counter_name_list:                counter_map[str(i)]=counter                i=i+1        return counter_map                    def update_counter_name_to_real(self,counter_properties,pmdata,datatype):        counter_name_map=self.get_counter_name_map(counter_properties,datatype)        for time,lics in pmdata.items():            for DN,counters in lics.items():                for counter_name, counter_value in counters.items():                    if (counter_name_map.has_key(counter_name)):                        del counters[counter_name]                        counters.update({counter_name_map[counter_name]:counter_value})            del pmdata[time][DN]            pmdata[time].update({DN:counters})        return pmdata                def get_expect_result(self):        expect_data = {}         node = {}          fileheader_data = self.pmdata_fileheader_5        lic_data = self.pmdata_lic_5        me_data = self.pmdata_me_5        counter_properties=self.counter_properties        lic_data=self.update_counter_name_to_real(counter_properties,lic_data,"lic")        me_data=self.update_counter_name_to_real(counter_properties,me_data,"me")        time = 0        while time < 60:            node["FileHeader"] = fileheader_data            node["PMData"] = dict(lic_data[time].items() + me_data[time].items())            expect_data[time] = node            node = {}            time = time + 5        return expect_data    def get_expect_result_multi(self):        node_m = {}        expect_data_m ={}        fileheader_data_5 = self.pmdata_fileheader_5        lic_data_5 = self.pmdata_lic_5        me_data_5 = self.pmdata_me_5        counter_properties = self.counter_properties        interval=self.options["interval"]        lic_data_m = self.multi_calculator(counter_properties,lic_data_5, "lic",interval)        me_data_m = self.multi_calculator(counter_properties,me_data_5,"me",interval)        fileheader_data_m = fileheader_data_5        lic_data_m=self.update_counter_name_to_real(counter_properties,lic_data_m,"lic")        me_data_m=self.update_counter_name_to_real(counter_properties,me_data_m, "me")                time=0        while(time<60):            node_m["PMData"] = dict(lic_data_m[time].items() + me_data_m[time].items())            node_m["FileHeader"] = fileheader_data_m                    expect_data_m[time] = node_m            node_m = {}            time = time + self.options["interval"]        return expect_data_m    def multi_calculator(self,counter_properties,pmdata_5,datatype,interval):           new_counters={}        pmdata_m={}            time=0        while time<60:            pmdata=pmdata_5[time]            for DN, counters in pmdata.items():                for counter_name, counter_value in counters.items():                    if(self.get_counter_multi_algorithm(counter_properties,int(counter_name)-1,datatype).strip()=="sum"):                        datatype_c = self.get_counter_datatype(counter_properties,int(counter_name)-1,datatype).strip()                        value = self.sum_counter(DN,counter_name,counter_value,time,datatype)                        new_counters[counter_name]=self.convert_datatype(datatype_c,value)                    elif(self.get_counter_multi_algorithm(counter_properties,int(counter_name)-1,datatype) == "avg"):                        datatype_c = self.get_counter_datatype(counter_properties,int(counter_name)-1,datatype).strip()                        value = self.avg_counter(DN,counter_name,counter_value,time,datatype)                        new_counters[counter_name]=self.convert_datatype(datatype_c,value)                    elif(self.get_counter_multi_algorithm(counter_properties,int(counter_name)-1,datatype)=="last"):                        datatype_c = self.get_counter_datatype(counter_properties,int(counter_name)-1,datatype).strip()                        value = self.last_counter(DN,counter_name,counter_value,time,datatype)                        new_counters[counter_name]=self.convert_datatype(datatype_c,value)                    elif(self.get_counter_multi_algorithm(counter_properties,int(counter_name)-1,datatype) =="max"):                        datatype_c = self.get_counter_datatype(counter_properties,int(counter_name)-1,datatype).strip()                        value = self.max_counter(DN,counter_name,counter_value,time,datatype)                        new_counters[counter_name]=self.convert_datatype(datatype_c,value)                self.addtwodimdict(pmdata_m, time, DN, new_counters)                new_counters={}            time= time+ interval                return pmdata_m    def check_options(self):                 if (self.options["ne_type"] == ""):            test_logger.logger_instance.log_error("netype is mandatory to input.")        if (self.options["nename"] == ""):            test_logger.logger_instance.log_error("nename is mandatory to input.")        if (self.options["nodeid"] == ""):            test_logger.logger_instance.log_error("nodeid is mandatory to input.")        if self.options["ne_type"].lower() not in ('sgsn','mme','sgw','pgw','ocgas','sbc','imshss','ltehss','gmlc','msc','hlr','3gsgsn','ggsn'):            test_logger.logger_instance.log_error("Only support SGSN,MME,SGW,PGW,OCGAS,SBC,IMSHSS,LTEHSS,GMLC,MSC,HLR,3GSGSN and GGSN.")        if (self.options["interval"] % 5):            test_logger.logger_instance.log_error("incorrect interval.It must be multiples of 5")        if self.options["time"] != "":            pattern = re.compile(r'\d{12}')            match = pattern.match(self.options["time"])            if match == None:                test_logger.logger_instance.log_error("The input pm_timestamp must be in format of YYmmddHHMM.")                    if (self.options["ne_type"].lower() in  ('ocgas','imshss','ltehss','gmlc','msc','hlr','3gsgsn','ggsn')):            if(self.options["licid"]!=""):                test_logger.logger_instance.log_error("No need to input LICID for OCGAS,IMSHSS,LTEHSS,GMLC,MSC,HLR,3GSGSN and GGSN")        else:            if(self.options["licid"]==""):                test_logger.logger_instance.log_error("Pls input the LICID for netype" + self.options["ne_type"])                    def check_pm_accuracy(self):          srcfile = self.get_file_list()        len_src_file = len(srcfile.items())        if (len_src_file == 0):            test_logger.logger_instance.log_error("NO Required pm files can be found in " + self.npm_dir)        if (self.options["interval"] == 5):            expect_data = self.get_expect_result()        else:            expect_data = self.get_expect_result_multi()                for time, file in srcfile.items():            if expect_data.has_key(time) == True:                test_logger.logger_instance.log_info("check pm file " + file)                self.compare_data(file, expect_data[time])