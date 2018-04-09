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
# driver=webdriver.PhantomJS(executable_path=r'D:\anaconda python\phantomjs-2.1.1-windows\bin\phantomjs.exe')
from PIL import Image
import pytesseract

driver = webdriver.Chrome(executable_path=r'D:\ksdler\chromedriver_win32_new\chromedriver')
####################################第二步:利用cookie登录#####################################
driver.get("http://index.baidu.com")
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
driver.get("http://index.baidu.com/?tpl=trend&word=%D0%DB%B0%B2%D0%C2%C7%F8")
time.sleep(3)

driver.get_screenshot_as_file(r'pictures\5.png')
print("截屏结束.................")
driver.quit()
###########二值化算法
def binarizing(img,threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img

img1=Image.open(r"pictures\5.png")
w,h=img1.size
# region = (220*3,320*3,420*3,380*3)//两个一起
##将图片放大3倍
out=img1.resize((w*3,h*3),Image.ANTIALIAS)
region1 = (220*3,320*3,320*3,380*3)
region2 = (320*3,320*3,420*3,380*3)
cropImg1 = out.crop(region1)
cropImg2 = out.crop(region2)
img1= cropImg1.convert('L')
img2= cropImg2.convert('L')
img1=binarizing(img1,200)
img2=binarizing(img2,200)
code1 = pytesseract.image_to_string(img1)
code2 = pytesseract.image_to_string(img2)

print ("整体搜索指数:" + str(code1).replace(".","").replace(" ",''))
print ("移动搜索指数:" + str(code2).replace(".","").replace(" ",''))
# img1.show()
# img2.show()