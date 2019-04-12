# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/12 15:00
# @Author   : tangky
# @Site     : 
# @File     : coroaverager1.py.py
# @Software : PyCharm

# 示例16-6 coroaverager1.py: 使用@coroutine装饰器定义并测试计算移动平均值的协程


from coroutil import coroutine

@coroutine
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total/count

coro_avg = averager()
print(coro_avg.send(40))
# 使用@coroutine装饰器装饰的averager协程,可以立即开始发送值
print(coro_avg.send(50))
try:
    coro_avg.send('spam')
    # 发送的值不是数字,导致协程内部有异常抛出
except Exception:
    pass
coro_avg.send(60)
# 由于在协程内没有异常处理,协程会终止.如果试图重新激活协程会抛出StopIteration异常