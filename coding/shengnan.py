#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

import os
import pandas as pd
import re


def read_pdf(path):
    list_2015 = []
    list_2014 = []
    list_2013 = []
    for dirpath, dirnames, filenames in os.walk (path):
        fileinfor = {}
        # print(filenames)
        for filename in filenames:
            # print('one',one)
            if '2015' in filename:
                filepath = dirpath + r'\\' + filename
                list_2015.append (filepath)
            if '2014' in filename:
                filepath = dirpath + r'\\' + filename
                list_2014.append (filepath)
            if '2013' in filename:
                filepath = dirpath + r'\\' + filename
                list_2013.append (filepath)
    return list_2015, list_2014, list_2013

def handle_2015(list_2015):
    j = 0
    m = 0
    n = 0
    factors = {}
    df = pd.DataFrame ({})
    for index, one in enumerate (list_2015):
        with open (one, 'r', encoding='utf8', errors='ignore') as f:
            content = f.readlines ()
            for i, line in enumerate (content):
                # print(line)

                if '第四节管理层讨论与分析' in line.replace (' ', '') and len (line.replace (' ', '')) < 13:
                    j = j + 1
                    # print('j',j)
                    # print(i,line.replace(' ',''),one)
                    factors["filepath"] = one
                    factors['filename'] = one.split ('\\')[-1].split ('：')[0]
                    factors['filetime'] = one.split ('\\')[-1].split ('：')[-1].split ('年')[0]
                    factors['firstindex'] = int (i)

                if '公司未来发展的展望' in line.replace (' ', '') and len (line.replace (' ', '')) < 13:
                    m = m + 1
                    # print('m',m)
                    # print(i,line.replace(' ',''),one)
                    factors['secondindex'] = int (i)



                if '第五节重要事项' in line.replace (' ', '') and len (line.replace (' ', '')) < 9:
                    n = n + 1
                    # print('n',n)
                    # print(i,line.replace(' ',''),one)
                    factors['thirdindex'] = int (i)
            print (index, factors)
            df = df.append (factors, ignore_index=True)
    # df.to_csv(r'data\index_2015.csv', encoding='gbk')
    return df

def handle_2013(list_2013):
    j = 0
    m = 0
    n = 0
    factors = {}
    df = pd.DataFrame ({})
    for index, one in enumerate (list_2013):
        with open (one, 'r', encoding='utf8', errors='ignore') as f:
            factors['firstindex'] = 0
            factors['secondindex'] = 0
            factors['thirdindex'] = 0
            content = f.readlines ()
            for i, line in enumerate (content):
                # print(line)
                if '第四节董事会报告' in line.replace (' ', '') and len (line.replace (' ', '')) < 10:
                    j = j + 1
                    # print('j',j)
                    # print(i,line.replace(' ',''),one)
                    factors["filepath"] = one
                    factors['filename'] = one.split ('\\')[-1].split ('：')[0]
                    factors['filetime'] = one.split ('\\')[-1].split ('：')[-1].split ('年')[0]
                    factors['firstindex'] = int (i)
                if '第三节董事会报告' in line.replace (' ', '') and len (line.replace (' ', '')) < 10:
                    j = j + 1
                    # print('j',j)
                    # print(i,line.replace(' ',''),one)
                    factors["filepath"] = one
                    factors['filename'] = one.split ('\\')[-1].split ('：')[0]
                    factors['filetime'] = one.split ('\\')[-1].split ('：')[-1].split ('年')[0]
                    factors['firstindex'] = int (i)

                if '公司未来发展的展望' in line.replace (' ', '') and len(line.replace (' ', '')) < 30:
                    m = m + 1
                    # print('m',m)
                    # print(i,line.replace(' ',''),one)
                    factors['secondindex'] = int (i)

                #
                # if '三、公司未来发展的展望' in line.replace (' ', '') and len(line.replace (' ', '')) < 13:
                #     m = m + 1
                #     # print('m',m)
                #     # print(i,line.replace(' ',''),one)
                #     factors['secondindex'] = int (i)


                if '三、董事会、监事会对会计师事务所本报告期“非标准审计报告”的说明' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '三、公司利润分配及分红派息情况' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '三、董事会关于报告期会计政策、会计估计变更或重要前期差错更正的说明' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '三、董事会对会计师事务所本报告期“非标准审计报告”的说明' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '三、报告期财务会计报告审计情况及会计政策、会计估计变更以及会计差错更正的说明' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)


                if '四、董事会、监事会对会计师事务所本报告期“非标准审计报告”的说明' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '四、公司利润分配及分红派息情况' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '四、董事会关于报告期会计政策、会计估计变更或重要前期差错更正的说明' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '四、董事会对会计师事务所本报告期“非标准审计报告”的说明' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '四、报告期财务会计报告审计情况及会计政策、会计估计变更以及会计差错更正的说明' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)

            print (index, factors)
            df = df.append (factors, ignore_index=True)
    # df.to_csv(r'data\index_2013.csv', encoding='gbk')
    return df

