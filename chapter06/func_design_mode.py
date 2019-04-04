# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/4 11:07
# @Author   : tangky
# @Site     : 
# @File     : func_design_mode.py
# @Software : PyCharm

"""
6.1.2 使用函数实现策略模式
示例6-1中,每个具体策略都是一个类,而且都只定义了一个方法,即discount.
此外,策略实例没有状态(没有实例属性)
把具体策略换成简单的函数,而且去掉了Promo抽象类
"""
# 示例6-3 Order类和使用函数实现的折扣策略
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')


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
        self.pormotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.pormotion is None:
            discount = 0
        else:
            discount = self.pormotion(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


def fidelity_promo(order):
    """为积分为1000或以上的顾客提供5%折扣"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0


def bulk_item_promo(order):
    """单个商品为20个或以上时提供10%折扣"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount


def large_order_promo(order):
    """订单中的不同商品达到10个或以上时提供7%折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * 0.7
    return 0
# 示例6-4 使用函数实现的促销折扣的Order类示例
joe = Customer('John Doe', 0)
ann = Customer('Ann Smith', 1100)
cart = [LineItem('banana', 4, .5),
        LineItem('apple', 10, 1.5),
        LineItem('watermelon', 5, 5.0)]
print(Order(joe, cart, fidelity_promo))
print(Order(ann, cart, fidelity_promo))
banana_cart = [LineItem('banana', 30, .5),
               LineItem('apple', 10, 1.5)]
print(Order(joe, banana_cart, bulk_item_promo))
long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
print(Order(joe, long_order, large_order_promo))
print(Order(joe, cart, large_order_promo))

# 6.1.3 选择最佳策略:简单的方式

# promos = [fidelity_promo, bulk_item_promo, large_order_promo]

def best_promo(order):
    """选择可用的最佳折扣"""
    return max(promo(order) for promo in promos)
# 示例6-5 best_promo函数计算所有折扣,并返回额度最大的
# print(Order(joe, long_order, best_p

"""
6.1.4 找出模块中的全部策略
模块也是一等对象,而且标准库中提供了几个处理模块的函数.
globals():返回一个字典,表示当前的全局符号表.这个符号表始终针对当前模块(对函数或方法来说,是指定义他们的模块,而不是调用他们的模块)
示例6-7 使用globals函数帮助best_promo自动找到其他可用的*_promo函数,过程有点曲折
"""
# 示例6-7 内省模块的全局变量空间,构建promos列表
# promos = [globals()[name] for name in globals()
#           if name.endswith('_promo')
#           and name != 'best_promo'] # 过滤掉best_promo自身,防止无限递归
# print(promos)
# print(globals())
"""
收集所有可用促销的另一种方法是,在一个单独的模块中保存所有策略函数,把best_promo排除在外
示例6-8中,最大的变化是内省名为promotions的独立模块,构建策略函数列表,构建策略函数列表.
注意:要导入promotions模块,以及提供高阶内省函数的inspect模块
"""
# 示例6-8 内省单独的promotions模块,构架promos列表
import promotions
import inspect

# print(inspect.signature(best_promo))
promos = [func for name, func in inspect.getmembers(promotions, inspect.isfunction)]
print(promos)
"""
inspect.getmembers函数用于获取对象(这里是promotions模块)的属性,第二个参数是可选的判断条件(一个布尔值函数).
我们使用的是inspect.isfunction,只获取模块中的函数
示例6-8不管命名策略,但是promotions模块只能包含计算订单折扣的函数
???当然,这是对代码的隐性假设.如果有人在promotions模块中使用不同的签名定义函数,那么best_promo函数尝试将其应用到订单上时会出错
我们可以添加更为严格的测试,审查传给实例的参数,进一步过滤函数.
示例6-8强调模块内省的一种用途
动态收集促销折扣函数更为显式的一种方案是使用简单的装饰器.
"""
