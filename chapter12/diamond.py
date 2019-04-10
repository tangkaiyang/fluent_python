# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/10 16:27
# @Author   : tangky
# @Site     : 
# @File     : diamond.py
# @Software : PyCharm

class A:
    def ping(self):
        print('ping:', self)


class B(A):
    def pong(self):
        print('pong:', self)


class C(A):
    def pong(self):
        print('PONG:', self)


class D(B, C):
    def ping(self):
        # super().ping()
        A.ping(self)
        print('post-ping:', self)

    def pingpong(self):
        self.ping()
        super(D, self).ping()
        self.pong()
        super(D, self).pong()
        C.pong(self)


if __name__ == '__main__':
    print(D.__mro__)
