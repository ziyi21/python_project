#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'


def get_content_index(file_path):
    file = open(file_path)
    content_index = []
    for i,line in enumerate(file):
        if '前五' in line and '客户' and '销售金额' in line :
            content_index.append(i)
        elif '前五' in line and '供应商' and '采购额' in line :
            content_index.append(i)
        elif '前五' in line and '供应商' and '关联' in line :
            content_index.append(i)
        elif '前五' in line and '客户' and '关联' in line :
            content_index.append(i)
        elif '前5' in line and '客户'  and '销售金额' in line:
            content_index.append (i)
        elif '前5' in line and '供应商'  and '采购额'in line:
            content_index.append (i)
        elif '前5' in line and '客户'  and '关联' in line:
            content_index.append (i)
        elif '前5' in line and '供应商'  and '关联'in line:
            content_index.append (i)
    print(content_index)
    file.close ()
    return content_index

def get_main_content(file_path,num,save_path):
    file = open (file_path)
    try:
        if num[0]:
            print(num[0])
            for j,content in enumerate(file):
                if j in range(num[0],num[-1]+100):
                    with open(save_path,'a') as f:
                        f.write(content + '\n')
            print ('有披露信息')
    except Exception as e:
        print('未披露相关内容')
        with open (save_path, 'a') as f:
            f.write ('0' + '\n')

if __name__ == '__main__':
    for i in [2012, 2013, 2014, 2015, 2016]:
        file_path = "data/{}_万科.txt".format (i)
        save_path = r'pdf_record/{}_simple_万科.txt'.format (i)
        index = get_content_index(file_path)
        get_main_content(file_path,index,save_path)