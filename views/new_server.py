import sys
from socket import *
from threading import Thread
HOST = '127.0.0.1'
PORT = 9999
ADDR = (HOST, PORT)

class Server():
    def __init__(self):
        #初始化用户列表

        self.list_user = []

        self.create_socket()

        # 创建套接字
    def create_socket(self):
        self.s = socket()
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s.bind(ADDR)
        self.s.listen(3)

        #主程序
    def main(self):
        while True:
            #循环接收套接字
            try:
                c, addr = self.s.accept()
                print('connect from:', addr)
            except KeyboardInterrupt:
                sys.exit('退出游戏')
            except OSError:
                sys.exit('退出游戏')
            except Exception as e:
                print(e)
                continue
            #创建线程处理数据

            t=Thread(target=self.handle,args=[c,])
            t.setDaemon(True)
            t.start()


    def handle(self,c):#接收数据 进行判断处理
        while True:
            data = c.recv(1024)
            # 判断客户端是否断开
            if not data:

                for i in self.list_user:
                    if i == c:
                        self.list_user.remove(i)
                c.close()

            # if....：
            #     注册
            # if...：
            #     登录
            # ......
            #满足条件判断是否进入游戏
            if data.decode() =='ready':
                self.do_entergame(c)
            # 判断人数是否满足开始游戏

    def do_entergame(self,c):
            #判断是否开始游戏
        self.list_user.append(c)
        print(self.list_user)
        c.send(b'longin')
        while len(self.list_user) >= 2:
            self.list_user[0].send(b'Pok')
            del self.list_user[0]
            self.list_user[0].send(b'Pok')
            del self.list_user[0]
            print(self.list_user)


if __name__ == '__main__':

    server=Server()
    server.main()
