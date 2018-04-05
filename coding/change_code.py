#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

import pandas as pd

data = pd.read_csv('movies_info.csv',encoding='utf-8')
data_list = list(data.values)
all_gbk = []
for i in data_list:
    one_gbk = []
    for m in range(len(i)):
        if type(i[m])== int or type(i[m])== float:
            one_gbk.append(i[m])
            continue
        i[m] = i[m].encode('gbk','ignore')
        one_gbk.append(i[m].decode('gbk'))
    all_gbk.append(one_gbk)

all_gbk = pd.DataFrame(all_gbk)
print(all_gbk)
header = ['编号','actor','image_url','index','real_time','time','title','total_booking']
all_gbk.to_csv('movies_info_gbk.csv',encoding='gbk',index=False,header=header)