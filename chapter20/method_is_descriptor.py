# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/17 16:18
# @Author   : tangky
# @Site     : 
# @File     : method_is_descriptor.py
# @Software : PyCharm

# 示例20-14 Text类,继承自UserString类
import collections


class Text(collections.UserString):
    def __repr__(self):
        return 'Text({!r})'.format(self.data)

    def reverse(self):
        return self[::-1]


if __name__ == '__main__':
    # 示例20-15 测试一个方法Text.reverse
    word = Text('forward')
    print(word)  # 1.Text实例的repr方法返回一个类似Text构造方法调用的字符串,可用于创建相同的实例
    print(word.reverse())  # 2.reverse方法返回反向拼写的单词
    print(Text.reverse(Text('backward')))  # 3.在类上调用方法相当于调用函数
    print(type(Text.reverse), type(word.reverse))  # 4.注意类型是不同的,一个是function,一个是method
    print(list(map(Text.reverse, ['repaid', (10, 20, 30), Text('stressed')]))) # 5.Text.reverse相当于函数,甚至可以处理Text实例之外的其他对象
    print(Text.reverse.__get__(word))  # 6.函数都是非覆盖型描述符.在函数上调用__get__方法是传入实例,得到的是绑定到那个实例上的方法
    print(Text.reverse.__get__(None, Text))  # 7.调用函数的__get__方法时,如果instance参数的值是None,那么得到的是函数本身
    print(word.reverse)  # 8.调用Text.reverse.__get__(word),返回对应的绑定方法
    print(word.reverse.__self__)  # 9.绑定方法对象有个__self__属性,其值是调用这个方法的实例引用.
    print(word.reverse.__func__ is Text.reverse)  # 10.绑定方法的__func__属性是依附在托管类上那个原始函数的引用
