#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'
import os
from pypinyin import pinyin,lazy_pinyin
import pandas as pd
import time
#
# folder = 'data/movie/'
# isCreated=os.path.exists(folder)
# print(isCreated)
#
# def create_foleder(foldernames):
#     current_position="data/movie/"
#     foldername=str(current_position)+str(foldernames)+"/"
#     isCreated=os.path.exists(foldername)
#     if not isCreated:
#         os.makedirs(foldername)
#         print(str(foldername)+'is created')
#         return foldername
#     else:
#         print("the folder has been created before")
#         return foldername
#
# if __name__ == '__main__':
#     movie_name = '头号玩家'
#     url = 'http://search.mtime.com/search/?q={}'.format (movie_name)
#     movie_name_pinyin = lazy_pinyin(movie_name)
#     foldernames = '_'.join(i for i in movie_name_pinyin)
#     path_name = create_foleder (foldernames)
#     print('path_name' , path_name)
#     print('_'.join(i for i in movie_name_pinyin))
#     # create_foleder()
#
# df = pd.read_csv('data/movie/movie_list.csv',encoding = 'gbk')
# print(df['movie_name'].values.tolist())

# # 测试携程网抓取的下一页内容
# import time
# from selenium import webdriver
# driver = webdriver.Chrome(executable_path=r'D:\ksdler\chromedriver_win32_new\chromedriver')
# sight_url = 'http://you.ctrip.com/sight/hangzhou14/49894.html'
# driver.get(sight_url)
# # driver.set_window_size()
# driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
# time.sleep(1)
# # driver.execute_script('window.scrollTo(document.body.scrollHeight,200)')
# time.sleep(1)
# try:
#     driver.find_element_by_xpath('//*[@id="appd_wrap_close"]').click()
#     print('点击')
# except:
#     pass
# a = driver.find_element_by_css_selector('div.ttd_pager.cf div a.nextpage').get_attribute('href')
# print(a)
# driver.find_element_by_xpath('//*[@id="sightcommentbox"]/div[11]/div/a[7]').click()
# driver.find_element_by_css_selector('div.ttd_pager.cf div a.nextpage').click()

#四种遍历查找文件的方法
# for filename in os.listdir(r'data\movie'):
#     print (filename)
# import glob
# for filename in glob.glob(r'data\movie\*.csv'):
#     print (filename)
# check_list = []
# comments_url = []
# for dirpath, dirnames, filenames in os.walk(r'data\movie'):
#     # print('Directory', dirpath)
#     for i in range(1,32):
#         i = str(i)
#         if len(i) == 1:
#             i = '0'+i
#         check_list.append(i)
#     for filename in filenames:
#         check_name = filename.split('.')[0].split('-')[-1]
#         if check_name in check_list:
#             movie_url_file = dirpath+ r'\\' + filename
#             print (dirpath+ r'\\' + filename)
#             try:
#                 df = pd.read_csv(movie_url_file, encoding='gbk')
#             except:
#                 df = None
#             try:
#                 comment_url = df['urls_comments']
#                 print(comment_url,filename)
#             except:
#                 comment_url = None
#             if comment_url:
#                 print('w')


b = 1+1
print(b)