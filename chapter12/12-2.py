# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/10 16:12
# @Author   : tangky
# @Site     : 
# @File     : 12-2.py
# @Software : PyCharm
import collections


# class AnswerDict(dict):
class AnswerDict(collections.UserDict):
    def __getitem__(self, key):
        return 42


ad = AnswerDict(a='foo')
print(ad)
print(ad['a'])
d = {}
d.update(ad)
print(d['a'])
print(d)
