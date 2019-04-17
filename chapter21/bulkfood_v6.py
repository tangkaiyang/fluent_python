# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/17 20:16
# @Author   : tangky
# @Site     : 
# @File     : bulkfood_v6.py
# @Software : PyCharm
# 使用Quantity和NonBlank描述符的LineItem类
import model_v5 as model


def entity(cls):  # 1.装饰器是一个类
    for key, attr in cls.__dict__.items():  # 2.迭代存储类属性的字典
        if isinstance(attr, model.Validated):  # 3.如果属性是Validated描述符实例...
            type_name = type(attr).__name__
            attr.storage_name = '_{}#{}'.format(type_name, key)  # 4...使用描述符类的名称和托管属性的名称命名storage_name
    return cls  # 5.


@entity  # 1.唯一的变化是添加了装饰器
class LineItem:
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    raisins = LineItem('Golden raisins', 10, 6.95)
    print(dir(raisins)[:3])
    print(LineItem.description.storage_name)
    print(raisins.description)
    print(getattr(raisins, '_NonBlank#description'))