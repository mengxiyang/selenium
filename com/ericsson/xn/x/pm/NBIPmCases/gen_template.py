import sys

def gen_sql(counter_name,ne_type,data_type,start_time,end_time):
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
    return sql + "\n" + ",".join(type_list)

print gen_sql(counter_name='Memtotal,Nettotal3,CpuUsageMean,CpuUsagePeak,MemUsageMean,MemUsagePeak,NetUsageMean3,NetUsagePeak3',ne_type='msc',data_type='me',start_time='2016-07-21 12:00:00',end_time='2016-07-21 12:55:00')