# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/17 9:35
# @Author   : tangky
# @Site     : 
# @File     : bulkfood_v4b.py
# @Software : PyCharm

# 示例20-3 通过托管类调用时,__get__方法返回描述符的引用


class Quantity:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self # 1.如果不是通过实例调用,返回描述符本身
        else:
            return getattr(instance, self.storage_name) # 2.否则,返回托管属性的值

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must be > 0')


class LineItem:
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    print(LineItem.weight)
    br_nuts = LineItem('Brazil nuts', 10, 34.95)
    print(br_nuts.price)