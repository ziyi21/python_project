#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

import requests
from requests import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def get_html(url):
    soup = None
    try:
        response = requests.get(url,timeout=30)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html,'html.parser')
        else:
            print('获取不到页面内容',response.status_code,url)
    except RequestException as e:
        print(url,'该网站无法访问',e)
    finally:
        soup = soup
    return soup

def get_ajax_html(url):
    urls = []
    driver = webdriver.Chrome (executable_path=r'D:\ksdler\chromedriver_win32_new\chromedriver')
    driver.get(url)
    driver.execute_script ('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep (2)
    driver.execute_script ('window.scrollTo(document.body.scrollHeight,200)')
    time.sleep (2)
    a=driver.find_element_by_xpath('//*[@id="j-course-box"]/div/div[4]/div/div/div/ul/li[3]/a').text
    print(a)
    # driver.find_element_by_xpath('//*[@id="auto-id-1527057202955"]/li[2]').click()
    url_link = driver.find_elements_by_xpath ('//*[@class="uc-course-list_ul"]/li')
    for one_li in url_link:
        url = one_li.find_element_by_xpath ('//a[@class="j-href"]').get_attribute ('href')
        print (url)
        urls.append (url)
    driver.execute_script ('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep (2)
    while driver.find_element_by_xpath('//li[@class="ux-pager_btn ux-pager_btn__next"]/a[@class="th-bk-main-gh"]'):
        driver.find_element_by_xpath('//li[@class="ux-pager_btn ux-pager_btn__next"]/a[@class="th-bk-main-gh"]').click()
        driver.execute_script ('window.scrollTo(document.body.scrollHeight,200)')
        time.sleep (2)
        url_link = driver.find_elements_by_xpath ('//*[@class="uc-course-list_ul"]/li')
        for one_li in url_link:
            url = one_li.find_element_by_xpath ('//a[@class="j-href"]').get_attribute ('href')
            print (url)
            urls.append (url)
    return url

if __name__ == '__main__':
    url = 'http://study.163.com/courses-search?keyword=python'
    soup = get_html(url)
    # print(soup)
    # print(soup.select_one('class.ux-pager').text)
    get_ajax_html(url)
