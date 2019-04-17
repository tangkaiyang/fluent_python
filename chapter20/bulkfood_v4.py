# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/17 7:53
# @Author   : tangky
# @Site     : 
# @File     : bulkfood_v4.py
# @Software : PyCharm

# 示例20-2 每个Quantity描述符都有独一无二的storage_name
class Quantity:
    __counter = 0  # 1.__counter是Quantiry类的类属性,统计Quantity实例的数量

    def __init__(self):
        cls = self.__class__  # 2.cls是Quantity类的引用
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix,
                                            index)  # 3.每个描述符实例的storage_name属性都是独一无二的,因为其值由描述符类的名称和__counter属性的当前值构成(例如,_Quantity#0)
        cls.__counter += 1  # 4.递增__counter属性的值

    def __get__(self, instance, owner):  # 5.实现__get__方法,因为托管属性的名称与storage_name不同
        return getattr(instance, self.storage_name)  # 6.使用内置的getattr函数从instance中获取储存属性的值

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)  # 7.使用内置的setattr函数把值存储在instance中
        else:
            raise ValueError('value must be > 0')


class LineItem:
    weight = Quantity()  # 8.不用把托管属性的名称传给Quantity构造方法
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    cocounts = LineItem('Brazilian cocount', 20, 17.95)
    print(cocounts.weight, cocounts.price)
    print(getattr(cocounts, '_Quantity#0'), getattr(cocounts, '_Quantity#1'))
    # LineItem.weight
    """
    LineItem.weight抛出AttributeError异常,
    AttributeError: 'NoneType' object has no attribute '_Quantity#0'
    抛出AttributeError异常时实现__get__方法的方式之一,
    如果选择这么做,应该修改错误信息,去掉NoneType和_Quantity#0,这是实现细节.
    改成"'LineItem' class has no such attribute"更好.
    最好能给出缺少的属性名,但是在这个示例中,描述符不知道托管属性的名称
    """
