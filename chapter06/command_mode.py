# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/4 13:43
# @Author   : tangky
# @Site     : 
# @File     : command_mode.py
# @Software : PyCharm

"""
6.2 "命令"模式
命令设计模式也可以通过把函数作为参数传递而简化
"命令"模式的目的是解耦调用操作的对象(调用者)和提供实现的对象(接收者)
如:调用者是图形应用程序中的菜单项,而接收者是被编辑的文档或应用程序本身
这个模式的做法是,在二者之间放一个Command对象,让它实现只有一个方法(execute)的接口,
调用接收者中的方法执行所需的操作.这样,调用者无需了解接收者的接口,而且不同的接收者可以适应不同的Command子类.
调用者有一个具体的命令,通过调用execute方法执行.
命令模式是回调机制的面向对象替代品
我们可以不为调用者提供一个Command实例,而是给它一个函数.此时,调用者不用调用command.execute(),直接调用command()即可.
MacroCommand可以实现成定义了__call__方法的类.
这样,MacroCommand的实例就是可调用对象,各自维护着一个函数列表,供以后调用
"""


# 示例6-9 MacroCommand的各个实例都在内部存储着命令列表
class MacroCommand:
    """一个执行一组命令的命令"""

    def __init__(self, commands):
        self.commands = list(commands)

    def __call__(self):
        for command in self.commands:
            command()
# 复杂的"命令"模式(如支持撤销操作)可能需要更多,而不仅是简单的回调函数
# 像实例6-9中的MacroCommand那样的可调用实例,可以保存任何所需的状态,而且除了__call__之外还可以提供其他方法
# 可以使用闭包在调用之间保存函数的内部状态
