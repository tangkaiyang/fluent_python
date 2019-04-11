# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 10:46
# @Author   : tangky
# @Site     : 
# @File     : sentence_iter.py
# @Software : PyCharm

import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        return SentenceIterator(self.words)


class SentenceIterator:
    def __init__(self, words):
        self.words = words
        self.index = 0

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word

    def __iter__(self):
        return self
"""
与前一版相比,这里只多了一个__iter__方法.这一版没有__getitem__方法,为的是明确表明这个类可以迭代,因为实现了__iter__方法
根据可迭代协议,__iter__方法实例化并返回一个迭代器
SentenceIterator示例引用单词列表
self.index用于确定下一个要获取的单词
如果self.index索引位上没有单词,那么抛出StopIteration异常
注意,对这个示例来说,其实没必要在SentenceIterator类中实现__iter__方法,这么做是因为迭代器应该实现__next__和__iter__两个方法,
而且这么做能让迭代器通过issubclass(SentenceInterator, abc.Iterator)测试.如果让SentenceIterator类继承abc.Iterator类,
那么它会继承abc.Iterator.__iter__这个具体方法
"""