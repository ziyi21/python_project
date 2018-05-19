#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

import itchat
import time , datetime

def timerfun(path) :
    while True:
        now = datetime.datetime.now()
        current_time = time.localtime (time.time ())
        if ((current_time.tm_hour == 8) and (current_time.tm_min == 0) and (current_time.tm_sec == 0)):
            print('bingo')
            send_contents = get_contents (path)
            # print(send_contents)
            SentChatRoomsMsg(send_contents)
            print(now, '全部发送成功')
            time.sleep (1)  # 每次判断间隔1s，避免多次触发事件

def SentChatRoomsMsg(send_contents):
    chatrooms = itchat.get_chatrooms(update=True)
    print(len(chatrooms))
    for one_name in chatrooms:
        name = one_name['NickName']
        if '大数据' in name or '数据家' in name or '学习' in name or '交流' in name or '数据分析与应用' in name or '智新赋能' in name or '实习信息' in name or '高级研修' in name : # or '优惠' in name

            if '公安' not in name and '栖霞' not in name and '哈希大数据'!= name.replace(' ' ,''):
                print (name)
                searchName = name
                iRoom = itchat.search_chatrooms(searchName)
                for room in iRoom:
                    if room['NickName'] == searchName:
                        userName = room['UserName']
                        print(room['NickName'])
                        # 实现发送消息的功能
                        itchat.send_msg(send_contents, userName)
                        print(userName,'发送成功')

        # elif '哈希数据科技' in name:
        #     searchName = name
        #     iRoom = itchat.search_chatrooms (searchName)
        #     for room in iRoom:
        #         if room['NickName'] == searchName:
        #             userName = room['UserName']
        #             print (room['NickName'])
        #             itchat.send_msg ('翔玉&老庄生日快乐哦', userName)
        #             print (userName, '发送成功')

        # 单独测试
        # if '相亲相爱' in one_name or '喜欢男神' in one_name:3
        #     searchName = one_name
        #     print(searchName)
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
    # itchat.auto_login(hotReload=True)  # 首次扫描登录后后续自动登录
    path = 'data/chatrooms/chatrooms_contents.txt'
    send_contents = get_contents(path)
    now = datetime.datetime.now ()
    current_time = time.localtime (time.time())
    print(current_time,send_contents)
    # SentChatRoomsMsg(send_contents)
    timerfun(path)
