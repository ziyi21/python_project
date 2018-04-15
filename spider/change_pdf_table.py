#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

import tabula
import subprocess
# df = tabula.read_pdf(r'C:\Users\Think\Desktop\深圳能源集团股份有限公司.pdf', encoding='gbk', pages='all')
# # print(df)
# for indexs in df.index:
#     # 遍历打印企业名称
#     print(df.loc[indexs].values[1].strip())

subprocess.call('"D:\搜狗高速下载\pdf2htmlEX-win32-0.14.6-upx-with-poppler-data\pdf2htmlEX.exe"  --dest-dir C:\\Users\\Think\\Desktop\\out C:\\Users\\Think\\Desktop\\TCL集团：2016年年度报告.pdf', shell=True)