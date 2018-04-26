#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

from selenium import webdriver
import time

def get_url():
    pass

if __name__ == '__main__':

    travel_name = ['夫子庙']
    driver = webdriver.Chrome (executable_path=r'D:\ksdler\chromedriver_win32_new\chromedriver')
    for one_travel in travel_name:
        print(one_travel)
        url = 'http://piao.qunar.com/ticket/list.htm?keyword={}&region=&from=mpl_search_suggest'.format(one_travel)
        driver.get(url)
        travel_url = driver.find_element_by_xpath('//*[@id="search-list"]/div[1]/div[1]/div[2]/h3/a').get_attribute('href')
        driver.find_element_by_xpath ('//*[@id="search-list"]/div[1]/div[1]/div[2]/h3/a').click()
        driver.get(travel_url)
        driver.execute_script ('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep (1)
        driver.execute_script ('window.scrollTo(document.body.scrollHeight,200)')
        time.sleep (1)
        user_comments = driver.find_element_by_xpath('//*[@id="mp-comments"]/h2').text
        print(user_comments)
    pass


