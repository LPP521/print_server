# coding=gbk
"""
@File    :   main.py    
@Contact :   13132515202@163.com

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2019/12/12 22:39   LiuHe      1.0         None
"""
import os
import time
import socket
import win32api
import win32print


def server():
    IP_PORT = ('0.0.0.0', 9999)

    # 创建socket实例
    sk = socket.socket()
    sk.bind(IP_PORT)

    sk.listen(0)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    print("服务端开启，正在监听")

    while True:
        conn, addr = sk.accept()

        print("{0}, {1} 已连接".format(addr[0], addr[1]))

        data = conn.recv(1024)
        data_str = str(data, 'utf-8')
        cmd, file_name, file_size = data_str.split("|")
        path = os.path.join(BASE_DIR, file_name)
        file_size = int(file_size)
        has_sent = 0
        with open(path, 'wb') as fp:
            while has_sent != file_size:
                data = conn.recv(1024)
                fp.write(data)
                has_sent += len(data)
                print('\r'+'[保存进度]:%s%.2f%%'%('>'*int((has_sent/file_size)*50),
                                                  float(has_sent/file_size)*100), end='')

        print()

        print("%s保存成功" % file_name)
        try:
            win32api.ShellExecute(
                0,
                "print",
                file_name,
                '/d:"%s"' % win32print.GetDefaultPrinter(),
                ".",
                0
            )
        except Exception as e:
            print(e)


if __name__== '__main__':
    server()