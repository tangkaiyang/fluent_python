# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/12 14:10
# @Author   : tangky
# @Site     : 
# @File     : coroaverager0.py
# @Software : PyCharm

# 示例16-3 coroaverager0.py: 定义一个计算移动平均值的协程
def averager():
    total = 0.0
    count = 0
    average = None
    while True:  # 只要调用方不断把值发送给这个协程,它就会一直接收值,然后生成结果.仅当调用方在协程上调用.close()方法,或者没有对协程的引用而被垃圾回收程序回收时,这个协程才会终止
        term = yield average # 这里的yield表达式用于暂停执行协程,把结果发给调用方;还用于接收调用方后面发给协程的值,恢复无限循环
        total += term
        count += 1
        average = total/count
# 使用协程的好处是,total和count声明为局部变量即可,无需使用实例属性或闭包在多次调用之间保持上下文
# 示例16-4 coroaverager0.py的测试
coro_avg = averager()
next(coro_avg) # 调用next函数,预激协程,也可以使用.send(None)
coro_avg.send(30)
# coro_avg.close() # 停止协程(还有其他方法),coro_avg = averager()重新启动协程