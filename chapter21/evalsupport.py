# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/17 20:44
# @Author   : tangky
# @Site     : 
# @File     : evalsupport.py
# @Software : PyCharm

# 示例21-7 evaltime.py导入的模块
print('<[100]> evalsupport module start')


def deco_alpha(cls):
    print('<[200]> deco_alpha')

    def inner_1(self):
        print('<[300]> deco_alpha:inner_1')

    cls.method_y = inner_1
    return cls


class MetaAleph(type):
    print('<[400]> MetaAleph body')

    def __init__(cls, name, bases, dic):
        print('<[500]> MetaAleph.__init__')

        def inner_2(self):
            print('<[600]> MetaAleph.__init__:inner_2')

        cls.method_z = inner_2


print('<[700]> evalsupport module end')
