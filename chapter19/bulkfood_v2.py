# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/16 16:41
# @Author   : tangky
# @Site     : 
# @File     : bulkfood_v2.py
# @Software : PyCharm

# 示例19-17 定义了weight特性的LineItem类

class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # 1.已经使用特性的设值方法了
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    @property  # 2.装饰读值方法
    def weight(self):  # 3.实现特性的方法,名称与公开属性一样weight
        return self.__weight  # 4.真正的值存储在私有属性__weight中

    @weight.setter  # 5.被装饰的读值方法有个.setter属性,这个属性也是装饰器;这个装饰器把读值方法和设值方法绑定在一起
    def weight(self, value):
        if value > 0:
            self.__weight = value  # 6.如果值大于零,设置私有属性__weight
        else:
            raise ValueError('value must be > 0')  # 7.否则,抛出ValueError异常
