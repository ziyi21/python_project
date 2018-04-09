#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

import re
import wget as wget
from urllib3.util import request
from selenium.webdriver import ActionChains
from selenium import webdriver
import os
import time

# driver = webdriver.PhantomJS (executable_path='浏览器引擎/自己使用phantomjs')
driver = webdriver.PhantomJS ()
if int (stockNumber) >= 600000:
    dst_url = 'http://www.cninfo.com.cn/cninfo-new/disclosure/sse'
else:
    dst_url = 'http://www.cninfo.com.cn/cninfo-new/disclosure/szse'

driver.get (dst_url)
prefixpath = "文件夹路径"
driver.find_element_by_class_name ("input-stock").send_keys (stockNumber)
driver.find_element_by_xpath ("//ul[@id='stock_list']/li[1]/a").click ()

prefixpathname = prefixpath + stockNumber + "/"
if os.path.exists (prefixpathname):
    pass
else:
    os.mkdir (prefixpathname)
# driver.find_element_by_xpath("//ul[@id='stock_list']/li[1]").send_keys(Keys.ENTER)
# 切换网页，以获取新弹出的网页窗口
for handle in driver.window_handles:
    driver.switch_to_window (handle)
    # print('current url:%s'%driver.current_url)
time.sleep (1)
urldata = driver.find_element_by_xpath ("//ul[@id='category_list']")
# print('%s'%urldata.text)
chain = ActionChains (driver)
moveelment = driver.find_element_by_xpath ("//div[@class='search-condition c5 drop-down']/a/div")
chain.move_to_element (moveelment).perform ()
driver.find_element_by_xpath ("//div[@class='search-condition c5 drop-down']/a/div").click ()

urldata = driver.find_element_by_xpath ("//div[@class='search-condition c5 drop-down']/a/div")
# print('%s'%urldata.text)
driver.find_element_by_xpath ("//ul[@id='category_list']/li[1]/a").click ()
# 选择需要的项，年报，半年报...等等
# 如果需要下载全部数据，需要点击更多，直到数据全部显示
# while(rslt[0] != rslt[1]):
#    driver.find_element_by_link_text('更多').click()
#    #等待网页相应时间
#    time.sleep(1)
#    urldata = driver.find_element_by_xpath("//div[@id='con-div-his-fulltext']/div[@class='stat-right']")
#    print('%s'%urldata.text)
#    patternStr = '\d+'
#    rslt = re.findall(patternStr,urldata.text)
listNum = int (rslt[0])

# listNum
if (listNum != 0):
    for indexValue in range (1, listNum + 1):
        findXpathStr = "//ul[@id='ul_his_fulltext']/li[%d]/div[@class='t3']/dd/span/a" % indexValue
        # print('%s'%findXpathStr)
        urlTextGet = driver.find_element_by_xpath (findXpathStr)
        print ('%s' % urlTextGet.text)

        driver.find_element_by_xpath (findXpathStr).click ()
        time.sleep (1)
        for handle in driver.window_handles:
            driver.switch_to_window (handle)
        time.sleep (1)
        # print('%s'%driver.current_url)
        urldata1 = driver.find_element_by_class_name ("year")
        try:
            urldata2 = driver.find_element_by_class_name ("new_day")
        except:
            urldata2 = driver.find_element_by_class_name ("day")
        timeStr = '%s%s' % (urldata1.text, urldata2.text)
        # print('%s%s'%(urldata1.text,urldata2.text))
        nameUrl = driver.find_element_by_xpath ('//div[@class="bd-top"]/h2')
        # print('%s'%nameUrl.text.replace(name,'').strip())
        # srcUrl = driver.find_element_by_xpath('//div[@class="bd-ct"]/iframe.src')
        # print('%s'%srcUrl.text)
        # downloadfilename = './new/%s%s.pdf'%(nameUrl.text.replace(name,'').strip(),timeStr)
        nameUrlList = nameUrl.text.split ('\n')
        if (len (nameUrlList) > 1):
            downloadfilename = '%s%s%s.pdf' % (prefixpathname, nameUrlList[1].strip (), timeStr)
        else:
            downloadfilename = '%s%s%s.pdf' % (prefixpathname, nameUrlList[0].strip (), timeStr)

        pageRequest = request.urlopen (driver.current_url)
        pageRead = pageRequest.read ().decode ('utf-8')
        # pageRequest.readlines().decode('utf-8')
        findlinkSuccess = 0
        for eachline in pageRead.split ('\n'):
            webDownloadURL = re.findall ('src="(.+)"', eachline)
            if (len (webDownloadURL) > 0) and re.search ('iframe', eachline) and re.search ('pdf', eachline.lower ()):
                wgetURL = webDownloadURL[0]
                # print('%s'%wgetURL)
                findlinkSuccess = 1
                break
                # 关闭当前URL窗口
        if (os.path.exists (downloadfilename)):
            print ('%s已存在' % downloadfilename)
        elif (findlinkSuccess == 1):
            wget.download (wgetURL, downloadfilename)
        else:
            print ('无效链接！ignore')
        driver.close ()

        # 返回指向前一次最新的URL
        for handle in driver.window_handles:
            driver.switch_to_window (handle)
        time.sleep (1)

driver.close ()
driver.quit ()