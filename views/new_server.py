import json
import random
import sys
import threading
from socket import *
from threading import Thread

from aptdaemon.lock import acquire

from module.user import user

from sql.handle_sql import Handle_Sql

HOST = '127.0.0.1'
PORT = 8000
ADDR = (HOST, PORT)
wan = ['1万', '2万', '3万', '4万', '5万', '6万', '7万', '8万', '9万']
tiao = ['1条', '2条', '3条', '4条', '5条', '6条', '7条', '8条', '9条']
bing = ['1饼', '2饼', '3饼', '4饼', '5饼', '6饼', '7饼', '8饼', '9饼']

class Server():
    def __init__(self):
        #初始化用户列表
        self.create_socket()
        #准备游戏套接字列表
        self.ready_socket = []
        # 游戏桌子id 和客户端套接字列表{'1':[c1,c2,c3,c4]}
        self.dict_desk = {}
        # 游戏桌子id 和牌库麻将列表{'1':[majiang]}
        self.dict_majiang = {}
        # 游戏桌子id 和东家麻将列表{'1':(手牌[],打出去的牌[],碰牌[],杠牌[])}
        self.dict_majiang_east = {}
        # 游戏桌子id 和南家麻将列表{'1':(手牌[],打出去的牌[],碰牌[],杠牌[])}
        self.dict_majiang_south = {}
        # 游戏桌子id 和西家麻将列表{'1':(手牌[],打出去的牌[],碰牌[],杠牌[])}
        self.dict_majiang_west = {}
        # 游戏桌子id 和北家麻将列表{'1':(手牌[],打出去的牌[],碰牌[],杠牌[])}
        self.dict_majiang_north = {}
        #
        self.dict_sit_majiang = {}
        #锁
        self.lock = threading.RLock()

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
            data = json.loads(c.recv(1024).decode())
            # 判断客户端是否断开
            if not data:
                for k,v in self.dict_desk.items():
                    if c in v:
                        pass
                        #挂机处理
                c.close()
            #注册
            elif data['protocol']=='R':
                self.do_rigister(data,c)

            elif data['protocol']=='L':
                self.do_login(data,c)

            #满足条件判断是否进入游戏,如果可以则开始游戏
            elif data['protocol']=='Ready':
                self.do_entergame(c)

            #玩游戏,代表是客户端打出的牌
            elif data['protocol']=='Play':
                self.do_playgame(data)

    def do_playgame(self,data):
        #如果刚开局,data中只有desk_id信息,则由服务器直接发送数据给各个客户端
        if len(data) == 1:
            desk_id = data['desk_id']
            data_majiang = {'protocol':'Play'}
            data_majiang['desk_id'] = desk_id
            print(self.dict_desk,"--------")
            for i in range(len(self.dict_desk[desk_id])):
                #给麻将排序
                print(self.dict_sit_majiang[str(i)])
                print(type(self.dict_sit_majiang[str(i)]))
                majiang_type, majiang_set = self.sort_majiang(self.dict_sit_majiang[str(i)][desk_id])
                data_majiang['majiang'] = majiang_set
                data_majiang['wan'] = majiang_type[0]
                data_majiang['tiao'] = majiang_type[1]
                data_majiang['bing'] = majiang_type[2]
                #碰
                data_majiang['peng_majiang'] = []
                #杠
                data_majiang['angang_majiang'] = []
                self.dict_desk[desk_id][i].send(json.dumps(data_majiang).encode())
        else:
            pass


    def do_entergame(self,c):
        #判断是否开始游戏
        # 在对dict_desk,ready_socket进行操作时需要保证线程安全
        self.lock.acquire()
        #定义是否可以开始游戏,因为后续过程上锁,让上锁时间尽量减短
        paly_flag = 0
        desk_id = ''
        try:
            self.ready_socket.append(c)
            # 看准备好游戏套接字的个数
            if len(self.ready_socket) < 1:
                # 可以给显示匹配的样式
                pass
            # 开始游戏
            else:
                paly_flag = 1
                #桌子最大id
                maxid = self.find_maxid()
                desk_id = str(maxid + 1)
                self.dict_desk[desk_id] = self.ready_socket
                #客户端进入,准备游戏的客户端清空
                self.ready_socket = []
        finally:
            self.lock.release()
        #开始游戏
        if paly_flag:
            #初始化4家牌,以最后一家准备为东家(该玩家为东家)
            self.init_majiang(desk_id)
            self.do_playgame({'desk_id':desk_id})

    def init_majiang(self,desk_id):
        """
        desk_id:桌号
        初始化一桌麻将
        :return:
        """
        try:
            # 在对majiang进行操作时需要保证线程安全
            self.lock.acquire()
            # 麻将牌
            majiang = []
            for i in range(3):
                for j in range(1, 10):
                    for k in range(4):
                        if i == 0:
                            majiang.append(str(j) + "万")
                        if i == 1:
                            majiang.append(str(j) + "条")
                        if i == 2:
                            majiang.append(str(j) + "饼")

            #初始化手牌 打乱牌库顺序
            random.shuffle(majiang)
            # 初始化4家麻将手牌[[],[],[],[]]
            majiang_split = []
            majiang_split.append(majiang[0:13])
            majiang_split.append(majiang[13:26])
            majiang_split.append(majiang[26:39])
            majiang_split.append(majiang[39:52])
        finally:
            self.lock.release()

        # 游戏桌子id 和东家麻将列表{'1':(手牌[],打出去的牌[],碰牌[],杠牌[])}
        self.dict_majiang_east = {desk_id: majiang[0:14]}
        # 游戏桌子id 和南家麻将列表{'1':(手牌[],打出去的牌[],碰牌[],杠牌[])}
        self.dict_majiang_south = {desk_id: majiang[14:27]}
        # 游戏桌子id 和西家麻将列表{'1':(手牌[],打出去的牌[],碰牌[],杠牌[])}
        self.dict_majiang_west = {desk_id: majiang[27:40]}
        # 游戏桌子id 和北家麻将列表{'1':(手牌[],打出去的牌[],碰牌[],杠牌[])}
        self.dict_majiang_north = {desk_id: majiang[40:53]}
        # 剩余牌库(将牌库给4个玩家后的麻将牌库)
        self.dict_majiang = {desk_id: majiang[53:]}
        #麻将对应位置
        self.dict_sit_majiang['0'] = self.dict_majiang_east
        self.dict_sit_majiang['1'] = self.dict_majiang_south
        self.dict_sit_majiang['2'] = self.dict_majiang_west
        self.dict_sit_majiang['3'] = self.dict_majiang_north

    def do_rigister(self, data,c):
        #注册时判断用户名是否已经存在
        if Handle_Sql().check(user(data['username'])):
            c.send(json.dumps({'protocol':'Rno'}).encode())
        else:
            user_ = user(data['username'],data['password'],data['phone'],data['ip'])
            Handle_Sql().insert_one(user_)
            c.send(json.dumps({'protocol':'Ryes'}).encode())

    def do_login(self, data,c):
        user_ = user(data['username'],data['password'])
        #去数据库校验用户名密码
        if Handle_Sql().check(user_):
            c.send(json.dumps({'protocol':'Lyes'}).encode())
        else:
            c.send(json.dumps({'protocol':'Lno'}).encode())

    def find_maxid(self):
        """

        :return: 返回最大桌号码,如果是第一桌就是0
        """
        if not self.dict_desk:
            return 0
        return max([int(i) for i in list(self.dict_desk.keys())])

    # 整理牌面
    def sort_majiang(self,majiang):
        """

        :param majiang: 传入一个麻将列表
        :return:返回一个按照万筒条顺序返回的大列表[[],[],[]]
        和一个排序好的麻将列表[]
        """
        def each_sort(each_type):
            """

            :param each_type: 1~9的花色列表
            :return:根据花色排序
            """
            result = []

            for each_majiang in majiang:
                if each_majiang in each_type:
                    # 将具体花色对应的牌存储进结果
                    result.append(each_majiang)
            return result

        # 对各种类型的牌面进行排序(需要返回值用sorted)
        global wan
        global tiao
        global bing
        wan = sorted(each_sort(wan))
        tiao = sorted(each_sort(tiao))
        bing = sorted(each_sort(bing))
        # 按照花色排序
        majiang_type = [wan, tiao, bing]
        majiang_set = []
        majiang_set.extend(wan)
        majiang_set.extend(tiao)
        majiang_set.extend(bing)
        return majiang_type,majiang_set

if __name__ == '__main__':

    server=Server()
    server.main()
