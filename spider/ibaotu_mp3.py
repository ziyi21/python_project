#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

from selenium import webdriver
import time
import pandas as pd
import  urllib.request

def get_music_url(music_web_url):
    df = pd.DataFrame({})
    music_infor = {}
    check = None
    driver.get(music_web_url)
    time.sleep(3)
    try:
        check = driver.find_element_by_xpath('/html/body/div[4]/div/a[1]')
    except:
        print('未弹出提示框')
    if check:
        check.click()
    music_url_list = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[2]/ul/li')
    for i, one_music in enumerate(music_url_list):
        music_infor['music_url'] = one_music.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/ul/li[{}]//audio[@id="audio0"]/source'.format(i+1)).get_attribute('src')
        music_infor['music_name'] = one_music.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/ul/li[{}]/div/div[2]/a[1]'.format(i+1)).text
        df = df.append (music_infor, ignore_index=True)
    print (df)
    return df

def get_freesound(url):
    driver.get(url)
    music_url = driver.find_element_by_xpath('//*[@id="single_sample_player"]/div/div[1]/a[1]').get_attribute('href')
    music_name = driver.find_element_by_xpath('//*[@id="single_sample_header"]/a[2]').text.encode('gbk','ignore').decode('gbk')
    print(music_name,music_url)
    return music_url,music_name

def get_goodlisten(url):
    driver.get(url)

def download_music(music_infor):
    for j in range (music_infor.iloc[:, 0].size):
        music_name = music_infor.ix[j, 0]
        music_url = music_infor.ix[j, 1]
        try:
            data = urllib.request.urlopen(music_url).read ()
            print (music_url)
            with open (('D:\\download_music\\freesound\\{}.mp3'.format (music_name)), 'wb') as f:
                f.write (data)
        except:
            print ("{}######链接不存在，继续下载下一首########".format (music_name))

def download_music_test(music_url,music_name):
    try:
        data = urllib.request.urlopen(music_url).read ()
        print (music_url)
        with open (('D:\\download_music\\freesound\\{}.mp3'.format (music_name)), 'wb') as f:
            f.write (data)
    except:
        print ("{}######链接不存在，继续下载下一首########".format (music_name))

if __name__ == '__main__':
    url = 'http://ibaotu.com/peiyue/?chan=bd&label=video&plan=D2-bd&kwd=10024'
    freesound_url = 'https://freesound.org/people/YleArkisto/sounds/425987/'
    good_listen_url = 'http://www.htqyy.com/play/3'
    driver = webdriver.Chrome (executable_path=r'D:\ksdler\chromedriver_win32_new\chromedriver')
    # music_url,music_name = get_freesound(freesound_url)
    # music_infor = get_music_url(url)
    music_url = 'https://freesound.org/data/previews/425/425987_4415905-lq.mp3'
    music_name = 'freesound'
    download_music_test(music_url,music_name)