def handle_2014(list_2014):
    j = 0
    m = 0
    n = 0
    factors = {}
    df = pd.DataFrame ({})
    for index, one in enumerate (list_2014):
        with open (one, 'r', encoding='utf8', errors='ignore') as f:
            content = f.readlines ()
            for i, line in enumerate (content):
                # print(line)
                if '第四节董事会报告' in line.replace (' ', '') and len (line.replace (' ', '')) < 10:
                    j = j + 1
                    # print('j',j)
                    # print(i,line.replace(' ',''),one)
                    factors["filepath"] = one
                    factors['filename'] = one.split ('\\')[-1].split ('：')[0]
                    factors['filetime'] = one.split ('\\')[-1].split ('：')[-1].split ('年')[0]
                    factors['firstindex'] = int (i)
                if '第三节董事会报告' in line.replace (' ', '') and len (line.replace (' ', '')) < 10:
                    j = j + 1
                    # print('j',j)
                    # print(i,line.replace(' ',''),one)
                    factors["filepath"] = one
                    factors['filename'] = one.split ('\\')[-1].split ('：')[0]
                    factors['filetime'] = one.split ('\\')[-1].split ('：')[-1].split ('年')[0]
                    factors['firstindex'] = int (i)

                if '公司未来发展的展望' in line.replace (' ', '') and len (line.replace (' ', '')) < 13:
                    m = m + 1
                    # print('m',m)
                    # print(i,line.replace(' ',''),one)
                    factors['secondindex'] = int (i)
                    check = int(i)

                if '三、董事会、监事会对会计师事务所本报告期“非标准审计报告”的说明' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '三、公司利润分配及分红派息情况' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '三、董事会关于报告期会计政策、会计估计变更或重要前期差错更正的说明' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '三、董事会对会计师事务所本报告期“非标准审计报告”的说明' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '三、报告期财务会计报告审计情况及会计政策、会计估计变更以及会计差错更正的说明' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '三、报告期财务会计报告审计情况及会计政策、会计估计变更以及会计差错更正的说'in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)


                if '四、董事会、监事会对会计师事务所本报告期“非标准审计报告”的说明' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '四、公司利润分配及分红派息情况' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '四、董事会关于报告期会计政策、会计估计变更或重要前期差错更正的说明' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '四、董事会对会计师事务所本报告期“非标准审计报告”的说明' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)
                if '四、报告期财务会计报告审计情况及会计政策、会计估计变更以及会计差错更正的说明' in line.replace (' ', ''):
                    # print('存在')
                    factors['thirdindex'] = int (i)

            print (index, factors)
            df = df.append (factors, ignore_index=True)
    # df.to_csv(r'data\index_2014.csv', encoding='gbk')
    return df

def handle_content(df):
    df_content = pd.DataFrame ({})
    factors = {}
    for i in range (len (df)):
        factors['filepath'] = df.iloc[i]['filepath']
        factors['filename'] = df.iloc[i]['filename']
        factors['filetime'] = df.iloc[i]['filetime']
        # if '300020银江股份' in factors['filename']:
        #     continue
        with open (factors['filepath'], 'r', encoding='utf8', errors='ignore') as f:
            first_factor = []
            second_factor = []
            content = f.readlines ()
            for j, line in enumerate (content):
                # print(i,line)
                # print (df.iloc[i]['firstindex'],df.iloc[i]['secondindex'], df.iloc[i]['thirdindex'])
                if j >= int (df.iloc[i]['firstind'
                                        ']) and j < int (df.iloc[i]['secondindex']) :
                    first_factor.append (re.sub ('\d+.', '', line.replace (' ', '')).replace (r'/r/n', '').replace (r'/n', '').encode('gbk', 'ignore').decode ('gbk'))
                if j >= int (df.iloc[i]['secondindex']) and j < int (df.iloc[i]['thirdindex']):
                    second_factor.append (re.sub ('\d+.', '', line.replace (' ', '')).replace (r'/r/n', '').replace (r'/n', '').encode('gbk', 'ignore').decode ('gbk'))
            first_factors = ''.join (sentence for sentence in first_factor)
            second_factors = ''.join (sentence for sentence in second_factor)
            factors['firstfactor'] = first_factors
            factors['secondfactor'] = second_factors
            factors['firstsentence'] = len (re.findall ('。', first_factors)) + len (re.findall (';', first_factors)) +len (re.findall ('，', first_factors)) + len (re.findall (',', first_factors)) + len (re.findall ('；', first_factors))
            factors['secondsentence'] = len (re.findall ('。', second_factors)) + len (re.findall (';', second_factors)) + len (re.findall ('，', second_factors)) + len (re.findall (',', second_factors))+len (re.findall ('；', second_factors))
            if len(first_factors)>30000:
                factors['firstfactor'] = None
            print(i,factors['secondsentence'],factors['firstsentence'],factors['filename'])
        # print(i,factors['firstsentence'],factors['secondsentence'],factors['filename'])
        df_content = df_content.append (factors, ignore_index=True)
        df_content.to_csv (r'data\{}_sentence.csv'.format(df.iloc[1]['filetime']), encoding='gbk')
    # # df_content.to_csv (r'data\2015.csv', encoding='gbk')


if __name__ == '__main__':
    path = r'D:\辅助项目\15爬虫项目\9、胜男的数据分析\年报TXT'
    # list_2015, list_2014, list_2013 = read_pdf (path)
    # content_2015 = handle_2015 (list_2015)
    # handle_content (content_2015)
    # content_2013 = handle_2013 (list_2013)
    # handle_content (content_2013)
    # content_2014 = handle_2014 (list_2014)
    # handle_content(content_2014)

    # # 整合多个csv文件内容
    # concat_all = []
    # years = [2013,2014,2015]
    # for year in years:
    #     one = pd.read_csv ('data\cut_words\{}_factors2.csv'.format(year),encoding='gbk')
    #     concat_all.append(one)
    # reports = pd.concat (concat_all)
    # reports.to_csv('data/cut_words/company_factors2.csv',encoding='gbk')




