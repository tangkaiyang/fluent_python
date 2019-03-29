# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/3/29 19:24
# @Author   : tangky
# @Site     : 
# @File     : slice_test.py
# @Software : PyCharm

invoice = """
... 0.....6................................40........52...55........
... 1909 Pimoroni PiBrella $17.50 3 $52.50
... 1489 6mm Tactile Switch x20 $4.95 2 $9.90
... 1510 Panavise Jr. - PV-201 $28.00 1 $28.00
... 1601 PiTFT Mini Kit 320x240 $34.95 1 $34.95
... """
SKU = slice(0, 6)
print(SKU)
DESCRIPTION = slice(6, 40)
print(DESCRIPTION)
UNIT_PRICE = slice(40, 52)
print(UNIT_PRICE)
QUANTITY = slice(52, 55)
print(QUANTITY)
ITEM_TOTAL = slice(55, None)
print(ITEM_TOTAL)
line_items = invoice.split('\n')[2:]
for item in line_items:
    print(item[UNIT_PRICE], item[DESCRIPTION])