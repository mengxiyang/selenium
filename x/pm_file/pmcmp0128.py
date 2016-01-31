import datetime as pydateimport osimport xml.saximport loggingimport refrom optparse import OptionParserfrom collections import Counterfrom com.ericsson.xn.commons import PyProperties# npm_dir_root="/opt/xoam/data/northbound/pm/ready"run_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))npm_dir_root = os.path.join(run_dir, "ready")lic_counters_dir = run_dir + os.sep + "conf" + os.sep + "lic_counters"me_counters_dir = run_dir + os.sep + "conf" + os.sep + "me_counters"global logPMParserlogging.basicConfig(level=logging.DEBUG,                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',                    datefmt='%a, %d %b %Y %H:%M:%S',                    filename=os.path.join(os.getcwd(), 'Detail.log'),                    filemode='w')logPMParser = logging.getLogger('pmcmp.py')def find_pm_file(path, timestamp):    for i in os.listdir(path):        if (i.find(timestamp) != -1):            return i    else:        return "missing"def get_file_list():    if options.time == "":        nowtime = pydate.datetime.now()    else:        pm_time = options.time        nowtime = pydate.datetime.strptime(pm_time, "%Y%m%d%H%M")    npm_interval = options.interval    round = 60 / npm_interval    timeshift = nowtime.minute % npm_interval    filelist = {}    npm_dir = npm_dir_root + os.path.sep + options.nodeid    for i in range(1, round + 1):        timeshift += npm_interval        time_delta = nowtime + pydate.timedelta(minutes=-timeshift)        pm_timestamp = time_delta.strftime("%Y%m%d") + "-" + time_delta.strftime("%H%M")        pm_file = find_pm_file(npm_dir, pm_timestamp)        if (pm_file != "missing"):            filelist[time_delta.minute] = npm_dir + "/" + pm_file        i = i + 1    return filelistdef compare_pm(srcfile, baseInfo):    srcInfo = parse_xml_file(srcfile)    for a, b in baseInfo.items():        if (a == "FileHeader"):            for c, d in b.items():                if srcInfo[a].has_key(c) == True:                    if (srcInfo[a][c] != baseInfo[a][c]):                        logPMParser.error(srcfile + " data accuracy test failed.")                        logPMParser.error(                            "failed." + a + "/" + c + " value is " + srcInfo[a][c] + ", and the expected result is:" +                            baseInfo[a][c])                        return -1                else:                    logPMParser.error(srcfile + " data accuracy test failed.")                    logPMParser.error("attribute:" + a + "/" + c + " is missing.")                    return -1        elif (a == "PMData"):            for i, j in b.items():                if srcInfo[a].has_key(i) == True:                    for v1, v2 in j.items():                        if srcInfo[a][i].has_key(v1) == True:                            if srcInfo[a][i][v1] != baseInfo[a][i][v1]:                                logPMParser.error(srcfile + " data accuracy test failed.")                                logPMParser.error("PM counter:" + a + "/" + i + "/" + v1 + " value is " + str(                                    srcInfo[a][i][v1]) + ", and the expected result is:" + str(baseInfo[a][i][v1]))                                return -1                        else:                            logPMParser.error(srcfile + " data accuracy test failed.")                            logPMParser.error("PM counter:" + a + "/" + i + "/" + v1 + " is missing.")                            return -1                else:                    logPMParser.error(srcfile + " data accuracy test failed.")                    logPMParser.error("PM DN:" + a + "/" + i + " missing.")                    return -1    for a, b in srcInfo.items():        if (a == "FileHeader"):            for c, d in b.items():                if baseInfo[a].has_key(c) == False:                    logPMParser.error(srcfile + " accuracy test failed ")                    logPMParser.error("extra attribute:" + a + "/" + c + " in " + srcfile)                    return -1        elif (a == "PMData"):            for i, j in b.items():                if baseInfo[a].has_key(i) == False:                    logPMParser.error(srcfile + " accuracy test failed ")                    logPMParser.error("extra PM DN:" + a + "/" + i + " in " + srcfile)                    return -1                else:                    for v1, v2 in j.items():                        if baseInfo[a][i].has_key(v1) == False:                            logPMParser.error(srcfile + " accuracy test failed ")                            logPMParser.error("extra PM counter:" + a + "/" + i + "/" + v1 + " in " + srcfile)                            return -1class PMSaxHandler(xml.sax.ContentHandler):    def __init__(self):        xml.sax.ContentHandler.__init__(self)        logPMParser.info('SAX handler init.')        self.node = {}        self.isHeader = False        self.headerPara = {}        self.counters = {}        self.counter = ""        self.lics = {}        self.isLic = False        self.key = None        self.isCounter = False        self.dn = ""    def startElement(self, name, attrs):        if (name == "FileHeader"):            self.isHeader = True            logPMParser.info('Found a header information.')        elif (name == "Pm"):            self.isLic = True            self.dn = attrs["Dn"].strip().encode('utf-8')            logPMParser.info('Found a lic information.')        elif (name == "V"):            self.isCounter = True            self.counter = attrs["i"].strip().encode('utf-8')        self.key = name.strip().encode('utf-8')    def characters(self, content):        content = content.strip().encode('utf-8')        if (self.isHeader):            if ('FileHeader' != self.key and 'BeginTime' != self.key and 'EndTime' != self.key):                if (self.key is not None):                    self.headerPara[self.key] = content        elif (self.isLic and self.isCounter):            if ('V' == self.key):                if (self.key is not None):                    self.counters[self.counter] = int(content)    def endElement(self, name):        if (name == self.key):            self.key = None        if ('Pm' == name):            self.isLic = False            self.lics[self.dn] = self.counters            self.counters = {}        if ('FileHeader' == name):            self.isHeader = False        if ('V' == name):            self.isCounter = False    def endDocument(self):        self.node["FileHeader"] = self.headerPara        self.node["PMData"] = self.lics        logPMParser.info('End the parsing of XML.')def parse_xml_file(xmlpath):    parser = xml.sax.make_parser()    handler = PMSaxHandler()    parser.setContentHandler(handler)    parser.parse(open(xmlpath, 'r'))    return handler.nodedef get_options():    parser = OptionParser(usage="usage: %prog -t <netype> -n <nename> -o <nodeid> [-l <licid>] [-i <interval>] [-p <timestamp>]")    parser.add_option("-i", "--interval", action="store", type="int", dest="interval", default=15,                      help="specify the rop of northbound pm file[5|15]. The default rop is 15")    parser.add_option("-t", "--type", action="store", type="string", dest="ne_type", default="True",                      help="specify the netype")    parser.add_option("-n", "--nename", action="store", type="string", dest="nename", default="True",                      help="specify the nename")    parser.add_option("-o", "--nodeid", action="store", type="string", dest="nodeid", default="True",                      help="specify the nodeid")    parser.add_option("-l", "--licid", action="store", type="string", dest="licid", default="",                      help="specify the licId and no need for NEs of AS, IMSHSS and LTEHSS")    parser.add_option("-p", "--timestamp", action="store", type="string", dest="time", default="",                      help="specify the timestamp back from which to process the pm file[YYmmddHHMM]")    (options, args) = parser.parse_args()    if (options.ne_type == "True"):        print "-t is mandatory to input."        parser.print_help()        return -1    if (options.nename == "True"):        print "-n is mandatory to input."        parser.print_help()        return -1    if (options.nodeid == "True"):        print "-o is mandatory to input."        parser.print_help()        return -1    if (options.ne_type.lower() != 'sgsn' and options.ne_type.lower() != 'mme' and options.ne_type.lower() != 'sgw' and options.ne_type.lower() != 'pgw' and options.ne_type.lower() != 'as' and options.ne_type.lower() != 'sbc' and options.ne_type.lower() != 'imshss' and options.ne_type.lower() != 'ltehss'):        print "Only support NETYPE including SGSN,MME,SGW,PGW,AS,SBC,IMSHSS and LTEHSS."        parser.print_help()        return -1    if (options.interval % 5):        print "incorrect interval.It must be multiples of 5"        parser.print_help()        return -1    if options.time != "":        pattern = re.compile(r'\d{12}')        match = pattern.match(options.time)        if match == None:            print "The input pm_timestamp must be in format of YYmmddHHMM."            parser.print_help()            return -1    return optionsdef addtwodimdict(thedict, key_a, key_b, val):    if key_a in thedict:        thedict[key_a].update({key_b: val})    else:        thedict.update({key_a: {key_b: val}})def get_fileheader_data(inpath):    fileheader_map = PyProperties.Properties(inpath).dict_info()    fileheader_map["InfoModelReferenced"] = options.ne_type.upper() + "-PM-V1.0.0"    return fileheader_mapdef get_pm_data_lic(inpath, netype):    pm_counter_path = inpath    counters = {}    DNs = {}    oldtime = 0    pmdata_map = {}    data_map = PyProperties.Properties(inpath).dict_info()    for key, value in data_map.items():        if (netype.lower() == "as" or netype.lower() == "imshss" or netype.lower() == "ltehss"):            time, licid = key.split("-")            time = int(time)        else:            time = int(key)            licid = options.licid        # get counters info        counter_value = value.split(",")        for index in range(0, len(counter_value)):            counters[str(index + 1)] = int(counter_value[index])            index = index + 1        dn = "DC=Ericsson,SubNetwork=1,ManagedElement=" + options.nodeid + "|" + options.nename + ",L=" + licid        addtwodimdict(pmdata_map, time, dn, counters)        counters = {}    return pmdata_mapdef get_pm_data_me(inpath):    file_map = PyProperties.Properties(inpath).dict_info()    medata_map = {}    counters = {}    counters_value = []    for time, value in file_map.items():        time = int(time)        # get counters info        counter_value = value.split(",")        for index in range(0, len(counter_value)):            counters[str(index + 1)] = int(counter_value[index])            index = index + 1        dn = "DC=Ericsson,SubNetwork=1,ManagedElement=" + options.nodeid + "|" + options.nename        addtwodimdict(medata_map, time, dn, counters)        counters = {}    return medata_mapdef get_expect_result(netype):    baseInfo = {}    node = {}    fileheader_cfg_path = lic_counters_dir + os.sep + "fileheader.cfg"    lic_counters_cfg_path = lic_counters_dir + os.sep + netype + ".cfg"    me_counters_cfg_path = me_counters_dir + os.sep + netype + ".cfg"    fileheader_data = get_fileheader_data(fileheader_cfg_path)    lic_data = get_pm_data_lic(lic_counters_cfg_path, options.ne_type)    me_data = get_pm_data_me(me_counters_cfg_path)    time = 0    while time < 60:        node["FileHeader"] = fileheader_data        node["PMData"] = dict(lic_data[time].items() + me_data[time].items())        baseInfo[time] = node        node = {}        time = time + 5    return baseInfodef get_expect_result_multi_rop(netype):    current_rop = options.interval    circle_round = current_rop / 5    node_m = {}    node_5 = get_expect_result(netype)    node_m[0] = node_5[0]    time1 = 0    time2 = time1 + 5    while (time1 < 60):        while (time2 - time1 < 5 * circle_round):            pmdata_m = node_m[time1]["PMData"]            for lic, counters in pmdata_m.items():                if (node_5[time2]["PMData"].has_key(lic) == True):                    X, Y = Counter(node_5[time2]["PMData"][lic]), Counter(counters)                    z = dict(X + Y)                    pmdata_m[lic] = z            node_m[time1]["PMData"] = pmdata_m            time2 += 5        time1 += options.interval        if (time1 != 60):            node_m[time1] = node_5[time1]            time2 = time1 + 5    return node_mif __name__ == '__main__':    options = get_options()    if options == -1:        exit()    else:        nename = options.nename        nodeid = options.nodeid        licid = options.licid        netype = options.ne_type.lower()    npm_dir = npm_dir_root + os.path.sep + options.nodeid    if (not os.path.exists(npm_dir)):        os.makedirs(npm_dir)    if (options.interval == 5):        base_data = get_expect_result(netype)    else:        base_data = get_expect_result_multi_rop(netype)    srcfile = get_file_list()    len_src_file = len(srcfile.items())    if (len_src_file == 0):        print "no required pm files can be found in " + npm_dir        exit()    success_num = 0    fail_num = 0    print "Start PM comparing............"    for time, file in srcfile.items():        if base_data.has_key(time) == True:            flag = compare_pm(file, base_data[time])            if flag == -1:                fail_num += 1                print file + " accuracy test failed. For failed reason pls refer to Detail.log"            else:                success_num += 1                logPMParser.debug(file + " accuracy test success.")                print file + " accuracy test success"    print "Finish PM comparing. Total:" + str(len_src_file) + " files.Success:" + str(success_num) + " Fail:" + str(        fail_num)