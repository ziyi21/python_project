#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'
import datetime,time
# with open('data/chatrooms/chatrooms_account.txt',encoding='utf8') as f:
#     results = f.readlines()
# for line in results:
#     if '大数据' in line or '数据家' in line or '学习' in line or '交流' in line or '数据分析与应用' in line or '智新赋能' in line or '实习信息' in line or '优惠' in line:
#         if '公安' not in line and '栖霞' not in line and ' 哈希大数据'!=line.replace(' ' ,''):
#             print(line)
    # print(f.readlines())

# with open('data/chatrooms/chatrooms_contents.txt',encoding='utf8') as f:
#     contents = f.readlines()
#
# send_contents = ''.join( content.replace('\xa0','') for content in contents )
# print(send_contents)


def timerfun(sched_time,path) :
    flag = 0
    while True:
        now = datetime.datetime.now()
        if now > sched_time and now < sched_time + datetime.timedelta(seconds=1) :  # 因为时间秒之后的小数部分不一定相等，要标记一个范围判断
            send_contents=get_contents(path)
            print(send_contents)
            time.sleep(1)    # 每次判断间隔1s，避免多次触发事件
            flag = 1
        else :
            #print('schedual time is {0}'.format(sched_time))
            #print('now is {0}'.format(now))
            if flag == 1 :
                # sched_time = sched_time + datetime.timedelta(days=1)  # 把目标时间增加一天，一天后触发再次执行
                sched_time = sched_time + datetime.timedelta (seconds=50)
                flag = 0

def get_contents(path):
    with open (path, encoding='utf8') as f:
        contents = f.readlines ()
    send_contents = ''.join (content.replace ('\xa0', '') for content in contents)
    return send_contents

if __name__ == '__main__':
    path = 'data/chatrooms/chatrooms_contents.txt'
    # send_contents = get_contents(path)
    sched_time = datetime.datetime (2018, 5, 1, 1,1 , 10)  # 设定初次触发事件的事件点
    print(sched_time)
    # SentChatRoomsMsg(send_contents)
    timerfun(sched_time,path)