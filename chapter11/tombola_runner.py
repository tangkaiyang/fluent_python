# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/10 14:34
# @Author   : tangky
# @Site     : 
# @File     : tombola_runner.py
# @Software : PyCharm

import doctest

from tombola import Tombola

# 要测试的模块
import bingo, lotto, tombolist

TEST_FILE = 'tombola_tests'
TEST_MSG = '{0:16} {1.attempted:2} tests, {1.failed:2} failed - {2}'


def main(argv):
    verbose = '-v' in argv
    real_subclasses = Tombola.__subclasses__()
    virtual_subclasses = list(Tombola._abc_registry)

    for cls in real_subclasses + virtual_subclasses:
        test(cls, verbose)


def test(cls, verbose=False):
    res = doctest.testfile(
        TEST_FILE,
        globs={'ConcreteTombola': cls},
        verbose=verbose,
        optionflags=doctest.REPORT_ONLY_FIRST_FAILURE
    )
    tag = 'FAIL' if res.failed else 'OK'
    print(TEST_MSG.format(cls.__name__, res, tag))


if __name__ == '__main__':
    import sys

    main(sys.argv)
