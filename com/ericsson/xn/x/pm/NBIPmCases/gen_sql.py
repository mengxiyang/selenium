import sys

def gen_sql(counter_name,ne_type,data_type,start_time,end_time=None):
    counter_name_list=counter_name.split(",")
    counter_list=[]
    type_list=[]
    for counters in counter_name_list:
        if counters.find('-')!=-1:
            name=counters.split("-")[0][0]
            start=int(counters.split("-")[0][1:])
            end=int(counters.split("-")[1][1:])
            for index in range(start,end+1):
                counter_list.append(name+str(index))
                type_list.append("int")
                index=index+1
        else:
            counter_list.append(counters)
            type_list.append("int")
    sql= "select " + ",".join(counter_list) + " into outfile '/opt/xoam/" + ne_type + "_" + data_type + ".cfg' fields terminated by ',' from pm_" + ne_type + "_" + data_type + " where start_time>='" + start_time + "' and start_time<='" + end_time +"';"
#   gen sql for IMSHSS and LTEHSS multiple LICs
#   sql = "select substring(lic_id,9,3) as abstract," + ",".join(counter_list) + " into outfile '/opt/xoam/" + ne_type + "_" + data_type + ".cfg' fields terminated by ',' from pm_" + ne_type + "_" + data_type + " where start_time='" + start_time + "' order by --abstract asc ;"

    return sql + "\n" + ",".join(type_list)

print gen_sql(counter_name='A1-A22',ne_type='gmlc',data_type='lic',start_time='2017-02-21 08:00:00',end_time='2017-02-21 08:55:00')
#print for IMSHSS and LTEHSS multiple LICs
#print gen_sql(counter_name='F1-F4,G1-G4',ne_type='imshss',data_type='lic',start_time='2017-02-08 12:00:00')