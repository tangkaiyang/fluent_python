# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/15 11:37
# @Author   : tangky
# @Site     : 
# @File     : flags_asyncio.py
# @Software : PyCharm


# 示例18-5 flags_asyncio.py:使用asyncio和aiohttp包实现的异步下载脚本
import asyncio
import aiohttp
from flags import BASE_URL, save_flag, show, main


@asyncio.coroutine
def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = yield from aiohttp.request('GET', url) # 阻塞的操作通过协程实现,客户代码通过yield from把职责委托给协程,以便异步运行协程
    image = yield from resp.read() # 读取响应的内容是一项单独的异步操作
    return image


@asyncio.coroutine
def download_one(cc): # 用到了yield from所以必须是协程
    image = yield from get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    loop = asyncio.get_event_loop() # 获取时间循环底层实现的引用
    to_do = [download_one(cc) for cc in sorted(cc_list)]
    wait_coro = asyncio.wait(to_do) # wait不是阻塞型函数.wait是一个协程,等传给它的所有协程运行完毕后结束(默认行为)
    res, _ = loop.run_until_complete(wait_coro) # 执行事件循环,直到wait_coro运行结束;事件循环运行的过程中,这个脚本会在这里阻塞.
    loop.close()

    return len(res)


if __name__ == '__main__':
    main(download_many)
