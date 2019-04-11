# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 15:21
# @Author   : tangky
# @Site     : 
# @File     : artiprog_v3.py
# @Software : PyCharm

import itertools

def aritprog_gen(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)
    if end is not None:
        ap_gen = itertools.takewhile(lambda n: n < end, ap_gen)
    return ap_gen
