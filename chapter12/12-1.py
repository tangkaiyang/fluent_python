# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/10 15:58
# @Author   : tangky
# @Site     : 
# @File     : 12-1.py
# @Software : PyCharm
import collections


# class DoppelDict(dict):
class DoppelDict(collections.UserDict):
    def __setitem__(self, key, value):
        super(DoppelDict, self).__setitem__(key, [value] * 2)


dd = DoppelDict(one=1)  # 继承自dict的__init__方法忽略了我们覆盖的__setitem__方法:'one'的值没有重复
print(dd)
dd['two'] = 2  # []运算符会调用我们覆盖的__setitem__方法,
print(dd)
dd.update(three=3)  # 继承自dict的update方法也不使用我们覆盖的__setitem__方法
print(dd)
