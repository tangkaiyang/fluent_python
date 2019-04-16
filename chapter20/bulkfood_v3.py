# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/16 20:14
# @Author   : tangky
# @Site     : 
# @File     : bulkfood_v3.py
# @Software : PyCharm


# 示例20-1 使用Quantity描述符管理LineItem的属性
class Quantity:  # 1.描述符基于协议实现,无需创建子类
    def __init__(self, storage_name):
        self.storage_name = storage_name  # 2.Quantity实例有个storage_name属性,这是托管实例中存储值的属性的名称

    def __set__(self, instance, value):  # 3.尝试为托管属性赋值时,会调用__set__方法.这里,self是描述符实例,instance是托管实例,value是要设定的值
        if value > 0:
            instance.__dict__[
                self.storage_name] = value  # 4.必须直接处理托管实例的__dict__属性;如果使用内置的setattr函数,会再次出发__set__方法,导致无限递归
        else:
            raise ValueError('value must be > 0')


class LineItem:
    weight = Quantity('weight')  # 5.第一个描述符绑定给weight属性
    price = Quantity('price')  # 6.第二个描述符绑定给price属性

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
