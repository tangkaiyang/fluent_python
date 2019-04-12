# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/12 13:48
# @Author   : tangky
# @Site     : 
# @File     : simple_coro2.py
# @Software : PyCharm

# 示例16-2 产出两个值的协程
def simple_coro2(a):
    print('-> Started: a =', a)
    b = yield a
    print('-> Received: b =', b)
    c = yield a + b
    print('-> Received: c =', c)

my_coro2 = simple_coro2(14)
from inspect import getgeneratorstate

print(getgeneratorstate(my_coro2))
# print(next(my_coro2))
next(my_coro2)
print(getgeneratorstate(my_coro2))
# print(my_coro2.send(28))
my_coro2.send(28)
try:
    # print(my_coro2.send(99))
    my_coro2.send(99)
except StopIteration:
    print(StopIteration)

print(getgeneratorstate(my_coro2))