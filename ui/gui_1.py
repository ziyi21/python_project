#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'
import wx
class App(wx.App):
    def OnInit(self):
        frame = wx.Frame(parent=None,title = 'the first one')
        frame.Show()
        return True
app = App()
app.MainLoop()