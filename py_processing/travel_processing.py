#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'
import pandas as pd
import numpy as np
# 导入结巴分词的模块
import jieba
from jieba import analyse
# 导入统计词频的模块
from collections import Counter

# 根据分类构建用户自己的字典，
def create_user_dict(filepath):
    user_dict_origin = pd.read_excel(filepath)
    print(user_dict_origin)
    for i in range(user_dict_origin.shape[1]):
        one_factor = pd.DataFrame(user_dict_origin.iloc[:,i])
        # notnull_factor = one_factor.dropna().values  # 结果每一个值是一个列表，然后归入每一列的总列表中
        notnull_factor =  np.array(one_factor.dropna()).tolist() # 将DataFrame的值转化为series类型，再转换为列表类型
        # 依次将每个word按行追加到文件后面，并且指定编码方式为utf-8
        for word in notnull_factor:
            with open('data/travel/factors_line.txt', 'a',encoding='utf-8') as f:
                f.write(word[0] + '\n')

# 获取每个评论的内容
def cut_content(filepath,stopwords):
    try:
        contents = pd.read_csv(filepath)
    except:
        contents = pd.read_csv(filepath, encoding='gbk')
    # print(contents.head(6))
    # print('数据的规模', contents.shape)
    all_cuts = []
    # 所有评论的切分汇总
    for report_index in range(contents.shape[0]):
        cut_report_results = []
        # print(contents.iloc[report_index, 1])
        cut_report_result = jieba.lcut(contents.iloc[report_index, 2], cut_all=False)  # lcut返回的是一个完整的列表cut_all=False 表示的精确切词
        for cut_word in cut_report_result:
            if cut_word.strip() not in stopwords:
                cut_report_results.append(cut_word)
        # 通过字典的形式保存统计得到的词频
        counts_results = dict(Counter(cut_report_results))
        # 返回一家公司的完整切分信息，将原有表格的所有列都返回
        one_cut_results = [contents.iloc[report_index, 0], contents.iloc[report_index, 1], contents.iloc[report_index, 2],contents.iloc[report_index, 3], contents.iloc[report_index, 4], contents.iloc[report_index, 5], contents.iloc[report_index, 6], contents.iloc[report_index, 7], contents.iloc[report_index, 8], cut_report_results,counts_results]
        all_cuts.append(one_cut_results)
    return all_cuts

# 统计切分出的词语的分类情况
def statistics_factors(filepath):
    contents_filepath = [r'data/travel/ctrip.csv'] #,r'data/travel/mafenwo.csv'r'data/travel/ctrip.csv
    for content_filepath in contents_filepath:
        cuts_results = cut_content(content_filepath, stopwords)
        print('cuts_results',cuts_results)
        factors = pd.read_excel(filepath)
        # 获取因子表的列名
        table_header = factors.columns.values.tolist()
        print(table_header)
        #	comment	savetime	star	time	user_name
        # user_name	create_time	blog	star	scenery_star	interest_star	performance_star	travel_time	scenery
        # 需要添加原表格的内容
        # all_company_header = ['index','comment','savetime','star','time','user_name'] + table_header
        all_company_header = ['user_name','create_time','blog','star','scenery_star','interest_star','performance_star','travel_time','scenery'] + table_header
        all_company = []

        for cuts_result in cuts_results:
            # 从统计好的词频中获取
            word = cuts_result[9]
            dict = cuts_result[10]
            factor_list = [cuts_result[0],cuts_result[1],cuts_result[2],cuts_result[3],cuts_result[4],cuts_result[5],cuts_result[6],cuts_result[7],cuts_result[8]]
            for one_column_name in table_header:
                factor_count = 0
                every_factor = factors[one_column_name].dropna().values.tolist()
                for name in word:
                    if name in every_factor:
                        factor_count = dict[name] + factor_count
                factor_list.append(factor_count)
            all_company.append(factor_list)
        print(all_company)
    # # #     ############ 将数据保存到本地
        try:
            pd.DataFrame(data=all_company).to_csv('data\\travel\\{}_factores.csv'.format(content_filepath.split('/')[-1].split('.')[0]),header=all_company_header,index=False,encoding= 'gbk')
        except:
            pd.DataFrame(data=all_company).to_csv('data\\travel\\{}_factores.csv'.format(content_filepath.split('/')[-1].split('.')[0]),header=all_company_header,index=False,encoding= 'utf8')
        try:
            pd.DataFrame(data=cuts_results).to_csv('data\\travel\\{}_cutwords.csv'.format(content_filepath.split('/')[-1].split('.')[0]), header=False,index=False,encoding= 'gbk')
        except:
            pd.DataFrame (data=cuts_results).to_csv ('data\\travel\\{}_cutwords.csv'.format (content_filepath.split ('/')[-1].split ('.')[0]), header=False,index=False, encoding='utf8')

if __name__ == '__main__':
    factors_filepath = r'data/travel/travel_factors.xlsx'
    # 创建用户自己的分词字典
    # create_user_dict(factors_filepath)
    # 将自定义的分词字典加入结巴分词库
    jieba.load_userdict(r'data/travel/factors_line.txt')
    stopwords = [line.rstrip() for line in open(r'data/travel/stopwords_gbk.txt', 'r')]
    # 使用自定义停用词集合
    analyse.set_stop_words(r'data/travel/stopwords_utf-8.txt')
    # 切分文章内容
    statistics_factors(factors_filepath)