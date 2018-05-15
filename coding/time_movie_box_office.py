#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

from selenium import webdriver
import pandas as pd
import time
import datetime
import os
from pypinyin import lazy_pinyin

def create_foleder(foldernames):
    current_position="data/movie/"
    foldername=str(current_position)+str(foldernames)+"/"
    isCreated=os.path.exists(foldername)
    if not isCreated:
        os.makedirs(foldername)
        print(str(foldername)+'is created')
        return foldername
    else:
        print("the folder has been created before")
        return foldername

def timerfun(sched_time,url_ori,movie_names) :
    flag = 0

    while True:
        index = 0

        now = datetime.datetime.now()
        if now > sched_time and now < sched_time + datetime.timedelta(seconds=1) :  # 因为时间秒之后的小数部分不一定相等，要标记一个范围判断
            # print(movie_names)
            for i,movie_name in enumerate(movie_names):
                print(i,movie_name)
                url = url_ori + movie_name
                print(url)
                contents = get_movie (url)
                if index == 0:
                    time.sleep (5)
                    # save_info(contents, contents['movie_name'][0] + 'box_office')
                    movie_name = movie_name.replace ('|', '')
                    movie_name = movie_name.replace (':', '')
                    movie_name = movie_name.replace ('：', '')
                    movie_name = movie_name.replace ('.', '')
                    movie_name = movie_name.replace (' ', '')
                    movie_name_pinyin = lazy_pinyin (movie_name)
                    foldernames = '_'.join (i for i in movie_name_pinyin)
                    save_path = create_foleder (foldernames)
                    save_name =  foldernames + '_box_office'
                    print(save_name)
                    save_info1 (contents, save_name, save_path)
                    print (now, save_path, '存储成功')
                    time.sleep (1)  # 每次判断间隔1s，避免多次触发事件
                if index != 0 and len(contents) == 8:
                    time.sleep(5)
                    # save_info(contents, contents['movie_name'][0] + 'box_office')
                    movie_name = movie_name.replace ('|', '')
                    movie_name = movie_name.replace (':', '')
                    movie_name = movie_name.replace ('：', '')
                    movie_name = movie_name.replace ('.', '')
                    movie_name = movie_name.replace (' ', '')
                    movie_name_pinyin = lazy_pinyin (movie_name)
                    foldernames = '_'.join (i for i in movie_name_pinyin)
                    try:
                        save_path = create_foleder (foldernames)
                        save_name = foldernames + '_box_office'
                    except:
                        save_name = None
                        save_path = None
                    print(save_name)
                    if save_path and save_name:
                        save_info (contents,save_name,save_path)
                        print(now,save_path,'存储成功')
                    time.sleep(1)    # 每次判断间隔1s，避免多次触发事件
                elif index != 0 and len(contents) < 8:
                    del movie_names[i]
                flag = 1
        else :
            if flag == 1 :
                sched_time = sched_time + datetime.timedelta (minutes=30)
                # sched_time = sched_time + datetime.timedelta(hours=1)  # 把目标时间增加一天，一天后触发再次执行
                # sched_time = sched_time + datetime.timedelta (seconds=30)
                flag = 0

def read_movies():
    df = pd.read_csv ('data/movie/movie_list.csv', encoding='gbk')
    movie_names = df['movie_name'].values.tolist()
    # print(movie_names)
    return movie_names


def get_movie(url):
    driver = webdriver.PhantomJS (executable_path=r'D:\anaconda python\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    now = datetime.datetime.now()
    df = pd.DataFrame({})
    contents = {}
    print(url)
    try:
        driver.get(url)
        time.sleep(3)
        movie_url = driver.find_element_by_xpath('//*[@id="moreRegion"]/li/h3/a').get_attribute('href')
        driver.find_element_by_xpath ('//*[@id="moreRegion"]/li/h3/a').click ()
        print(movie_url)
        driver.get(movie_url)
        time.sleep(5)
        contents['movie_url'] = movie_url
        contents['movie_name'] = driver.find_element_by_xpath('//*[@id="db_head"]/div[2]/div/div[1]/h1').text.encode('gbk','ignore').decode('gbk')
        contents['record_time'] = now
        driver.find_element_by_xpath('//*[@id="ratingRegion"]/div[2]/div').click()
        time.sleep(3)
        if driver.find_element_by_xpath('//*[@id="honorText"]/div/dl//dt'):
            contents['flash_time'] = driver.find_element_by_xpath('//*[@id="honorText"]/div/dl//dt').text.encode('gbk','ignore').decode('gbk')
            try:
                contents['inland_income'] = driver.find_element_by_xpath('//*[@id="honorText"]/div/dl/dd/ul/li[1]').text.encode('gbk','ignore').decode('gbk')
            except:
                pass
            try:
                contents['movie_ranking'] = driver.find_element_by_xpath('//*[@id="honorText"]/div/dl/dd/ul/li[2]').text.encode('gbk','ignore').decode('gbk')
            except:
                pass
            try:
                contents['all_income'] = driver.find_element_by_xpath('//*[@id="honorText"]/div/dl/dd/ul/li[3]').text.encode('gbk','ignore').decode('gbk')
            except:
                pass
            try:
                contents['show_days'] = driver.find_element_by_xpath('//*[@id="honorText"]/div/dl/dd/ul/li[4]').text.encode('gbk','ignore').decode('gbk')
            except:
                pass
        # elif driver.find_element_by_xpath('//*[@id="honorText"]/div/dl/dt')
        print(contents)
        df = df.append(contents, ignore_index=True)
    except Exception as e :
        print(e)
    return df

def save_info(contents, name,save_path):
    df = pd.DataFrame()
    df = df.append(contents.copy())
    df.to_csv(save_path+'{}.csv'.format(name), encoding='gbk',index=None, mode='a',header = False)
    # df.to_csv(save_path+'{}.csv'.format(name), encoding='gbk', index=None, mode='a')

def save_info1(contents, name,save_path):
    df = pd.DataFrame()
    df = df.append(contents.copy())
    # df.to_csv(save_path+'{}.csv'.format(name), encoding='gbk',index=None, mode='a',header = False)
    df.to_csv(save_path+'{}.csv'.format(name), encoding='gbk', index=None, mode='a')

if __name__ == '__main__':
    movie_name = '头号玩家'
    # movie_names = ['闺蜜2', '三伏天', '奇葩朵朵', '暴裂无声', '21克拉', '战神纪', '后来的我们', '幕后玩家', '追·踪', '低压槽：欲望之城']
    url = 'http://search.mtime.com/search/?q='
    # url = 'http://search.mtime.com/search/?q={}'.format (movie_name)
    # 获取某部影片的基本信息
    now = time.strftime('%Y-%m-%d', time.localtime(time.time())).split(' ')[0]
    sched_time = datetime.datetime (2018, 5, 7, 18, 33, 10)
    print(sched_time)
    # movie_name_pinyin = lazy_pinyin(movie_name)
    # foldernames = '_'.join(i for i in movie_name_pinyin)
    # save_path = create_foleder (foldernames)
    # print('_'.join(i for i in movie_name_pinyin))
    movie_names = read_movies ()
    timerfun (sched_time, url,movie_names)

    # df = get_movie (url)
    # print(df['movie_name'])
    # save_info(contents,movie_name+'box_office')
    # movie_name = 'jinritoutiao'
    # create_foleder(movie_name)




