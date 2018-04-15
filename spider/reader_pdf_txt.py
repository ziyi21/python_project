#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

import os

def get_content_index(file_path):
    file = open(file_path)
    content_index = []
    key_word1 = ['前五','客户','销售']
    key_word1 = ['前五', '客户', '销售']

    for i,line in enumerate(file):
        if '前五' in line and '客户' in line and '销售' in line :
            content_index.append(i)
        elif '前五' in line and '供应商' in line and '采购' in line :
            content_index.append(i)
        elif '前五' in line and '供应商' in line and '关联' in line :
            content_index.append(i)
        elif '前五' in line and '客户' in line and '关联' in line :
            content_index.append(i)
        # elif '前五' in line and '应收款' in line:
        #     content_index.append (i)
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
    sz_txt_path = 'D:\\financial_reports\\sz_financial_reports\\sz_txt_all'
    sh_txt_path = 'D:\\financial_reports\\sh_financial_reports\\sh_txt_all'
    all_file_name = os.listdir(sz_txt_path)
    for file in all_file_name:
        save_analysis_path = 'D:\\financial_reports\\sz_financial_reports\\sz_txt_analysis'
        fname = os.path.splitext (file)[0]
        read_path = os.path.join (sz_txt_path, file)
        print(read_path)
        save_path = os.path.join(save_analysis_path,fname+'_analysis'+'.txt')
        print(save_path)
        index = get_content_index (read_path)
        get_main_content (read_path, index, save_path)

