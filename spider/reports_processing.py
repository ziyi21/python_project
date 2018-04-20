#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

import os
import pandas as pd

def create_reports_table(filename,path):
    df = pd.DataFrame ({})
    analysis_data = {}
    failed_company = []
    # 所有内容初始化
    analysis_data['total_information'] = 0
    analysis_data['five_customers_sale_all'] = 0
    analysis_data['five_relevance_customers_sale'] = 0
    analysis_data['five_relevance_customers_check'] = 0
    analysis_data['five_customers_name'] = 0
    analysis_data['five_customers_sale'] = 0

    analysis_data['five_supplier_buy_all'] = 0
    analysis_data['five_relevance_supplier_buy'] = 0
    analysis_data['five_relevance_supplier_check'] = 0
    analysis_data['five_supplier_name'] = 0
    analysis_data['five_supplier_buy'] = 0
    with open(path) as all:
        customer = 0
        company_name = {}
        company_index = []
        all_txt = all.read()
        # 判断披露金额占比是否有0%的情况存在
        if '0%' not in all_txt or '0.00%' not in all_txt or '0.0%' not in all_txt:
            show_check = 1
        else:
            show_check = 0

        # 财报中未披露前五客户或前五供应商信息的公司情况
        if "未披露" in all_txt:
            print('未披露')
            analysis_data['five_customers_sale_all'] = 0
            analysis_data['five_relevance_customers_sale'] = 0
            analysis_data['five_relevance_customers_check'] = 0
            analysis_data['five_customers_name'] = 0
            analysis_data['five_customers_sale'] = 0

            analysis_data['five_supplier_buy_all'] = 0
            analysis_data['five_relevance_supplier_buy'] = 0
            analysis_data['five_relevance_supplier_check'] = 0
            analysis_data['five_supplier_name'] = 0
            analysis_data['five_supplier_buy'] = 0

        # 财报中未披露前五客户或前五供应商信息的公司情况
        elif "pdf解码错误" in all_txt:
            print('pdf解码错误')
            failed_company.append(file_name)
        else:
            # print(''.join(content for content in all_txt.strip().split()))
            with open (path) as f:
                for i,company_line in enumerate(f):
                    # print(company_line)
                    # 有披露内容的指标的判断
                    # 1前五名客户合计销售金额占年度销售总额的比例
                    if '客户' in company_line and '销售' in company_line and '总额' in company_line:
                        customer = 1
                    elif '客户' in company_line and '营业' in company_line and '总额' in company_line:
                        customer = 1
                    if customer == 1 and '销售' in company_line and '比' in company_line:
                        analysis_data['five_customers_sale_all'] = 1
                    elif '客户' in company_line and '销售' in company_line and '比' in company_line:
                        analysis_data['five_customers_sale_all'] = 1
                    elif '客户' in company_line and '营业' in company_line and '比' in company_line:
                        analysis_data['five_customers_sale_all'] = 1
                    elif '客户' in company_line and '营业' in company_line and '总额' in company_line:
                        analysis_data['five_customers_sale_all'] = 1
                    elif '客户' in company_line and '营业' in company_line and '总额' in company_line:
                        analysis_data['five_customers_sale_all'] = 1

                    # 2前五名客户销售额中关联方销售额合计占年度销售总额的比例
                    if '客户' in company_line and "关联" in company_line and '比' in company_line:
                        analysis_data['five_relevance_customers_sale'] = 1

                    # 3前五名客户分别与自己的关联关系
                    if analysis_data['five_relevance_customers_sale'] == 1 and show_check == 1:
                        analysis_data['five_relevance_customers_check'] = 1
                    elif analysis_data['five_relevance_customers_sale'] == 0:
                        analysis_data['five_relevance_customers_check'] = 0
                    else:
                        analysis_data['five_relevance_customers_check'] = -1

                    # 4前五名客户具体名称和5前五名客户的具体销售额
                    if '前五' in company_line or '前5' in company_line:
                        if '前五' in company_line and '客户资料':
                            analysis_data['five_customers_name'] = 1
                            analysis_data['five_customers_sale'] = 1
                        if '前5' in company_line and '客户资料':
                            analysis_data['five_customers_name'] = 1
                            analysis_data['five_customers_sale'] = 1
                        if '前五' in company_line and '供应商资料':
                            analysis_data['five_supplier_name'] = 1
                            analysis_data['five_supplier_buy'] = 1
                        if '前5' in company_line and '供应商资料':
                            analysis_data['five_supplier_name'] = 1
                            analysis_data['five_supplier_buy'] = 1
                    else:
                        if '有限公司' in company_line or '股份公司' in company_line or '有限责任公司' in company_line:
                        # company_name[i] = company_line
                            company_index.append(i)

                    # 6前五名供应商合计采购金额占年度采购总额比例
                    if '供应商' in company_line and '采购' in company_line and '比' in company_line:
                        analysis_data['five_supplier_buy_all'] = 1

                    # 7前五名供应商采购额中关联方采购额占年度采购总额比例
                    if '供应商' in company_line and "关联" in company_line and '比' in company_line:
                        analysis_data['five_relevance_supplier_buy'] = 1

                    # 8前五名供应商分别与自己的关联关系
                    if analysis_data['five_relevance_supplier_buy'] == 1 and show_check == 1:
                        analysis_data['five_relevance_supplier_check'] = 1
                    elif analysis_data['five_relevance_supplier_buy'] == 0:
                        analysis_data['five_relevance_supplier_check'] = 0
                    else:
                        analysis_data['five_relevance_supplier_check'] = -1

    # 4前五名客户具体名称是否存在
    # 5前五名客户的具体销售额
    print('有关的公司数量',len(company_index))
    check = []
    if len(company_index) < 5:
        analysis_data['five_customers_name'] = 0
        analysis_data['five_customers_sale'] = 0
        analysis_data['five_supplier_name'] = 0
        analysis_data['five_supplier_buy'] = 0
    elif len(company_index) > 15:
        analysis_data['five_customers_name'] = 1
        analysis_data['five_customers_sale'] = 1
        analysis_data['five_supplier_name'] = 1
        analysis_data['five_supplier_buy'] = 1
    else:
        for j,relevance_company in enumerate(company_index):
            m = int(relevance_company)-j
            check.append(m)
        if len(check)-len(set(check)) > 8:
            print('差值',len(check)-len(set(check)))
            analysis_data['five_customers_name'] = 1
            analysis_data['five_customers_sale'] = 1
            analysis_data['five_supplier_name'] = 1
            analysis_data['five_supplier_buy'] = 1
            # 5前五名客户的具体销售额

    analysis_data['classify'] = '深市'
    analysis_data['ID'] = file_name.split('_')[2]
    analysis_data['name'] = file_name.split('_')[1]
    analysis_data['time'] = file_name.split('_')[0]
    analysis_data['total_information'] = int(analysis_data['five_customers_sale_all'])+int(analysis_data['five_relevance_customers_sale'])+int(analysis_data['five_relevance_customers_check'])+int(analysis_data['five_customers_name'])+int(analysis_data['five_customers_sale'])+int(analysis_data['five_supplier_buy_all']) +int(analysis_data['five_relevance_supplier_buy'])+int(analysis_data['five_relevance_supplier_check'])+int(analysis_data['five_supplier_name'])+int(analysis_data['five_supplier_buy'])
    print(analysis_data)
    df = df.append (analysis_data, ignore_index=True)
    return df

def save_info(contents, name):
    df = pd.DataFrame()
    df = df.append(contents.copy())
    df.to_csv('D:\\financial_reports\\sz_financial_reports\\{}.csv'.format(name+'_test'), encoding='gbk',)

if __name__ == '__main__':
    analysis_path = 'D:\\financial_reports\\sz_financial_reports\\sz_txt'
    all_file = os.listdir(analysis_path)
    results = []
    for one in all_file:
        path = os.path.join(analysis_path,one)
        file_name = os.path.splitext(one)[0]
        print(path)
        table = create_reports_table(file_name,path)
        results.append(table)
    save_info(results,analysis_path.split('\\')[-1])
