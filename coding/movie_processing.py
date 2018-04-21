#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

import pandas as pd
from selenium import webdriver
import time
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import bs4

def get_comments_html(one_url):
    soup = None
    try:
        response = requests.get(one_url,timeout=30)
        if response.status_code == 200:
            html = response.text
            # print (html)
            soup = BeautifulSoup (html, 'html.parser')  # 设置解析器为“html”
        else:
            print ('获取不到', one_url, response.status_code)
    except RequestException as e:
        print ('获取不到', one_url, e)
    # print (soup)
    time.sleep (3)
    return soup

def get_comments_content(data):
    comments_content = {}
    contents = []
    df = pd.DataFrame ({})
    for one_url in data['comment_href']:
        one_soup = get_comments_html(one_url)
        for p in one_soup.find ("div", class_="db_mediacont db_commentcont").children:
            if isinstance (p, bs4.element.Tag):  # 使用isinstance过滤掉空行内容
                contents.append (p.get_text ().encode ('gbk', 'ignore').decode ('gbk'))
        content = '\n'.join (one for one in contents)
        comments_content['one_content_url'] = one_url
        comments_content['one_content'] = content
        df = df.append (comments_content, ignore_index=True)
        print(comments_content)
    return df

def get_people_infor(one_soup,writer_url):
    writer_infor = {}
    writers = []
    for tag in one_soup.find('div',class_='member_info').children:
        if isinstance (tag, bs4.element.Tag):  # 使用isinstance过滤掉空行内容
            # print(tag.get_text().encode ('gbk', 'ignore').decode ('gbk'))
            writers.append (tag.get_text ().encode ('gbk', 'ignore').decode ('gbk'))
    writer_infor['writer_url'] = writer_url
    writer_infor['people_infor_all'] = writers
    print(writer_infor)
    return writer_infor

def save_info(contents, name):
    df = pd.DataFrame()
    df = df.append(contents.copy())
    df.to_csv(r'data\movie_thwj\{}.csv'.format(name), encoding='gbk',index=None)

if __name__ == '__main__':
    content = pd.DataFrame ({})
    writer_infor = pd.DataFrame ({})
    read_path = r'data\movie\thwj_long_comments_basic.csv'
    read_short_writer_path = r'data\movie\thwj_short_comments.csv'
    read_writer_infor = r'data\movie\thwj_short_writer_information.csv'

    # 获取长评论的文章的连接
    long_comments_basic = pd.read_csv(read_path, encoding='gbk')
    content = get_comments_content(long_comments_basic)

    # 获取长评论的文章的连接
    # for one_url in long_comments_basic['comment_href']:
    #     one_soup = get_comments_html(one_url)
    #     if one_soup:
    #         comments_content = get_comments_content(one_soup,one_url)
    #         content = content.append (comments_content, ignore_index=True)
    # save_info(content, 'thwj_long_comments_content')
    # 获取长评论的作者的连接
    # for writer_url in long_comments_basic['writer_url']:
    #     writer_url = writer_url.split('blog')[0]
    #     print('长评论作者',writer_url)
    #     one_soup = get_comments_html (writer_url)
    #     if one_soup:
    #         writer_all = get_people_infor(one_soup,writer_url)
    #         writer_infor = writer_infor.append(writer_all,ignore_index=True)
    # save_info (writer_infor, 'thwj_writer_information')

    # 获取短评论的作者的连接
    writer_infor = pd.read_csv(read_writer_infor, encoding='gbk')
    # print(1,writer_infor['writer_url'])
    exist_urls = []
    short_comments_basic = pd.read_csv (read_short_writer_path, encoding='gbk')
    # print(2,short_comments_basic['short_writer_url'])
    for exist_url in writer_infor['writer_url']:
        exist_urls.append(exist_url)

    # for writer_url in short_comments_basic['short_writer_url']:
    #     writer_url = writer_url.replace ('my', 'i')
    #     if writer_url not in exist_urls:
    #         print('还没有爬',writer_url)
    #         one_soup = get_comments_html (writer_url)
    #         time.sleep(1)
    #         if one_soup:
    #             writer_all = get_people_infor(one_soup, writer_url)
    #             writer_infor = writer_infor.append(writer_all, ignore_index=True)
    #         save_info (writer_infor, 'thwj_short_writer2_information')
    #     else:
    #         print('已经爬完')

