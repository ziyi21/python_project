#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

import requests
from urllib import request
def getFile(url):
    file_name = url.split('/')[-1]
    u = request.urlopen(url)
    f = open('pdf_record/'+file_name, 'wb')
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        f.write(buffer)
    f.close()
    print ("Sucessful to 'download" + " " + file_name)

url = 'http://disclosure.szse.cn/finalpage/2018-04-09/1204593820.PDF'
getFile(url)