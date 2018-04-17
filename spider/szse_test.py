#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

'D:\\financial_reports\\sz_financial_reports\\sz_pdf\\2016_万科.PDF'
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

def parse(read_path):
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
    return doc,interpreter,device

def get_content_index(doc,interpreter,device,save_path):
    # 循环遍历列表，每次处理一个page的内容
    content = []
    try:
        for page_index,page in enumerate(doc.get_pages()): # doc.get_pages() 获取page列表
            # print(page_index)
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    results = x.get_text ().encode ('gbk', 'ignore').decode ('gbk')
                    # print(x.get_text())
                    # with open (save_path, 'a') as f:
                    #     results = x.get_text ().encode ('gbk', 'ignore').decode ('gbk')
                    #     print (results)
                    #     f.write (results + '\n')
                    # 判断获取前五客户的相关披露信息
                    if '前五' in results and '客户' in results :
                        print (page_index)
                        print(results)
                        content.append(page_index)
                    elif '前五' in results and '客户' in results and '销售' in results:
                        content.append (page_index)
                    elif '前五' in results and '客户' in results and '关联' in results:
                        content.append (page_index)
                    # 判断获取前五供应商的相关披露信息
                    elif '前五' in results and '供应商' in results :
                        content.append (page_index)
                    elif '前五' in results and '供应商' in results and '采购' in results:
                        content.append (page_index)
                    elif '前五' in results and '供应商' in results and '关联' in results:
                        content.append(page_index)
                    # 判断获取前五供货商的相关披露信息
                    elif '前五' in results and '供货商' in results :
                        content.append (page_index)
                    elif '前五' in results and '供货商' in results and '采购' in results:
                        content.append (page_index)
                    elif '前五' in results and '供货商' in results and '关联' in results:
                        content.append(page_index)

                    elif '前5' in results and '客户' in results :
                        content.append (page_index)
                    elif '前5' in results and '客户' in results and '销售' in results:
                        content.append (page_index)
                    elif '前5' in results and '客户' in results and '关联' in results:
                        content.append (page_index)
                    # 判断获取前五供应商的相关披露信息
                    elif '前5' in results and '供应商' in results :
                        content.append (page_index)
                    elif '前5' in results and '供应商' in results and '采购' in results:
                        content.append (page_index)
                    elif '前5' in results and '供应商' in results and '关联' in results:
                        content.append(page_index)
                    # 判断获取前五供货商的相关披露信息
                    elif '前5' in results and '供货商' in results :
                        content.append (page_index)
                    elif '前5' in results and '供货商' in results and '采购' in results:
                        content.append (page_index)
                    elif '前5' in results and '供货商' in results and '关联' in results:
                        content.append(page_index)
                    # 获取其他前五的披露的所有信息
                    # elif '前五' in results :
                    #     print(results)
                        # content.append(page_index)
    except Exception as e:
        print (save_path.split ('\\')[-1] + 'pdf解码错误')
    print(content)
    return list(set(content))

def get_content(doc, interpreter, device,content,save_path):
    # 循环遍历列表，每次处理一个page的内容
    # with open (save_path, 'a') as f:
    #     f.write ('披露信息所在财务报表的页数为：'+ content + '\n')
    try:
        if content[0]:
            for get_index in content:
                print(get_index)
                for page_index,page in enumerate(doc.get_pages ()):  # doc.get_pages() 获取page列表
                    interpreter.process_page (page)
                    # 接受该页面的LTPage对象
                    layout = device.get_result ()
                    if page_index == get_index or page_index-1 == get_index:
                        for x in layout:
                            if (isinstance(x, LTTextBoxHorizontal)):
                                print(x.get_text())
                                with open(save_path, 'a') as f:
                                    results = x.get_text().encode('gbk','ignore').decode('gbk')
                                    f.write(results + '\n')

            print(save_path.split('\\')[-1]+'信息提取成功')
    except Exception as e:
        print('未披露任何消息')
        with open (save_path, 'a') as f:
            f.write ('未披露相关内容'.encode('gbk','ignore').decode('gbk'))


if __name__ == '__main__':
    read_path = 'D:\\financial_reports\\sz_financial_reports\\sz_pdf\\2015_万科.PDF'
    save_path = 'D:\\financial_reports\\sz_financial_reports\\sz_txt\\2015_万科.txt'
    # 完整pdf的解析
    doc, interpreter, device = parse (read_path)
    # 获取有披露信息的页数
    index = get_content_index (doc, interpreter, device, save_path)
    # 保存对应页面中的所有内容
    get_content (doc, interpreter, device, index, save_path)
