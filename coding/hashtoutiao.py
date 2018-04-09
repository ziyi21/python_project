# -*- coding: utf-8 -*-

#爬取投资界：http://www.pedaily.cn/；巴比特：http://www.8btc.com/；36氪:http://36kr.com/newsflashes

import os
import pandas as pd
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from pyquery import PyQuery as pq
from requests.exceptions import RequestException
from faker import Factory #它可以生成很多模拟的数据，如user-agent
f = Factory.create()
headers = {'User-Agent': f.user_agent()}


def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = response.text
            doc = pq(html)  # 设置解析器为“lxml”
            return doc
        else:
            print('获取不到', url, response.status_code)
            return None
    except RequestException as e:
        print('获取不到', url, e)
        return None


def get_btc():
    url = 'http://www.8btc.com/sitemap'
    df = pd.DataFrame({})
    doc = get_html(url)
    # print(doc)
    title_list = doc('li.itm.itm_new').items()
    contents = {}
    n = 1
    for title in title_list:
        if n > 20:
            break
        contents['title'] = title('a').attr('title')
        contents['url'] = 'http://www.8btc.com' + title('a').attr('href')
        # print(title('p span:nth-child(3)').text())
        contents['pub_time'] = title('p span:nth-child(3)').text()

        if contents['url']:
            time.sleep(5)
            detail_doc = get_html(contents['url'])
            contents['views'] = detail_doc('.single-crumbs.clearfix span.pull-right.fa-eye-span').text()
        print(contents)
        df = df.append(contents, ignore_index=True)
        n = n + 1
    return df


def get_pedaily():
    url = 'http://www.pedaily.cn/first/'
    df = pd.DataFrame({})
    doc = get_html(url)
    title_list = doc('#firstnews-list ul').items()
    contents = {}
    for title in title_list:
        if title('span.time.date').text() == "0:00":
            break
        contents['title'] = title('a').attr('title')
        contents['url'] = title('a').attr('href')
        # print(title('p span:nth-child(3)').text())
        contents['pub_time'] = title('span.time.date').text()
        print(contents)
        df = df.append(contents, ignore_index=True)
    return df


# 启动浏览器，executable_path路径要根据自己chromedriver.exe的位置更改
driver = webdriver.Chrome(executable_path=r'D:\ksdler\chromedriver_win32_new\chromedriver')
# driver = webdriver.Chrome()
# 设置浏览器窗口位置及大小
# driver.set_window_rect(x=0, y=0, width=667, height=748)
# 设定页面加载限制时间
driver.set_page_load_timeout(30)
# 设置锁定标签等待时长
wait = WebDriverWait(driver, 20)
# 打开登陆网址


def get_36k():
    url = 'http://36kr.com/newsflashes'
    driver.get(url)
    # 模拟js操作向下滑动窗口到最底部
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight*0.8)')
    time.sleep(3)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight*0.8)')
    time.sleep(5)
    df = pd.DataFrame({})
    title_list = driver.find_elements_by_css_selector('.conter-wrapper .fast_section_list .sameday_list li')
    print(title_list)
    contents = {}
    for title in title_list:
         # print(title)
        contents['title'] = title.find_element_by_css_selector('h2 span').text
        contents['content'] = title.find_element_by_css_selector('.fast_news_content span').text
        contents['url'] = title.find_element_by_css_selector('.fast_news_content a').get_attribute('href')
        # print(title('p span:nth-child(3)').text())
        contents['pub_time'] = title.find_element_by_css_selector('div.publish-datetime span').get_attribute('title')
        print(contents)
        df = df.append(contents, ignore_index=True)
    driver.close()
    return df

def jiemian():
    content = {}
    df = pd.DataFrame ({})
    url = 'http://www.jiemian.com/'
    driver.get(url)
    driver.execute_script ('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep (5)
    driver.execute_script ('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep (3)
    driver.execute_script ('window.scrollTo(document.body.scrollHeight,0)')
    time.sleep (5)

    # 依次获取每个新闻分类的数据列表集
    tianxia_list = driver.find_elements_by_xpath ('//*[@id="centerAjax"]/div[2]/div[@class="news-view "]/div[@class="news-header"]/h3/a')
    china_list = driver.find_elements_by_xpath ('//*[@id="centerAjax"]/div[4]/div[@class="news-view "]/div[@class="news-header"]/h3/a')
    hongguan_list = driver.find_elements_by_xpath ('//*[@id="centerAjax"]/div[6]/div[@class="news-view "]/div[@class="news-header"]/h3/a')
    most_popular = driver.find_elements_by_xpath ('//*[@id="centerAjax"]/div[8]/ul/li/a')
    jmedia = driver.find_elements_by_xpath ('//*[@id="jmediaAjax"]/div[@class="media-news"]/div[@class="media-header"]/h3/a')
    # jmedia_introduction = driver.find_elements_by_xpath('//*[@id="jmediaAjax"]/div[class="media-news"]/div[@class="media-main"]/p')
    classes_name = ['天下', '中国', '宏观', '最热', '媒体']
    news_list = [tianxia_list, china_list, hongguan_list,most_popular,jmedia]
    for i,news_classes in enumerate(news_list):
        print (i, classes_name[i])
        for news in news_classes:
            content['header'] = news.text
            content['news_url'] = news.get_attribute('href')
            content['classes_name'] = classes_name[i]
            content['pubtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print(content)
            df = df.append (content, ignore_index=True)
    return df

def save_info(now, contents, name):
    df = pd.DataFrame()
    df = df.append(contents.copy())
    df.to_csv(r'hashtoutiao\{0}\{1}_{0}.csv'.format(now, name), encoding='gbk')


def main():
    now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    delDir = "hashtoutiao"
    delList = os.listdir(delDir)
    print(delList)
    if now not in delList:
        os.mkdir ('hashtoutiao\{}'.format(now))

    # btc = get_btc ()
    # save_info (now, btc, 'btc')
    #
    # ped = get_pedaily ()
    # save_info (now, ped, 'ped')
    #
    # tsk = get_36k ()
    # save_info (now, tsk, '36k')

    jm = jiemian()
    save_info(now,jm,'jiemian')

    # for f in delList:
    #     filePath = os.path.join(delDir, f)
    #     if os.path.isfile(filePath):
    #         os.remove(filePath)
    #         print(filePath + " was removed!")

if __name__ == '__main__':
    main()
