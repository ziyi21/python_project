#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

from sklearn.datasets import make_regression
import os
import pandas as pd
import re
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# content = pd.read_excel('data/cut_words/results/data.xlsx',encoding='gbk')
# # ix 获取对应具体行列的具体内容，可以直接指定名称或者是填写索引
# X = content.ix[:,['readability','depth','density','tone']]
# y = content.ix[:,'ROE']
# # print(X,y)
# X_scaler = preprocessing.MinMaxScaler().fit_transform(X)
# # X_scaler = min_max_scaler.fit_transform(X)
# print(X_scaler)
# # 拆分测试集和训练集
# train_X , test_X, train_y , test_y = train_test_split(X, y, test_size=0.5,random_state=0)
# # 训练多元线性回归模型
# lr = LinearRegression().fit(train_X ,train_y)
# # 预测测试集房价结果
# predict_result_lr = lr.predict(test_X)
# # print(predict_result_lr)
#
# # 计算预测的准确性
# print('训练集模型准确率', lr.score(train_X, train_y))
# print('测试集模型准确率', lr.score(test_X, test_y))
# # print("最高房价值为：",np.max(price_y))
# # print("最低房价值为：",np.min(price_y))
# # print("房价的均值为",np.mean(price_y))

X, y ,coefs= make_regression(n_samples=300, n_features=8, noise=0.2,coef=True,n_informative=7,bias=2)
X_sample = pd.DataFrame(X)
# X_sample.ix[]
y_sample = pd.DataFrame(y,columns=['y'])
coefs_sample = pd.DataFrame(coefs,columns=['coef'])
table = pd.concat([X_sample,y_sample,coefs_sample],axis=1)
print(coefs_sample)

table_new = pd.DataFrame(table)
table_new.to_csv(r'data\cut_words\regression2.csv',encoding='gbk')