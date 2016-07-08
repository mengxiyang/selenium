import sys

if __name__ == '__main__':
    counter_name_list=sys.argv[1].split(",")
    ne_type = sys.argv[2]
    data_type = sys.argv[3]
    start_time = sys.argv[4]
    end_time = sys.argv[5]
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
    print sql
    print ",".join(type_list)