# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/12 14:54
# @Author   : tangky
# @Site     : 
# @File     : coroutil.py
# @Software : PyCharm

# 示例16-5 coroutil.py: 预激协程的装饰器
from functools import wraps
def coroutine(func):
    """装饰器:向前执行到第一个`yield`表达式,预激`func`"""
    @wraps(func)
    def primer(*args, **kwargs): # 把被装饰的生成器函数替换成这里的primer函数;调用primer函数时,返回预激后的生成器
        gen = func(*args, **kwargs)
        next(gen)       # 预激生成器
        return gen      # 返回生成器
    return primer

