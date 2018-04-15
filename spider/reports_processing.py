#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

import os

def create_reports_table(filename,path):
    analysis_data = {}
    with open(path) as f:
        for i in f :
            print(i)
            if '前五' in i and '客户' in i:
                analysis_data['five_customers'] = 0
    analysis_data['name'] = file_name
    analysis_data['time'] = file_name.split('_')[0]


if __name__ == '__main__':
    analysis_path = 'D:\\financial_reports\\sz_financial_reports\\sz_txt_analysis'
    all_file = os.listdir(analysis_path)
    for one in all_file:
        path = os.path.join(analysis_path,one)
        file_name = os.path.splitext(one)[0]
        print(path)
        create_reports_table(file_name,path)
