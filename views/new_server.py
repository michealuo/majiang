import sys
from socket import *
from threading import Thread
from module.user import user

from sql.handle_sql import Handle_Sql

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
            data = c.recv(1024).decode().split(' ')
            # 判断客户端是否断开
            if not data:

                for i in self.list_user:
                    if i == c:
                        self.list_user.remove(i)
                        print(self.list_user)
                c.close()
            elif data[0]=='R':
                self.do_rigister(data[1], data[4], data[3], data[2],c)


            elif data[0]=='L':
                self.do_login(data[1], data[2],c)

            #满足条件判断是否进入游戏
            elif data[0]=='E':
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

    def do_rigister(self, name, passwd, phone, ip,c):
        if Handle_Sql().check(user(name)):
            c.send(b"rno")
        else:
            user_ = user(name, passwd, phone, ip)
            Handle_Sql().insert_one(user_)

            c.send(b'ryes')

    def do_login(self, name, passwd,c):
        user_ = user(name,passwd)
        if not Handle_Sql().check(user_):
            c.send(b'no')
        else:
            c.send(b'yes')

if __name__ == '__main__':

    server=Server()
    server.main()
