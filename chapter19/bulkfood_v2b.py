# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/16 16:49
# @Author   : tangky
# @Site     : 
# @File     : bulkfood_v2b.py
# @Software : PyCharm

# 示例19-18 效果与示例19-17一样,只不过没有使用装饰器
class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    def get_weight(self):  # 1.普通的读值方法
        return self.__weight

    def set_weight(self, value):  # 2.普通的设值方法
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')

    weight = property(get_weight, set_weight)  # 3.构建property对象,然后赋值给公开的类属性
