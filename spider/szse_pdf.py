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
    show = 'pdf解码错误'

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
                    if '前五' in results or '前5' in results :
                        if '客户' in results or '供应商' in results or '供货商' in results:
                            content.append(page_index)
                            content.append (page_index + 1)
                            if '销售' in results or '关联' in results or '采购' in results:
                                content.append (page_index)
                                content.append (page_index + 1)

                    elif '主要' in results and '客户' in results and '和' in results and '供应商' in results:
                        content.append (page_index)
                        content.append (page_index + 1)

                show = 'pdf解码成功'
            # if len(set(content)) >= 4:
            #     print('本报告停止检索')
            #     break
    except Exception as e:
        print (save_path.split ('\\')[-1] + 'pdf解码错误')
        show = 'pdf解码错误'
        print(content)
    finally:
        return list(set(content)),show

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
                    if page_index == get_index :
                        for x in layout:
                            if (isinstance(x, LTTextBoxHorizontal)):
                                print(x.get_text())
                                with open(save_path, 'a') as f:
                                    results = x.get_text().encode('gbk','ignore').decode('gbk')
                                    f.write(results + '\n')

            print(save_path.split('\\')[-1]+'信息提取成功')
    except Exception as e:
        print('未披露任何消息',e)
        with open (save_path, 'a') as f:
            f.write ('未披露相关内容'.encode('gbk','ignore').decode('gbk'))

if __name__ == '__main__':
    sz_pdf_path = 'D:\\financial_reports\\sz_financial_reports\\sz_pdf'
    all_file_name = os.listdir (sz_pdf_path)
    for file in all_file_name:
        # 指定不同类型文件的保存地址
        fname = os.path.splitext (file)[0]
        read_path = os.path.join (sz_pdf_path, file)
        print(read_path)
        # 保存完整pdf内容的地址
        save_txt_path = 'D:\\financial_reports\\sz_financial_reports\\sz_txt_all'
        save_all_path = os.path.join(save_txt_path,fname+'.txt')
        # 保存需要分析的pdf内容的地址
        save_analysis_path = 'D:\\financial_reports\\sz_financial_reports\\sh_txt'
        save_simple_path = os.path.join(save_analysis_path,fname+'_simple'+'.txt')
        # print(read_path,save_all_path,save_simple_path)
        # 完整pdf的解析
        doc, interpreter, device = parse (read_path)
        # 获取有披露信息的页数
        index,show = get_content_index (doc, interpreter, device, save_all_path)
        if show == 'pdf解码成功':
            # 保存对应页面中的所有内容
            get_content (doc, interpreter, device, index, save_simple_path)
        else:
            with open (save_simple_path, 'a') as f:
                f.write (show.encode ('gbk', 'ignore').decode ('gbk'))