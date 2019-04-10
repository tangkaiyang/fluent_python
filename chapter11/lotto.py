# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/10 13:42
# @Author   : tangky
# @Site     : 
# @File     : lotto.py
# @Software : PyCharm

import random
from tombola import Tombola


class LotteryBlower(Tombola):
    def __init__(self, iterable):
        self._balls = list(iterable)
        # 没有直接把iterable赋值个self._balls,这样使得LotteryBlower更灵活,iterable参数可以是任何可迭代类型
        # list(iterable)创建副本,这样,客户传入的列表iterable就不会被修改

    def load(self, iterable):
        self._balls.extend(iterable)

    def pick(self):
        try:
            position = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError('pick from empty LotteryBlower')
        return self._balls.pop(position)

    def loaded(self):
        return bool(self._balls)

    def inspect(self):  # inspect 检查
        return tuple(sorted(self._balls))
