#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

import itchat
import time , datetime

def timerfun(sched_time,path) :
    flag = 0
    while True:
        now = datetime.datetime.now()
        if now > sched_time and now < sched_time + datetime.timedelta(seconds=1) :  # 因为时间秒之后的小数部分不一定相等，要标记一个范围判断
            send_contents = get_contents(path)
            SentChatRoomsMsg(send_contents)
            print(now,'全部发送成功')
            time.sleep(1)    # 每次判断间隔1s，避免多次触发事件
            flag = 1
        else :
            #print('schedual time is {0}'.format(sched_time))
            #print('now is {0}'.format(now))
            if flag == 1 :
                sched_time = sched_time + datetime.timedelta(days=1)  # 把目标时间增加一天，一天后触发再次执行
                # sched_time = sched_time + datetime.timedelta (seconds=30)
                flag = 0

def SentChatRoomsMsg(send_contents):
    chatrooms = itchat.get_chatrooms(update=True)
    print(len(chatrooms))
    for one_name in chatrooms:
        one_name = one_name['NickName']
        if '大数据' in one_name or '数据家' in one_name or '学习' in one_name or '交流' in one_name or '数据分析与应用' in one_name or '智新赋能' in one_name or '实习信息' in one_name: # or '优惠' in one_name
            if '公安' not in one_name and '栖霞' not in one_name and '哈希大数据'!=one_name.replace(' ' ,''):
                searchName = one_name
                iRoom = itchat.search_chatrooms(searchName)
                for room in iRoom:
                    if room['NickName'] == searchName:
                        userName = room['UserName']
                        print(room['NickName'])
                        break
                print(send_contents)
                itchat.send_msg (send_contents, userName)
                print(userName,'发送成功')

        # 单独测试
        # if '相亲相爱' in one_name['NickName'] or '喜欢男神' in one_name['NickName']:
        #     searchName = one_name['NickName']
        #     iRoom = itchat.search_chatrooms(searchName)
        #     for room in iRoom:
        #         if room['NickName'] == searchName:
        #             userName = room['UserName']
        #             break
        #     itchat.send_msg (send_contents, userName)
        #     print(userName,'发送成功')
        # 获取好友列表的
        # friends = itchat.get_friends()
        # print(len(friends))
        # # for friend in friends:
        # #     print(friend['NickName'])

def get_contents(path):
    with open (path, encoding='utf8') as f:
        contents = f.readlines ()
    send_contents = ''.join (content.replace ('\xa0', '') for content in contents)
    return send_contents

if __name__ == '__main__':
    itchat.auto_login ()
    path = 'data/chatrooms/chatrooms_contents.txt'
    # send_contents = get_contents(path)
    sched_time = datetime.datetime (2018, 5, 1, 8, 00, 10)  # 设定初次触发事件的时间点
    print(sched_time)
    # SentChatRoomsMsg(send_contents)
    timerfun(sched_time,path)
