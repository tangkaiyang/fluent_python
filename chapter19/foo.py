# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/16 17:24
# @Author   : tangky
# @Site     : 
# @File     : foo.py
# @Software : PyCharm

class Foo:
    @property
    def bar(self):
        """The bar attribute"""
        return self.__dict__['bar']

    @bar.setter
    def bar(self, value):
        self.__dict__['bar'] = value