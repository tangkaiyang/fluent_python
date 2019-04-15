# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/15 8:13
# @Author   : tangky
# @Site     : 
# @File     : spinner_asyncio.py
# @Software : PyCharm


# 示例18-2 spinner_asyncio.py: 通过协程以动画形式显示文本式旋转指针

import asyncio
import itertools
import sys


@asyncio.coroutine
def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            yield from asyncio.sleep(.1)  # 这样的休眠不会阻塞时间循环
        except asyncio.CancelledError:  # 抛出该异常是因为发出了取消请求,因此退出循环
            break
    write(' ' * len(status) + '\x08' * len(status))


@asyncio.coroutine
def slow_function():  # slow_function函数是协程,在用休眠假装进行I/O操作时,使用yield from继续执行时间循环
    # 假装等待I/O一段时间
    yield from asyncio.sleep(3)  # yield from asyncio.sleep(3)表达式把控制权交给主循环,在休眠结束后恢复这个协程
    return 42


@asyncio.coroutine
def supervisor():
    spinner = asyncio.ensure_future(spin('thinking!'))  # asyncio.async(...)函数排定spin协程的运行时间,使用一个Task对象包装spin协程,并立即返回
    print('spinner object:', spinner)
    result = yield from slow_function()
    spinner.cancel()  # Task对象可以取消:取消后会在协程当前暂停的yield处抛出asyncio.CancelledError异常.协程可以捕获这个异常,也可以延迟取消,甚至拒绝取消
    return result


def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(supervisor())
    loop.close()
    print('Answer:', result)


if __name__ == '__main__':
    main()
