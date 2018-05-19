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
    for i in range(user_dict_origin.shape[1]):
        one_factor = pd.DataFrame(user_dict_origin.iloc[:,i])
        # notnull_factor = one_factor.dropna().values  # 结果每一个值是一个列表，然后归入每一列的总列表中
        notnull_factor =  np.array(one_factor.dropna()).tolist() # 将DataFrame的值转化为series类型，再转换为列表类型
        # 依次将每个word按行追加到文件后面，并且指定编码方式为utf-8
        for word in notnull_factor:
            with open('data/cut_words/factors_line.txt', 'a',encoding='utf-8') as f:
                f.write(word[0] + '\n')

# 获取每篇财务报告的内容
def cut_factor1(filepath,stopwords):
    contents = pd.read_csv(filepath,encoding='gbk')
    # print('数据的规模', contents.shape)
    all_cuts = []

    # 所有公司的切分汇总
    for report_index in range(contents.shape[0]):
        cut_report_results = []
        cut_report_result = jieba.lcut(contents.iloc[report_index, 4], cut_all=False)  # lcut返回的是一个完整的列表cut_all=False 表示的精确切词
        for cut_word in cut_report_result:
            if cut_word.strip() not in stopwords:
                cut_report_results.append(cut_word)
        # 通过字典的形式保存统计得到的词频
        counts_results = dict(Counter(cut_report_results))
        # 返回一家公司的完整切分信息
        one_cut_results = [contents.iloc[report_index, 1], contents.iloc[report_index, 3], contents.iloc[report_index, 5
        ], cut_report_results,counts_results]
        all_cuts.append(one_cut_results)
    return all_cuts

# 获取每篇财务报告的内容
def cut_factor2(filepath,stopwords):
    contents = pd.read_csv(filepath,encoding='gbk')
    # print('数据的规模', contents.shape)
    all_cuts = []
    # # 一家公司的切分流程
    # cut_report_results = []
    # cut_report_result = jieba.lcut(contents.iloc[2, 4], cut_all=False)  # lcut返回的是一个完整的列表cut_all=False 表示的精确切词
    # # print(cut_report_result)
    # for cut_word in cut_report_result:
    #     if cut_word.strip() not in stopwords:
    #         cut_report_results.append(cut_word)
    # # print(cut_report_results)
    # # 通过字典的形式保存统计得到的词频
    # counts_results = dict(Counter(cut_report_results))
    # # print(Counter(cut_report_results))
    # # 返回公司的完整信息
    # one_cut_results = [contents.iloc[2,1],contents.iloc[2,3], contents.iloc[2,7],cut_report_results, counts_results]
    # print(one_cut_results)
    # return one_cut_results

    # 所有公司的切分汇总
    for report_index in range(contents.shape[0]):
        cut_report_results = []
        cut_report_result = jieba.lcut(contents.iloc[report_index, 6], cut_all=False)  # lcut返回的是一个完整的列表cut_all=False 表示的精确切词
        for cut_word in cut_report_result:
            if cut_word.strip() not in stopwords:
                cut_report_results.append(cut_word)
        # 通过字典的形式保存统计得到的词频
        counts_results = dict(Counter(cut_report_results))
        # 返回一家公司的完整切分信息
        one_cut_results = [contents.iloc[report_index, 1], contents.iloc[report_index, 3], contents.iloc[report_index, 7], cut_report_results,counts_results]
        all_cuts.append(one_cut_results)
    return all_cuts


# 统计切分出的词语的分类情况
def statistics_factors1(filepath):
    cuts_results = cut_factor1(content_filepath, stopwords)
    # print('cuts_results',cuts_results)
    factors = pd.read_excel(filepath)
    # 获取因子表的列名
    table_header = factors.columns.values.tolist()
    all_company_header = ['filename','filetime','firstsentence'] + table_header
    all_company = []

    for cuts_result in cuts_results:
        # 从统计好的词频中获取
        # print('cut_result',cuts_result)
        word = cuts_result[3]
        dict = cuts_result[4]
        factor_list = [cuts_result[0],cuts_result[1],cuts_result[2]]
        for one_column_name in table_header:
            factor_count = 0
            every_factor = factors[one_column_name].dropna().values.tolist()
            for name in word:
                if name in every_factor:
                    factor_count = dict[name] + factor_count
            factor_list.append(factor_count)
        all_company.append(factor_list)
    print(all_company)
    ############ 将数据保存到本地
    pd.DataFrame(data=all_company).to_csv('data/cut_words/{}_factors1.csv'.format(all_company[1][1]),header=all_company_header,encoding='gbk',index=False)
    pd.DataFrame(data=cuts_results).to_csv('data/cut_words/{}_words1.csv'.format(all_company[1][1]), header=False,encoding='gbk',index=False)

# 统计切分出的词语的分类情况
def statistics_factors2(filepath):
    cuts_results = cut_factor2(content_filepath, stopwords)
    # print('cuts_results',cuts_results)
    factors = pd.read_excel(filepath)
    # 获取因子表的列名
    table_header = factors.columns.values.tolist()
    all_company_header = ['filename','filetime','sencendsentence'] + table_header
    all_company = []

    for cuts_result in cuts_results:
        # 从统计好的词频中获取
        # print('cut_result',cuts_result)
        word = cuts_result[3]
        dict = cuts_result[4]
        factor_list = [cuts_result[0],cuts_result[1],cuts_result[2]]
        for one_column_name in table_header:
            factor_count = 0
            every_factor = factors[one_column_name].dropna().values.tolist()
            for name in word:
                if name in every_factor:
                    factor_count = dict[name] + factor_count
            factor_list.append(factor_count)
        all_company.append(factor_list)
    print(all_company)
    ############ 将数据保存到本地
    pd.DataFrame(data=all_company).to_csv('data/cut_words/{}_factors2.csv'.format(all_company[1][1]),header=all_company_header,encoding='gbk',index=False)
    pd.DataFrame(data=cuts_results).to_csv('data/cut_words/{}_words2.csv'.format(all_company[1][1]), header=False,encoding='gbk',index=False)

if __name__ == '__main__':
    forcast = r'data/cut_words/forcast.xlsx'
    plan =  r'data/cut_words/plan.xlsx'
    content_filepaths = [r'data/2013_sentence.csv',r'data/2014_sentence.csv',r'data/2015_sentence.csv']
    for content_filepath in content_filepaths:
        # 将自定义的分词字典加入结巴分词库
        jieba.load_userdict ('data/cut_words/factors_line.txt')
        stopwords = [line.rstrip () for line in open (r'data\cut_words\stopwords_gbk.txt', 'r')]
        # 使用自定义停用词集合
        # 切分文章内容
        statistics_factors1 (plan)
        statistics_factors2 (forcast)

    # 创建用户自己的分词字典
    # create_user_dict(forcast)
    # create_user_dict(plan)

    # # 切分文章内容
    #     # statistics_factors1(plan)
    #     # statistics_factors2(forcast)
