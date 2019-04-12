# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/12 17:27
# @Author   : tangky
# @Site     : 
# @File     : coroaverager3.py.py
# @Software : PyCharm

# 示例16-17 coroaverager3.py: 使用yield from计算平均值并输出统计报告
from collections import namedtuple

Result = namedtuple('Result', 'count average')
