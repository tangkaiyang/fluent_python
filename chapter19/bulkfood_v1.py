# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/16 16:35
# @Author   : tangky
# @Site     : 
# @File     : bulkfood_v1.py
# @Software : PyCharm

# 示例19-15 最简单的LineItem类
class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
