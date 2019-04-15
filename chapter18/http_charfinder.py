# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/15 19:45
# @Author   : tangky
# @Site     : 
# @File     : http_charfinder.py
# @Software : PyCharm
import asyncio
import aiohttp
from aiohttp import web
import sys


# 后半部分:启动和关闭事件循环与HTTP服务器
# 示例18-17 http_charfinder.py: main和init函数
@asyncio.coroutine
def init(loop, address, port):  # 1.init协程产出一个服务器,交给事件循环驱动
    app = web.Application(loop=loop)  # 2.aiohttp.web.Application类表示Web应用...
    app.router.add_route('GET', '/', home)  # 3....通过路由把URL模式映射到处理函数上;这里,把GET /路由映射到home函数上
    handler = app.make_handler()  # 4.app.make_handler方法返回一个aiohttp.web.RequestHandler实例,根据app对象设置的路由处理HTTP请求
    server = yield from loop.create_server(handler,
                                           address,
                                           port)  # 5.create_server方法创建服务器,以handler为协议处理程序,并把服务器绑定在指定的地址(address)和端口(port)上
    return server.socket[0].getsockname()  # 6.返回第一个服务器套接字的地址和端口


def main(address='127.0.0.1', port=8888):
    port = int(port)
    loop = asyncio.get_event_loop()
    host = loop.run_until_complete(init(loop, address, port))  # 7.运行init函数,启动服务器,获取服务器的地址和端口
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))
    try:
        loop.run_forever()  # 8.运行事件循环;控制权在事件循环手上时,main函数会在这里阻塞
    except KeyboardInterrupt:
        pass
    print('Server shutting down.')
    loop.close()  # 9.关闭事件循环

# 示例18-18 home函数.根据这个HTTP服务器配置,home函数用于处理/(跟)URL
def home(request): # 1.一个路由处理函数,参数是一个aiohttp.web.Request实例
    query = request.GET.get('query', '').strip() # 2.获取查询字符串,去掉首尾的空白
    print('Query: {!r}'.format(query)) # 3.在服务器的控制台中记录查询
    if query: # 4.如果有查询字符串,从索引(index)中找到结果,使用HTML表格中的行渲染结果,把结果赋值给res变量,再把状态消息赋值给msg变量
        descriptions = list(index.find_descriptions(query))
        res = '\n'.join(ROW_TPL.format(**vars(descr))
                        for descr in descriptions)
        msg = index.status(query, len(descriptions))
    else:
        descriptions = []
        res = ''
        msg = 'Enter words describing characters.'
    html = template.format(query=query, result=res, # 5.渲染HTML页面
                           message=msg)
    print('Sending {} results'.format(len(descriptions)))# 6.在服务器的控制台中记录响应
    return web.Rsponse(content_type=CONTENT_TYPE, text=html)# 7.构建Response对象,将其返回

if __name__ == '__main__':
    main(*sys.argv[1:])
