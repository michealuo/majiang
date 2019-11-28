import sys
from socket import *
from threading import Thread
from time import sleep
HOST = '127.0.0.1'
PORT = 9999
ADDR = (HOST, PORT)


class Server(Thread):
    def __init__(self):
        self.c = None
        self.list_user = []
        super().__init__()
        self.create_socket()
    def create_socket(self):
        # 创建报节字
        self.s = socket()
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s.bind(ADDR)
        self.s.listen(3)

    def run(self):  # 处理请求
        self.handle()

    def handle(self):
        pass

    def do_request(self,c,l):  # 收消息
        while True:
            data = c.recv(1024)
            if not data:
                # for i in range(len(l)):
                #     if l[i][0] == c:
                #         del l[i]
                for i in l:
                    if i[0]==c:
                        l.remove(i)
                print(l)
                c.close()
            elif data.decode() =='ready':
                c.send(b'longin')


            #print(data.decode())


if __name__ == '__main__':
    #初始化服务器
    server = Server()
    # 循环创建线程接入客户
    while True:

        try:
            server.c, addr = server.s.accept()
            client_info = (server.c, addr)
            server.list_user.append(client_info)
            print(server.list_user)
            print('connect from:', addr)

        except KeyboardInterrupt:
            sys.exit('退出游戏')
        except OSError:
            sys.exit('退出游戏')
        except Exception as e:
            print(e)
            continue

        server.setDaemon(True)
        server.start()
        sleep(0.1)
        if len(server.list_user) >= 2:


            server.list_user[0][0].send(b'Pok')
            del server.list_user[0]
            server.list_user[0][0].send(b'Pok')
            del server.list_user[0]

            print(server.list_user)