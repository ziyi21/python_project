#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'
# -*- coding: cp936 -*-

import wx
import string
app=wx.App()
win=wx.Frame(None,title='计算器',size=(410,335))
bg=wx.Panel(win)

def result(event):
    a=entfile1.GetValue()
    b=entfile2.GetValue()
    f=flofile.GetValue()
    if f=='+':
        res=int(a)+int(b)
        refile.SetValue(a+f+b+'='+str(res))
    elif f=='-':
        res=int(a)-int(b)
        refile.SetValue(a+f+b+'='+str(res))
    elif f=='*':
        res=int(a)*int(b)
        refile.SetValue(a+f+b+'='+str(res))
    elif f=='%':
        res=float(a)/int(b)
        refile.SetValue(a+f+b+'='+str(res))

rebut=wx.Button(bg,label='OK')

rebut.Bind(wx.EVT_BUTTON,result)

entfile1=wx.TextCtrl(bg)
entfile2=wx.TextCtrl(bg)
flofile=wx.TextCtrl(bg)
refile=wx.TextCtrl(bg)

level=wx.BoxSizer()
level.Add(entfile1,proportion=1,flag=wx.EXPAND)
level.Add(flofile,proportion=0,flag=wx.LEFT,border=5)
level.Add(entfile2,proportion=1,flag=wx.EXPAND|wx.LEFT,border=5)

down=wx.BoxSizer(wx.VERTICAL)
down.Add(level,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
down.Add(rebut,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=5)
down.Add(refile,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)

bg.SetSizer(down)

win.Show()
app.MainLoop()