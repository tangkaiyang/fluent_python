# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 7:23
# @Author   : tangky
# @Site     : 
# @File     : bingoaddable.py
# @Software : PyCharm


import itertools
from tombola import Tombola
from bingo import BingoCage


class AddableBingoCage(BingoCage):
    def __add__(self, other):
        if isinstance(other, Tombola):
            return AddableBingoCage(self.inspect() + other.inspect())
        else:
            return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Tombola):
            other_iterable = other.inspect()
        else:
            try:
                other_iterable = iter(other)
            except TypeError:
                self_cls = type(self).__name__
                msg = "right operand in += must be {!r} or an iterable"
                raise TypeError(msg.format(self_cls))
        self.load(other_iterable)
        return self # 增量赋值特殊方法必须返回self
