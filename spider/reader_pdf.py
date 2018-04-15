#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

import sys
import importlib
import os
importlib.reload(sys)
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

'''
 解析pdf 文本，保存到txt文件中
'''

def parse(read_path,save_path):
    fp = open(read_path, 'rb') # 以二进制读模式打开
    #用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages(): # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    content = []
                    with open(save_path, 'a') as f:
                        results = x.get_text().encode('gbk','ignore').decode('gbk')
                        print(results)
                        f.write(results + '\n')

if __name__ == '__main__':
    sz_pdf_path = 'D:\\financial_reports\\sz_financial_reports\\sz_pdf'
    sh_pdf_path = 'D:\\financial_reports\\sh_financial_reports\\sh_pdf'
    all_file_name = os.listdir(sz_pdf_path)
    for file in all_file_name:
        save_txt_path = 'D:\\financial_reports\\sz_financial_reports\\sz_txt_all'
        fname = os.path.splitext (file)[0]
        read_path = os.path.join (sz_pdf_path, file)
        print(read_path)
        save_path = os.path.join(save_txt_path,fname+'.txt')
        print(save_path)
        parse(read_path,save_path)