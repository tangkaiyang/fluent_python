# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/18 7:54
# @Author   : tangky
# @Site     : 
# @File     : bulkfood_v7.py
# @Software : PyCharm
# 示例21-14 有元类的支持,继承model.Entity类即可
import model_v7 as model


class LineItem(model.Entity):  # 1.LineItem是model.Entity的子类
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
