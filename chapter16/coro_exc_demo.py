# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/12 16:18
# @Author   : tangky
# @Site     : 
# @File     : coro_exc_demo.py
# @Software : PyCharm

# 示例16-8 coro_exc_demo.py:学习在协程中处理异常的测试代码
class DemoException(Exception):
    """为这次演示定义的异常类型"""


def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException:  # 特别处理DemoException异常
            print('*** DemoExceptiion handled. Continuing...')
        else:  # 如果没有异常,那么显示接受到的值
            print('-> coroutine received: {!r}'.format(x))
    raise RuntimeError('This line should never run.')  # 这一行永远不会执行
# 示例16-8 中的最后一行代码不会执行,因为只有未处理的异常才会中止那个无限循环,而一旦出现未处理的异常,协程会立即终止
# 示例16-9 激活和关闭demo_exc_handling,没有异常
exc_coro = demo_exc_handling()
next(exc_coro)
exc_coro.send(11)
exc_coro.send(22)
exc_coro.close()
from inspect import getgeneratorstate

print(getgeneratorstate(exc_coro))

# 示例16-10 把DemoException异常传入demo_exc_handling不会导致协程中止
exc_coro = demo_exc_handling()
next(exc_coro)
exc_coro.send(11)
exc_coro.throw(DemoException)
print(getgeneratorstate(exc_coro))

# 如果传入协程的异常没有处理,协程会停止,即状态变成'GEN_CLOSED'
# 示例16-11 如果无法处理传入的异常,协程会终止
exc_coro = demo_exc_handling()
next(exc_coro)
exc_coro.send(11)
try:
    exc_coro.throw(ZeroDivisionError)
except Exception:
    print(ZeroDivisionError)
print(getgeneratorstate(exc_coro))
