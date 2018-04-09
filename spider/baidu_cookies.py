#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'
#-*-coding:utf-8-*-
import sys
from importlib import reload
reload(sys)

from selenium import webdriver
import time
import pickle
driver = webdriver.PhantomJS(executable_path=r'D:\anaconda python\phantomjs-2.1.1-windows\bin\phantomjs.exe')
# driver = webdriver.Chrome(executable_path=r'D:\ksdler\chromedriver_win32_new\chromedriver')
driver.get('http://index.baidu.com/?tpl=trend&word=%D0%DB%B0%B2%D0%C2%C7%F8')
e1 = driver.find_element_by_id("TANGRAM_12__userName")
e1.send_keys("635516607@qq.com")
e2 = driver.find_element_by_id("TANGRAM_12__password")
e2.send_keys("woaini+365.88")
e3 = driver.find_element_by_id("TANGRAM_12__submit")
e3.click()
cookies = driver.get_cookies()
time.sleep(6)
pickle.dump(cookies, open("cookies.pkl","wb"))
