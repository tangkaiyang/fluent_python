# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/9 14:44
# @Author   : tangky
# @Site     : 
# @File     : vector_v1.py
# @Software : PyCharm

from array import array
import math
import reprlib


class Vector2d:
    typecode = 'd'

    def __init__(self, components):  # components组件
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(self._components))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.sqrt(sum(x*x for x in self))

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)