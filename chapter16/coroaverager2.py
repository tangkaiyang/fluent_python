# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/12 16:43
# @Author   : tangky
# @Site     : 
# @File     : coroaverager2.py
# @Software : PyCharm


# 示例16-13 coroaverager2.py: 定义一个求平均值的协程,让它返回一个结果
# yield:产生
from collections import namedtuple

Result = namedtuple('Result', 'count average')

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break  # 为了返回值,协程必须正常终止;
        total += term
        count += 1
        average = total/count
    return Result(count, average)  # 返回一个namedtuple,包含count和average两个字段.

# 示例16-14 coroaverager2.py: 说明averager行为的doctest
# coro_avg = averager()
# next(coro_avg)
# coro_avg.send(10)
# coro_avg.send(30)
# coro_avg.send(6.5)
# coro_avg.send(None)
# 发送None会终止循环,导致协程结束,返回结果.生成器对象会抛出StopIteration异常.
# 异常对象的value属性保存着返回的值
# 注意,return表达式的值会偷偷传给调用方,赋值给StopIteration异常的一个属性.
# 这样做有点不合常理,但是能保留生成器对象的常规行为--耗尽时抛出StopIteration异常

# 示例16-15 展示如何获取协程返回的值
# 示例16-15 捕获StopIteration异常,获取averager返回的值
coro_avg = averager()
next(coro_avg)
coro_avg.send(10)
coro_avg.send(30)
coro_avg.send(6.5)
try:
    coro_avg.send(None)
except StopIteration as exc:
    result = exc.value
print(result)
