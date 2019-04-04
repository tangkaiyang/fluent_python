# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/4 15:24
# @Author   : tangky
# @Site     : 
# @File     : registration.py
# @Software : PyCharm

registry = []


def register(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func


@register
def f1():
    print('running f1()')


@register
def f2():
    print('running f2()')


def f3():
    print('running f3()')


def main():
    print('running main()')
    print('registry ->', registry)
    f3()
    f1()
    f2()


if __name__ == '__main__':
    main()

"""
import registration时,控制台会打印出
running register(<function f1 at 0x00000000050BA950>)
running register(<function f2 at 0x00000000050BAA60>)
函数装饰器在导入模块时立即执行,而被装饰的函数只在明确调用时运行.
导入时和运行时的区别

"""
