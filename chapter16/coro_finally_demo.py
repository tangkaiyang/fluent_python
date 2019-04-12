# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/12 16:35
# @Author   : tangky
# @Site     : 
# @File     : coro_finally_demo.py
# @Software : PyCharm

# 示例16-12 coro_finally_demo.py: 使用try/finally块在协程终止时执行操作
class DemoException(Exception):
    """为这次演示定义的异常类型"""

def demo_finally():
    print('-> coroutine started')
    try:
        while True:
            try:
                x = yield
            except DemoException:
                print('*** DemoException handled. Continuing...')
            else:
                print('-> coroutine received: {!r}'.format(x))
    finally:
        print('-> coroutine ending')
