# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/15 7:55
# @Author   : tangky
# @Site     : 
# @File     : spinner_thread.py
# @Software : PyCharm


# 示例18-1 spinner_thread.py:通过线程以动画形式显示文本式旋转指针
import threading
import itertools
import time
import sys


class Signal:
    go = True


def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'): # 无限循环,itertools.cycle函数会从指定的序列中反复不断地生成元素
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status)) # 显示文本动画的诀窍:使用退格符(\x08)把光标移回来
        time.sleep(.1)
        if not signal.go:
            break
    write(' ' * len(status) + '\x08' * len(status)) # 使用空格清除状态消息,把光标移回开头


def slow_function():
    # 假装等待I/O一段时间
    time.sleep(3) # 调用sleep函数会阻塞主线程,这么做,以便释放GIL,创建从属线程
    return 42


def supervisor(): # 这个函数设置从属线程,显示线程对象,运行耗时的计算,最后杀死线程
    signal = Signal()
    spinner = threading.Thread(target=spin,
                               args=('thinking!', signal))
    print('spinner object:', spinner)
    spinner.start()
    result = slow_function() # 运行slow_function函数,阻塞主线程.同时,从属线程以动画方式显示旋转指针
    signal.go = False
    spinner.join()
    return result


def main():
    result = supervisor()
    print('Answer:', result)


if __name__ == '__main__':
    main()
