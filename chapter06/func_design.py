# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/3 19:22
# @Author   : tangky
# @Site     : 
# @File     : func_design.py
# @Software : PyCharm

"""
第六章 使用一等函数实现设计模式
使用函数对象重构"策略"模式,
一种更简单的方式,简化"命令"模式
6.1 案例分析:重构"策略"模式
6.1.1 经典的"策略"模式
上下文:把一些计算委托给不同算法的可互换组件,它提供服务.
策略:实现不同算法的组件共同的接口
具体策略:策略的具体子类
"""
# 示例6-1 实现Order类,支持插入式折扣策略
from abc import ABC, abstractmethod
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')  # fidelity忠诚度


class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:  # 上下文
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


class Promotion(ABC):  # 策略:抽象基类
    @abstractmethod
    def discount(self, order):
        """返回折扣金额(正值)"""


class FidelityPromo(Promotion):  # 第一个具体策略
    """为 积分为1000或以上的顾客提供5%折扣"""

    def discount(self, order):
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0


class BulkItemPromo(Promotion):  # 第二个具体策略
    """单个商品为20个或以上时提供10%折扣"""

    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * .1
        return discount


class LargeOrderPromo(Promotion):  # 第三个具体策略
    """订单中的不同商品达到10个或以上时提供7%折扣"""

    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * .07
        return 0
# Promotion定义为抽象基类(Abstract Base Class, ABC),为了使用@abstractmethod装饰器,从而明确表明所用的模式
# Python3.4中,声明抽象基类最简单的方式是子类化abc.ABC
# Python3.0到Python3.3,class Promotion(metaclass=ABCMeta)
# 示例6-2 使用不同促销折扣的Order类示例
joe = Customer('John Doe', 0)
ann = Customer('Ann Smith', 1000)
cart = [LineItem('banana', 4, .5),
        LineItem('apple', 10, 1.5),
        LineItem('watermelon', 5, 5.0)]
print(Order(joe, cart, FidelityPromo()))
print(Order(ann, cart, FidelityPromo()))
banana_cart = [LineItem('banana', 30, .5),
               LineItem('apple', 10, 1.5)]
print(Order(joe, banana_cart, BulkItemPromo()))
long_order = [LineItem(str(item_code), 1, 1.0)
              for item_code in range(10)]
print(Order(joe, long_order, LargeOrderPromo()))
print(Order(joe, cart, LargeOrderPromo()))