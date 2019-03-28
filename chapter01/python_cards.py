# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/3/28 19:51
# @Author   : tangky
# @Site     : 
# @File     : python_cards.py
# @Software : PyCharm


import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


beer_card = Card('7', 'diamonds')
print(beer_card)

deck = FrenchDeck()
print(deck[0])
print(deck[-1])

from random import choice

print(choice(deck))
print(choice(deck))

print(deck[:3])
print(deck[12::13])

for card in deck:
    print(card)
for card in reversed(deck):
    print(card)

"""
如果一个集合类型没有实现__contains__方法,那么in运算符就会按顺序做一次迭代搜索
"""

suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]


for card in sorted(deck, key=spades_high):
    print(card)

"""
特殊方法的存在是为了被Python解释器调用的,自己不需要去调用他们,
即没有my_object.__len__()这种写法,而是应该使用len(object).
在执行len(my_object)的时候,如果my_object是一个自定义类的对象,那么Python会自己去调用其中由你实现的__len__方法
然而如果是Python内置的类型,比如列表list,字符串str,字节序列bytearray等,
那么CPython会抄近路,__len__实际上会直接返回PyVarObject里的ob_size属性.
"""