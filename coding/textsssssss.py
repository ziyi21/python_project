#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'
import os
from pypinyin import pinyin,lazy_pinyin
import pandas as pd
#
# folder = 'data/movie/'
# isCreated=os.path.exists(folder)
# print(isCreated)
#
# def create_foleder(foldernames):
#     current_position="data/movie/"
#     foldername=str(current_position)+str(foldernames)+"/"
#     isCreated=os.path.exists(foldername)
#     if not isCreated:
#         os.makedirs(foldername)
#         print(str(foldername)+'is created')
#         return foldername
#     else:
#         print("the folder has been created before")
#         return foldername
#
# if __name__ == '__main__':
#     movie_name = '头号玩家'
#     url = 'http://search.mtime.com/search/?q={}'.format (movie_name)
#     movie_name_pinyin = lazy_pinyin(movie_name)
#     foldernames = '_'.join(i for i in movie_name_pinyin)
#     path_name = create_foleder (foldernames)
#     print('path_name' , path_name)
#     print('_'.join(i for i in movie_name_pinyin))
#     # create_foleder()

df = pd.read_csv('data/movie/movie_list.csv',encoding = 'gbk')
print(df['movie_name'].values.tolist())
