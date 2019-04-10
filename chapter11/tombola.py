# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/10 11:01
# @Author   : tangky
# @Site     : 
# @File     : tombola.py
# @Software : PyCharm

import abc


class Tombola(abc.ABC):                 # 自己定义的抽象基类要继承abc.ABC
    @abc.abstractmethod
    def load(self, iterable):           # 抽象方法使用@abstractmethod装饰器标记,而且定义体重通常只有文档字符串
        """从可迭代对象中添加元素"""

    @abc.abstractmethod
    def pick(self):                     # 根据文档字符串,如果没有元素可选,应该抛出LookupError
        """随机删除元素,然后将其返回
        如果实例为空,这个方法应该抛出'LookupError"""

    def loaded(self):                   # 抽象基类中可以包含具体方法
        """如果至少有一个元素,返回'True', 否则返回'False'"""
        return bool(self.inspect())     # 抽象方法中的具体方法只能依赖抽象基类定义的接口(即只能使用抽象基类中的其他具体方法,抽象方法或特性)

    def inspect(self):
        """返回一个有序元组,由当前元素构成"""
        items = []
        while True:                     # 我们不知道具体子类如何存储元素,不过为了得到inspect的结果,我们可以不断调用.pick()方法,把Tombola清空....
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)                # 然后使用.load()把所有元素放回去
        return tuple(sorted(items))
