# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/17 10:39
# @Author   : tangky
# @Site     : 
# @File     : bulkfood_v5.py
# @Software : PyCharm

# 示例20-7 使用Quantity和NonBlank描述符的LineItem类
import model_v5 as model # 1.

class LineItem:
    description = model.NonBlank() # 2.使用model.NonBlank描述符
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price