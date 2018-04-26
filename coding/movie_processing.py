#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

import pandas as pd
import re
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

def get_people_infor(data):
    writer_infor = {}
    writers = []
    df = pd.DataFrame ({})
    for writer_url in data:
        try:
            writer_url = writer_url.split('blog')[0]
        except:
            pass

        try:
            writer_url = writer_url.replace ('my', 'i')
        except:
            pass

        one_soup = get_comments_html (writer_url)
        for tag in one_soup.find('div',class_='member_info').children:
            if isinstance (tag, bs4.element.Tag):  # 使用isinstance过滤掉空行内容
                # print(tag.get_text().encode ('gbk', 'ignore').decode ('gbk'))
                writers.append (tag.get_text ().encode ('gbk', 'ignore').decode ('gbk'))
        writer_infor['writer_url'] = writer_url
        writer_infor['people_infor_all'] = writers
        print(writer_infor)
        df = df.append (writer_infor, ignore_index=True)
    return df

def people_infor_classify(data):
    writer_pic = {}
    df = pd.DataFrame ({})
    print(data.columns.values.tolist)
    # peoples = data.columns.values.tolist
    # print(len(data))
    # print(data.iloc[:,1])
    # 依次获取每一行的数据。
    for one in range(len(data)):
        one_line = data.iloc[one,:]
        people_infor_all = (one,one_line['people_infor_all'])
        print(one,one_line['writer_url'])
        print(one,people_infor_all)
        writer_pic['name'] = people_infor_all[1].split(',')[1].replace("'","")
        # print(people_infor_all[0].split(',')[2].replace("'",""))
        all_infor = people_infor_all[1].split(',')[2].replace("'","")
        # print(people_infor_all[1])
        if '男' in all_infor:
            writer_pic['gender'] = '男'
        elif '女' in all_infor:
            writer_pic['gender'] = '女'
        else:
            writer_pic['gender'] = None

        try:
            writer_pic['age'] = re.findall(r'\d+岁',all_infor)[0]
        except:
            writer_pic['age'] = None
        try:
            writer_pic['location'] = re.findall(r'居住在：(.*)',all_infor)[0].split(' ')[0]
        except:
            writer_pic['location'] = None
        try:
            writer_pic['constellatory'] = re.findall(r'(.*座)',all_infor)[-1].split(' ')[-1]
        except:
            writer_pic['constellatory'] = None
        try:
            writer_pic['follower'] = int(re.findall(r'(\d+)位粉丝', all_infor)[0])
        except:
            writer_pic['follower'] = None
        try:
            writer_pic['blog'] = int(re.findall(r'(\d+)篇日志', all_infor)[0])
        except:
            writer_pic['blog'] = None
        try:
            writer_pic['pictures'] = int(re.findall(r'(\d+)张照片', all_infor)[0])
        except:
            writer_pic['pictures'] = None
        try:
            writer_pic['group'] = int(re.findall(r'(\d+)个群组', all_infor)[0])
        except:
            writer_pic['group'] = None
        try:
            comments = re.findall(r'已得到的评价(.*?)\d{0,4}位粉丝',all_infor)[0]
        except:
            comments = None
        other_people_comment = 0
        try:
            for i in re.findall('\d+', comments):
                other_people_comment = int(i)+ other_people_comment
        except:
            comments = None
        try:
            writer_pic['other_people_comments'] = other_people_comment
            writer_pic['read_times'] = int(re.findall(r'访问量：(.*)加入时间',all_infor)[0])
            writer_pic['join_time'] = re.findall(r'加入时间：(.*)最后登录', all_infor)[0]
            writer_pic['load_time'] = re.findall(r'最后登录：(.*)添加到我的订阅', all_infor)[0]
        except:
            writer_pic['read_times'] = None
            writer_pic['join_time'] = None
            writer_pic['load_time'] = None
        writer_pic['writer_url'] = one_line['writer_url']
        writer_pic['classify'] = one_line['classify']
        print(writer_pic)
        df = df.append (writer_pic, ignore_index=True)
    return df

def save_info(contents, name):
    df = pd.DataFrame()
    df = df.append(contents.copy())
    df.to_csv(r'data\movie_thwj\{}.csv'.format(name), encoding='gbk',index=None)

if __name__ == '__main__':
    content = pd.DataFrame ({})
    writer_infor = pd.DataFrame ({})
    read_path = r'data\movie\thwj_long_comments_basic.csv'
    read_short_writer_path = r'data\movie\thwj_short_comments.csv'
    read_writer_infor = r'data\movie_thwj\writer_information.csv'

    # # 获取长评论的文章的连接
    # long_comments_basic = pd.read_csv(read_path, encoding='gbk')
    # content = get_comments_content(long_comments_basic)
    # save_info(content, 'thwj_writer_information')

    # # 获取长评论的作者的连接
    # long_writer_urls = long_comments_basic['writer_url']
    # writer = get_people_infor(long_writer_urls)
    # save_info(writer, 'thwj_writer_information')

    # # 获取短评论的作者的连接
    # short_writer_infor = pd.read_csv(read_short_writer_path, encoding='gbk')
    # short_writer_url = short_writer_infor['short_writer_url']
    # print(short_writer_url)
    # writer = get_people_infor(short_writer_url)
    # save_info(writer, 'thwj_short_writer_information')
    # print(1,writer_infor['writer_url'])

    peoples = pd.read_csv(read_writer_infor, encoding='gbk')
    people_classify = people_infor_classify(peoples)
    save_info(people_classify, 'writer_information_classify')

    # print(peoples)

    # 判断是否已经爬取完成
    # exist_urls = []
    # short_comments_basic = pd.read_csv (read_short_writer_path, encoding='gbk')['short_writer_url']
    # # print(2,short_comments_basic['short_writer_url'])
    # for exist_url in writer_infor['writer_url']:
    #     exist_urls.append(exist_url)

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

