# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/8 17:26
# @Author   : tangky
# @Site     : 
# @File     : clockdeco.py
# @Software : PyCharm

import time

def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked