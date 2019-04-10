# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/10 9:36
# @Author   : tangky
# @Site     : 
# @File     : frenchdeck2.py
# @Software : PyCharm

import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck2(collections.MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value):     # 为了支持洗牌,只需实现__setitem__方法
        self._cards[position] = value

    def __delitem__(self, position):            # 但是继承MutableSequence的类必须实现__delitem__方法,这是MutableSequence类的一个抽象方法
        del self._cards[position]

    def insert(self, position, value):          # 此外,还需要实现insert方法,这是MutableSequence类的第三个抽象方法
        self._cards.insert(position, value)
