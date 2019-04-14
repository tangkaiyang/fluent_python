# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/12 17:27
# @Author   : tangky
# @Site     : 
# @File     : coroaverager3.py.py
# @Software : PyCharm

# 示例16-17 coroaverager3.py: 使用yield from计算平均值并输出统计报告
from collections import namedtuple

Result = namedtuple('Result', 'count average')


# 子生成器
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:  # 至关重要的终止条件.如果不这么做,使用yield from调用这个协程的生成器会永远阻塞
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)  # 返回的Result会成为grouper函数中yield from表达式的值


# 委派生成器
def grouper(results, key):
    while True:
        results[key] = yield from averager()  # 这个循环每次迭代时会新建一个averager实例;每个实例都是作为协程使用的生成器对象


"""grouper发送的每个值都会经由yield from处理,通过管道传给averager实例.grouper会在yield from表达式处暂停,等待averager实例处理客户端发来的值.averager实例运行完毕后,
返回的值绑定到results[key]上.while循环会不断创建averager实例,处理更多的值 """


# 输出报告
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
            result.count, group, result.average, unit
        ))


# 客户端代码,即调用方
def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        next(group)
        for value in values:
            group.send(value)
        group.send(None)  # 重要!
    print(results) # 如果要调试,去掉注释
    report(results)


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}

if __name__ == '__main__':
    main(data)


"""
上述示例的运作方式
~外层for循环每次迭代会新建一个grouper实例,赋值给group变量;group是委派生成器
~调用next(group),预激委派生成器grouper,此时进入while True循环,调用子生成器averager后,在yield from表达式处暂停
~内层for循环调用group.send(value),直接把值传给子生成器averager.同时,当前grouper实例(group)在yield from表达式处暂停
~内层循环结束后,group实例依旧在yield from表达式处暂停,因此,grouper函数定义体中为results[key]赋值的语句还没有执行
~如果外城for循环的末尾没有group.send(None),那么averager子生成器永远不会终止,委派生成器group永远不会再次激活,因此永远不会为results[key]赋值.
~外层for循环重新迭代时会新建一个grouper实例,然后绑定到group实例(以及它创建的尚未终止的averager子生成器实例)被垃圾回收程序回收
"""