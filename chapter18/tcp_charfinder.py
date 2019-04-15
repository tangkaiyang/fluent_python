# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/15 16:21
# @Author   : tangky
# @Site     : 
# @File     : tcp_charfinder.py
# @Software : PyCharm

# 示例18-14 tcp_charfinder.py:使用asyncio.start_server函数实现的简易TCP服务器;
import sys
import asyncio

from charfinder import UnicodeNameIndex

CRLF = b'\r\n'
PROMPT = b'?>'

index = UnicodeNameIndex()


@asyncio.coroutine
def handle_queries(reader,
                   writer):  # 3.这个协程要传给asyncio.start_server函数,接收的两个参数是asyncio.StreamReader对象和asyncio.StreamWriter对象
    while True:  # 4. 这个循环处理会话,直到从客户端收到控制字符后退出
        writer.write(PROMPT)  # 5.StreamWriter.write方法不是协程只是普通的函数;这一行代码发送?>提示符
        yield from writer.drain()  # 6.StreamWriter.drain方法刷新writer缓冲;因为它是协程,所以必须使用yield from调用
        data = yield from reader.readline()  # 7.StreamReader.readline方法是协程,返回一个bytes对象
        try:
            query = data.decode().strip()
        except UnicodeDecodeError:  # 8.Telnet客户端发送控制字符时,可能会抛出UnicodeDecodeError异常:遇到这种情况,发送空字符
            query = '\x00'
        client = writer.get_extra_info('peername')  # 9.返回与套接字连接的远程地址
        print('Received from {}: {!r}'.format(client, query))  # 10.在服务器的控制台中记录查询
        if query:
            if ord(query[:1]) < 32:  # 11.如果收到控制字符或空字符,退出循环
                break
            lines = list(index.find_description_strs(query))  # 12.返回一个生成器,并从中构建一个列表
            if lines:
                writer.writelines(line.encode() + CRLF for line in
                                  lines)  # 13.使用默认的UTF-8编码把lines转换成bytes对象,并在每一行末尾添加回车符和换行符;注意,参数是一个生成器表达式
            writer.write(index.status(query, len(lines)).encode() + CRLF)  # 14.输出状态

            yield from writer.drain()  # 15.刷新输出缓冲
            print('Sent {} results'.format(len(lines)))  # 16.在服务器的控制台记录响应

    print('Close the client socket')  # 17.再服务器的控制台中记录会话结束
    writer.close()  # 18.关闭StreamWriter流


# handle_queries协程的名称是复数,因为它启动交互式会话后能处理各个客户端发来的多次请求
# 注意,示例18-14中所有的I/O操作都使用bytes格式.因此,我们要解码从网络中收到的字符串,还要编码发出的字符串.
# Python3默认使用的编码是UTF-8,这里就隐式使用了这个编码
# 有些I/O方法是协程,必须由yield from驱动,而另一些则是普通的函数.
# 示例18-15 tcp_charfinder.py:main函数创建并销毁事件循环和套接字服务器
def main(address='127.0.0.1', port=2323):  # 1.调用main函数时可以不传入参数
    port = int(port)
    loop = asyncio.get_event_loop()
    server_coro = asyncio.start_server(handle_queries, address, port,
                                       loop=loop)  # 2.asyncio.start_server协程运行结束后,返回的协程对象返回一个asyncio.Server实例,即一个TCP套接字服务器
    server = loop.run_until_complete(server_coro)  # 3.驱动server_coro协程,启动服务器(server)
    host = server.sockets[0].getsockname()  # 4.获取这个服务器的第一个套接字的地址和端口,然后..
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))  # 5...在服务器的控制台中显示出来.
    try:
        loop.run_forever()  # 6.运行事件循环;main函数在这里阻塞,直到在服务器的控制台中按CTRL-C键才会关闭
    except KeyboardInterrupt:  # 按CTRL-C键
        pass
    print('Server shutting down.')
    server.close()  # 7.关闭服务器
    loop.run_until_complete(server.wait_closed())  # 8.server.wait_closed()方法返回一个期物;调用loop.run_until_complete方法,运行期物
    loop.close()  # 9.终止事件循环


if __name__ == '__main__':
    main(*sys.argv[1:])  # 10.这是处理可选的命令行参数的简便方式

# 注意,run_until_complete方法的参数是一个协程(start_server方法返回的结果)或一个Future对象(server.wait_closed放回的结果).
# 如果传给run_until_complete方法的参数是协程,会把协程包装在Task对象中
"""
注意,main函数几乎会立即显示Serving on...消息,然后在调用loop.run_forever()方法时阻塞.
在那一点,控制权流动到事件循环中,而且一直待在哪里,不过偶尔会回到handle_queries协程,这个
协程需要等待网络发送或接受数据时,控制权又交还事件循环.在事件循环运行期间,只要有新客户端连接服务器就会启动一个handle_queries
协程实例.因此,这个简单的服务器可以并发处理多个客户端.出现KeyboardInterrupt异常,或者操作系统把进程杀死,服务器会关闭
"""
