import sys
from socket import *
from threading import Thread
from time import sleep
HOST = '127.0.0.1'
PORT = 9999
ADDR = (HOST, PORT)


class Server(Thread):
    def __init__(self, connfd, list_user):
        self.connfd = connfd
        self.list_user = list_user

        super().__init__()

    def run(self):  # 处理请求
        self.do_request(self.connfd, self.list_user)



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


def main():
    # 创建报节字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(3)
    list_user=[]
    # 循环创建线程接入客户
    while True:

        try:
            c, addr = s.accept()
            client_info = (c, addr)
            list_user.append(client_info)
            print(list_user)
            print('connect from:', addr)

        except KeyboardInterrupt:


            sys.exit('退出游戏')
        except OSError:
            sys.exit('退出游戏')
        except Exception as e:
            print(e)
            continue
        t = Server(c, list_user)
        t.setDaemon(True)
        t.start()
        sleep(0.1)
        if len(list_user) >= 2:


            list_user[0][0].send(b'Pok')
            del list_user[0]
            list_user[0][0].send(b'Pok')
            del list_user[0]

            print(list_user)


if __name__ == '__main__':
    main()
