# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/10 14:06
# @Author   : tangky
# @Site     : 
# @File     : tombolist.py
# @Software : PyCharm

from random import randrange
from tombola import Tombola


@Tombola.register  # 把TomboList注册为Tombola的虚拟子类
class TomboList(list):  # Tombolist扩展list

    def pick(self):
        if self:  # Tombolist从list中继承__bool__方法,列表不为空时返回True
            position = randrange(len(self))
            return self.pop(position)  # pick调用继承自list的self.pop方法,传入一个随机的元素索引
        else:
            raise LookupError('pop from empty TomboList')

    load = list.extend  # Tombolist.load与list.extend一样

    def loaded(self):
        return bool(self)  # loaded方法委托bool函数,

    def inspect(self):
        return tuple(sorted(self))
# Tombola.register(TomboList) #Python3.3之前使用的标准调用句法
