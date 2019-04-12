# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/12 11:39
# @Author   : tangky
# @Site     : 
# @File     : simple_coroutine.py
# @Software : PyCharm

# 示例16-1 可能是协程最简单的使用演示
def simple_coroutine(): # 协程使用生成器函数定义:定义体中有yield关键字
    print('-> coroutine started')
    x = yield # yield在表达式中使用:如果协程只需要从客户那里接受数据,那么产出值是None--这个值是隐式指定的,因为yield关键字右边没有表达式
    print('-> coroutine received:', x)

my_coro = simple_coroutine()
my_coro.send(None)
# print(my_coro) # 与创建生成器的方式一样,调用函数得到生成器对象
# next(my_coro)   # 首先要调用next(...)函数,因为生成器还没有启动,没有在yield语句处暂停,所以一开始无法发送数据
# my_coro.send(42) # 调用这个方法后,协程定义体中的yield表达式会计算出41;现在,协程会恢复,一直运行到下一个yield表达式,或者终止
# 这里,控制权流动到协程定义体的末尾,导致生成器像往常一样抛出StopIteration异常
