# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/10 17:07
# @Author   : tangky
# @Site     : 
# @File     : 12-8.py
# @Software : PyCharm

print(bool.__mro__)


def print_mro(cls):
    print(', '.join(c.__name__ for c in cls.__mro__))


print_mro(bool)
from frenchdeck2 import FrenchDeck2

print_mro(FrenchDeck2)
import numbers

print_mro(numbers.Integral)
import io

print_mro(io.BytesIO)
print_mro(io.TextIOWrapper)
import tkinter
print_mro(tkinter.Text)
