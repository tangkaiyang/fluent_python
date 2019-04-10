# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/10 13:25
# @Author   : tangky
# @Site     : 
# @File     : bingo.py.py
# @Software : PyCharm

import random
from tombola import Tombola


class BingoCage(Tombola):  # 明确指定BingoCage类扩展Tombola类
    def __init__(self, items):
        self._randomizer = random.SystemRandom()  # 假设我们将在线上游戏中使用这个.random.SystemRandom使用os.urandom()函数实现random API.os.urandom()函数生成"适合用于加密"的随机字节序列
        self._items = []
        self.load(items)  # 委托.load()方法实现初始加载

    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)  # 没有使用random.shuffle()函数,而是使用SystemRandom实例的.shuffle()方法

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):  # 没有必要满足Tombola接口,添加额外的方法没有问题
        self.pick()
