# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/14 19:46
# @Author   : tangky
# @Site     : 
# @File     : demo_executor_map.py
# @Software : PyCharm


# 示例17-6 demo_executor_map.py:简单演示ThreadPoolExecutor类的map方法
from time import sleep, strftime
from concurrent import futures


# 1.把传入的参数打印出来,并在前面加上[HH:MM:SS]格式的时间戳
def display(*args):
    print(strftime('[%H:%M:%S'), end=' ')
    print(*args)


# 2.在开始时显示一个消息,然后休眠n秒,最后在结束时再显示一个消息;消息使用制表符缩进,缩进量由n决定
def loiter(n):
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t' * n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t' * n, n))
    # 3.loiter函数返回n*10
    return n * 10


def main():
    display('Script starting.')
    # 4.创建ThreadPoolExecutor实例,有3个线程
    executor = futures.ThreadPoolExecutor(max_workers=3)
    # 5.把五个任务提交个executor(因为只有3个线程,所以只有三个任务立即开始:loiter(0),loiter(2), loiter(3);这是非阻塞调用)
    results = executor.map(loiter, range(5))
    # 6.立即显示调用executor.map方法的结果:一个生成器
    display('results:', results)
    display('Waiting for individual results:')
    # 7.for循环中enumerate函数会隐式调用next(results),这个函数又会在(内部)表示第一任务(loiter(0))的_f期物上调用_f.result()方法.result方法会阻塞,知道期物运行结束,因此这个循环每次迭代是都要等待下一个结果做好准备
    for i, result in enumerate(results):
        display('result {}: {}'.format(i, result))


main()
