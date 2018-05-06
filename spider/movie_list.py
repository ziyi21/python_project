#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

# 导入的相关模块
from requests import RequestException
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_list(url):
    soup = None
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup (html, 'html.parser')  # 设置解析器为“html”
        else:
            print ('获取不到',url, response.status_code)
    except RequestException as e:
        print ('获取不到', url, e)
    # print (soup)
    time.sleep (3)
    return soup

def parse_html(soup,year,month):
    info = {}
    df = pd.DataFrame ({})
    all_movies = soup.select('ul.clearfix > li')
    # print(all_movies[4])
    for i, tag in enumerate(all_movies):
        if i>=4 and tag.select_one('div.txt > p.pTit > span.sTit'):
            info['movie_name'] = tag.select_one('div.txt > p.pTit > span.sTit').text.replace(' ','').encode ('gbk', 'ignore').decode ('gbk')
            info['movie_href'] = 'http:' + tag.a['href']
            info['movie_show_time'] = tag.select_one('div.txt > p.pTit > span.sTime').text.replace(' ','').encode ('gbk', 'ignore').decode ('gbk')
            try:
                information = tag.select('div.txt > p.pDes')[0].text.replace(' ','').encode ('gbk', 'ignore').decode ('gbk')
                info['movie_classes'] = information.split('\r\n\r\n')[0]
                info['movie_show_location'] = information.split ('\r\n\r\n')[-1]
                info['movie_actors'] = tag.select ('div.txt > p.pDes')[1].text.replace (' ', '').encode ('gbk','ignore').decode ('gbk')
            except:
                print('不对')
            info['movie_introduce'] = tag.select_one('div.txt > p.pIntro').text.replace (' ', '').encode ('gbk','ignore').decode ('gbk')
            info['movie_year'] = year
            info['movie_month'] = month
            df = df.append(info,ignore_index=True)
            # print(i,info)
    return df

def next_pages(soup):
    try:
        next_page = 'http:'+ soup.select('div.video_page > a')[-1]['href']
        next_text = soup.select ('div.video_page > a')[-1].text
        # next_page = next_page[-1]
        if '下一页' in next_text:
            print(next_page,next_text)
            return next_page
        else:
            return None
    except:
        return None

def data_processing(path):
    pass

if __name__ == '__main__':
    year = ['2017','2018']#,'2019'还没有数据呢
    month = ['01','02','03','04','05','06','07','08','09','10','11','12']
    df = pd.DataFrame()
    for one_year in year:
        for one_month in month:
            url = 'http://dianying.2345.com/xinpian/{}/'.format(one_year+one_month)
            print(url)
            soup = get_list (url)
            df1 = parse_html (soup, one_year, one_month)
            page = next_pages (soup)
            df = df.append(df1,ignore_index=True)
            while page:
                next_soup = get_list (page)
                page = next_pages (next_soup)
                df2 = parse_html (next_soup,one_year,one_month)
                df = df.append(df2,ignore_index=True)
        print(df)
    df.to_csv (r'data\movie\movie_list.csv', encoding='gbk')
