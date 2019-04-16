# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/16 10:13
# @Author   : tangky
# @Site     : 
# @File     : bulkfood_v2prop.py
# @Software : PyCharm


# 示例19-24 bulkfood_v2prop.py:quantity特性工厂函数
def quantity(storage_name):  # 1.storage_name参数确定各个特性的数据存储在哪里;对weight特性来说,存储的名称是'weight'
    def qty_getter(
            instance):  # 2.qty_getter函数的第一个参数可以命名为self,但是这么做很奇怪,因为qty_getter函数不在类定义体中;instance只带要把属性存储其中的LineItem实例
        return instance.__dict__[
            storage_name]  # 3.qty_getter引用了storage_name,把它保存在这个函数的闭包里;值直接从instance.__dict__中获取,为的是跳过特性,防止无限递归

    def qty_setter(instance, value):  # 4.定义qty_setter函数,第一个参数也是instance
        if value > 0:
            instance.__dict__[storage_name] = value  # 5.值直接存到instance.__dict__中,这也是为了跳过特性
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)  # 6.构建一个自定义的特性对象,然后将其返回


# 示例19-23 bulkfood_v2prop.py:使用特性工厂函数quantity
class LineItem:
    weight = quantity('weight')  # 1.使用工厂函数把第一个自定义的特性weight定义为类属性
    price = quantity('price')  # 2.构建另一个自定义的特性,price

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # 3.特性已激活,确保不能把weight设为负数或零
        self.price = price

    def subtotal(self):
        return self.weight * self.price  # 4.这里也用到了特性,使用特性获取实例中存储的值


if __name__ == '__main__':
    # 示例19-25 quantity特性工厂函数
    nutmeg = LineItem('Moluccan nutmeg', 8, 13.95)
    print(nutmeg.weight, nutmeg.price) # 1.通过特性读取weight和price,这回遮盖同名实例属性
    print(sorted(vars(nutmeg).items())) # 2.使用vars函数审查nutmeg实例,查看真正用于存储值的实例属性
    # print(sorted(nutmeg.__dict__.items()))
    # print(vars()) # vars()未设置参数,等价于locals(),设置参数vars(nutmeg) == nutmeg.__dict__
    # print(locals())
