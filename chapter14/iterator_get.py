# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 9:52
# @Author   : tangky
# @Site     : 
# @File     : iterator_get.py
# @Software : PyCharm

# 一个简单的for循环,迭代一个字符串.背后是由迭代器的
s = 'ABC'
for char in s:
    print(char)

# 如果没有for语句,不得不使用while循环模式:
it = iter(s)
while True:
    try:
        print(next(it))
    except StopIteration:
        del it
        break

"""
使用可迭代的对象构建迭代器it
不断在迭代器上调用next函数,获取下一个字符
如果没有字符了,迭代器会抛出StopIteration异常
释放对it的引用,即废弃迭代器对象
退出循环
"""