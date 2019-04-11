# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 13:08
# @Author   : tangky
# @Site     : 
# @File     : gen_test.py
# @Software : PyCharm


# def gen_123():  # 只要Python函数中包含关键字yield,该函数就是生成器函数
#     yield 1  # 生成器函数的定义体中通常都有循环,不过这不是必要条件;
#     yield 2
#     yield 3
#
#
# print(gen_123)  # 函数对象
# print(gen_123())  # 返回一个生成器对象
# for i in gen_123():  # 生成器是迭代器,会生成传给yield关键字的表达式的值
#     print(i)
#
# g = gen_123()
# print(next(g))  # g是迭代器,所以调用next(g)会获取yield生成的下一个元素
# print(next(g))
# print(next(g))
# # print(next(g))

# 示例14-6 运行时打印消息的生成器函数
# def gen_AB():
#     print('start')
#     yield 'A'
#     print('continue')
#     yield 'B'
#     print('end.')
#
#
# for c in gen_AB():  # 迭代时,for机制的作用与g=iter(gen_AB())一样,用于获取生成器对象,然后每次迭代时调用next(g)
#     print('-->', c)
# # for机制会捕获异常,因此循环终止时没有报错

# 示例14-8 先在列表推导式中使用gen_AB生成器函数,然后在生成器表达式中使用
def gen_AB():
    print('start')
    yield 'A'
    print('continue')
    yield 'B'
    print('end.')

# res1 = [x*3 for x in gen_AB()]
# print(res1)
# for i in res1: # 这个for循环迭代列表推导式生成的res1雷柏啊
#     print('-->', i)
#
res2 = (x*3 for x in gen_AB()) # 生成器对象
print(res2)
# res3 = [x for x in res2]
# print(res3)
for i in res2: # 只有for循环迭代res2时,gen_AB函数的定义体才会真正执行.for循环每次迭代会隐式调用next(res2),前进到gen_AB函数中的下一个yield语句.注意,gen_AB函数的输出与for循环中print函数的输出夹杂在一起
    print('-->', i)
