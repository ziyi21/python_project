#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

import os
# 批量修改路径与文件名（要修改的目录名）
def Modifyprefix(Path,oldtype,newtype):
    all_file_list = os.listdir(Path)                            #列出指定目录下的所有文件
    for file_name in all_file_list:
        currentdir =os.path.join(Path, file_name)               #连接指定的路径和文件名or文件夹名字
        fname = os.path.splitext(file_name)[0]                  #分解出当前的文件路径名字
        ftype = os.path.splitext(file_name)[1]                  #分解出当前的文件扩展名
        if oldtype in ftype:
            repltype =ftype.replace(oldtype,newtype)      #将原文件名中的'oldcontent'字符串内容全替换为'newcontent'字符串内容
            # 方法一，直接切换操作位置
            newname = fname + repltype
            os.chdir(path) # 切换到对应文件的路径下再去操作文件内容
            os.rename(file_name,newname) # 重命名文件名称
            # 方法二，指定文件位置后进行操作
            # newname = os.path.join(Path,fname+repltype)         #文件路径与新的文件名字+原来的扩展名
            # os.rename(currentdir,newname)                       #重命名文件名称需要文件的地址+名称一起指定

if __name__ == '__main__':
    # 要修改的文件的地址
    path = "C:\\Users\\Think\\Desktop\\ps_ppt"
    oldtype = '.ppt'
    newtype = '.ppsx'
    # 调用修改文件后缀名的函数
    Modifyprefix(path,oldtype,newtype)