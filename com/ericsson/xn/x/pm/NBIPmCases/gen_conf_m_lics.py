
'''
Created on Feb 9, 2017

@author: eyyylll
'''
import sys
from fileinput import filename
import re

if __name__ == '__main__':

    file_name=sys.argv[1]
    inf = open(file_name,"r+")
    out_file = "./output.txt"

    i = 1
    time=0
    newlines=[]
    for line in inf.readlines():
        if i==33:
            i=1
            time=time+5
        lic_name = str(time)+"-LIC_LTE_"+str(i)+"="
        values = re.findall(r'\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+$',line)
        new_line = lic_name + values[0] +"\n"
        newlines.append(new_line)
        i=i+1

    of=open(out_file,"w+")
    of.writelines(newlines)
    of.close()
    inf.close()