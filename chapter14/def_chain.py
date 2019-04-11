# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 19:47
# @Author   : tangky
# @Site     : 
# @File     : def_chain.py
# @Software : PyCharm


def chain(*iterables):
    for it in iterables:
        yield from it
        # for i in it:
        #     yield i

s = 'ABC'
t = tuple(range(3))
print(list(chain(s, t)))
#chain生成器函数把操作依次交给接受到的各个可迭代对象处理
#引入了新句法

