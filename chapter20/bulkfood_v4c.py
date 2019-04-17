# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/17 9:43
# @Author   : tangky
# @Site     : 
# @File     : bulkfood_v4c.py
# @Software : PyCharm

# 示例20-4 整洁的LineItem类;Quantity描述符类现在位于导入的模块中
import bulkfood_v4b as model


class LineItem:
    weight = model.Quantity()  # 2.使用model.Quantity描述符
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
