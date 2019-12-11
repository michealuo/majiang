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
        # 游戏座位和麻将{'id_0':东家麻将}
        self.dict_sit_majiang = {}
        #锁
        self.lock = threading.RLock()
        # 存储客户端的套接字和名称字典name:c
        self.dict_client_user = {}
        self.wan = ['1万', '2万', '3万', '4万', '5万', '6万', '7万', '8万', '9万']
        self.tiao = ['1条', '2条', '3条', '4条', '5条', '6条', '7条', '8条', '9条']
        self.bing = ['1饼', '2饼', '3饼', '4饼', '5饼', '6饼', '7饼', '8饼', '9饼']

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

            #玩游戏
            elif data['protocol']=='Play':
                self.do_playgame(data,c)

    def do_playgame(self,data,c):
        #如果刚开局,data中只有desk_id信息,则由服务器直接发送数据给各个客户端
        if len(data) == 1:
            self.init_game(data)
        #刚初始话完毕牌库,得到东家打出第一张牌
        elif data['operation'] == 'put_majiang':
            #获取桌号,开始打牌
            desk_id = data['desk_id']
            data_majiang = {'protocol': 'Play'}
            data_majiang['desk_id'] = desk_id
            #如果获取到有麻将打出则提示其他玩家看牌
            if data['put_majiang']:
                #检验其他玩家是否能赢 杠 碰,不能则轮到下家
                lis_c = self.dict_desk[desk_id]
                for i in range(len(lis_c)):
                    if c != lis_c[i]:
                        # 给麻将排序,得到万,条,饼
                        majiang_type, majiang_set = self.sort_majiang(
                            self.dict_sit_majiang[desk_id + '_' + str(i)][0])
                        #加入得到的麻将验胡
                        if data['put_majiang'] in self.wan:
                            majiang_type[0].append(data['put_majiang'])
                        elif data['put_majiang'] in self.tiao:
                            majiang_type[1].append(data['put_majiang'])
                        elif data['put_majiang'] in self.bing:
                            majiang_type[2].append(data['put_majiang'])
                        #验胡牌
                        if self.check_win(majiang_type[0],majiang_type[1],majiang_type[2]):
                            data_majiang['operation'] = 'win'
                            #告诉每个玩家,该名玩家胡牌
                            for client in lis_c:
                                data_majiang['winner'] = self.getUserNameBySocket(i)
                                data_majiang['majiang_type'] = majiang_type
                                data_majiang['peng_majiang'] = self.dict_sit_majiang[desk_id + '_' + str(i)][desk_id][2]
                                data_majiang['angang_majiang'] = self.dict_sit_majiang[desk_id + '_' + str(i)][desk_id][3]
                                client.send(json.dumps(data_majiang).encode())

                #改变下家turns(代表是否该他接牌)给他一张牌
                print("==+==",data['put_majiang'])
        #游戏结束
        elif data['operation'] == 'over':
            desk_id = data['desk_id']
            self.release_resource(desk_id)

            
    def init_game(self,data):
        desk_id = data['desk_id']
        data_majiang = {'protocol': 'Play'}
        data_majiang['desk_id'] = desk_id
        for i in range(len(self.dict_desk[desk_id])):
            # 给麻将排序
            majiang_type, majiang_set = self.sort_majiang(self.dict_sit_majiang[desk_id+'_'+str(i)][0])
            # 是否该这个玩家出牌
            if len(majiang_set) == 14:
                data_majiang['turns'] = 1
            else:
                data_majiang['turns'] = 0
            data_majiang['majiang'] = majiang_set
            data_majiang['wan'] = majiang_type[0]
            data_majiang['tiao'] = majiang_type[1]
            data_majiang['bing'] = majiang_type[2]
            # 碰
            data_majiang['peng_majiang'] = []
            # 杠
            data_majiang['angang_majiang'] = []
            self.dict_desk[desk_id][i].send(json.dumps(data_majiang).encode())

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
            self.do_playgame({'desk_id':desk_id},c)

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
        self.dict_majiang_east = {desk_id: [majiang[0:14],[],[],[]]}
        # 游戏桌子id 和南家麻将列表{'1':(手牌[],打出去的牌[],碰牌[],杠牌[])}
        self.dict_majiang_south = {desk_id: [majiang[14:27],[],[],[]]}
        # 游戏桌子id 和西家麻将列表{'1':(手牌[],打出去的牌[],碰牌[],杠牌[])}
        self.dict_majiang_west = {desk_id: [majiang[27:40],[],[],[]]}
        # 游戏桌子id 和北家麻将列表{'1':(手牌[],打出去的牌[],碰牌[],杠牌[])}
        self.dict_majiang_north = {desk_id: [majiang[40:53],[],[],[]]}
        # 剩余牌库(将牌库给4个玩家后的麻将牌库)
        self.dict_majiang = {desk_id: majiang[53:]}
        #麻将对应位置
        self.dict_sit_majiang[desk_id + '_0'] = self.dict_majiang_east[desk_id]
        self.dict_sit_majiang[desk_id + '_1'] = self.dict_majiang_south[desk_id]
        self.dict_sit_majiang[desk_id + '_2'] = self.dict_majiang_west[desk_id]
        self.dict_sit_majiang[desk_id + '_3'] = self.dict_majiang_north[desk_id]


    def do_rigister(self, data,c):
        #注册时判断用户名是否已经存在
        if Handle_Sql().check(user(data['username'])):
            c.send(json.dumps({'protocol':'Rno','msg':'已经存在的账户'}).encode())
        else:
            user_ = user(data['username'],data['password'],data['phone'],data['ip'])
            Handle_Sql().insert_one(user_)
            c.send(json.dumps({'protocol':'Ryes'}).encode())

    def do_login(self, data,c):
        user_ = user(data['username'],data['password'])
        #去数据库校验用户名密码
        if Handle_Sql().check(user_):
            self.dict_client_user[data['username']] = c
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

        my_wan = sorted(each_sort(self.wan))
        my_tiao = sorted(each_sort(self.tiao))
        my_bing = sorted(each_sort(self.bing))
        # 按照花色排序
        majiang_type = [my_wan, my_tiao, my_bing]
        majiang_set = []
        majiang_set.extend(my_wan)
        majiang_set.extend(my_tiao)
        majiang_set.extend(my_bing)
        return majiang_type,majiang_set

    def getUserNameBySocket(self,c):
        for k,v in self.dict_client_user:
            if v == c:
                return k

    #验胡牌
    def check_win(self,wan, tiao, bing):
        common_type = [wan, tiao, bing]
        str_commontype = ['万', '条', '饼']
        majiang_else = {'万': [], '条': [], '饼': []}  # 记录多余待打麻将
        winflag = {'万': [], '条': [], '饼': []}  # 记录各个花色是否可赢
        cupple = {'万': [], '条': [], '饼': []}  # 记录单出来的对子

        # 验万条饼
        def check_each_type(type_list, str_typelist):
            digit_list = []  # 便于计算的牌面纯数字序列
            result_else = []  # 存储该花色待打牌
            result_else.clear()
            for each in type_list:
                digit_list.append(int(each[0]))
            digit_list_copy = digit_list.copy()

            # 检测顺子函数
            def check_ABC():
                nonlocal digit_list_copy
                for j in range(3):
                    for i in range(1, 8):
                        if i in digit_list_copy and i + 1 \
                                in digit_list_copy and i + 2 in digit_list_copy:
                            digit_list_copy.remove(i)
                            digit_list_copy.remove(i + 1)
                            digit_list_copy.remove(i + 2)

            # 检测三个一样的
            def check_AAA():
                nonlocal digit_list_copy
                for j in range(3):
                    for i in range(1, 10):
                        if digit_list_copy.count(i) == 3:
                            digit_list_copy = [each for each in \
                                               digit_list_copy if each != i]

            # 检测两个一样的
            def check_AA(str_type):
                nonlocal digit_list_copy
                for i in range(1, 10):
                    if digit_list_copy.count(i) == 2:
                        cupple[str_type].append(i)
                        digit_list_copy = [each for each in \
                                           digit_list_copy if each != i]

            check_ABC()
            check_AAA()
            check_AA(str_typelist)
            if digit_list_copy == []:
                winflag[str_typelist] = 1
            else:
                result_else.append(digit_list_copy)
                digit_list_copy = digit_list.copy()
                cupple[str_typelist].clear()
                check_AAA()
                check_ABC()
                check_AA(str_typelist)
                if digit_list_copy == []:
                    winflag[str_typelist] = 1
                else:
                    result_else.append(digit_list_copy)
                    digit_list_copy = digit_list.copy()
                    cupple[str_typelist].clear()
                    check_ABC()
                    check_AA(str_typelist)
                    check_AAA()
                    if digit_list_copy == []:
                        winflag[str_typelist] = 1
                    else:
                        result_else.append(digit_list_copy)
            try:
                result_min = min(len(each) for each in result_else)
                result_else_f = [each for each in result_else \
                                 if (len(each)) == result_min]
                cupple_num = result_else.index(result_else_f[0])
                if cupple_num == 0:
                    check_AAA()
                    check_AA(str_typelist)
                    check_ABC()
                elif cupple_num == 1:
                    check_AAA()
                    check_ABC()
                    check_AA(str_typelist)
            except ValueError:
                result_else_f = [[]]
            finally:
                majiang_else[str_typelist].extend(result_else_f[0])

        # 整体验胡
        for i in range(3):
            check_each_type(common_type[i],
                            str_commontype[i])
        if list(winflag.values()) == [1, 1, 1] and \
                sum([len(cupple[each]) for each in cupple]) == 1:
            return 1
        return 0
    def release_resource(self,desk_id):
        # 游戏桌子id 和客户端套接字列表{'1':[c1,c2,c3,c4]}
        del self.dict_desk[desk_id]
        # 游戏桌子id 和牌库麻将列表{'1':[majiang]}
        del self.dict_majiang[desk_id]
        # 游戏桌子id 和东家麻将列表{'1':(手牌[],打出去的牌[],碰牌[],杠牌[])}
        del self.dict_majiang_east[desk_id]
        # 游戏桌子id 和南家麻将列表{'1':(手牌[],打出去的牌[],碰牌[],杠牌[])}
        del self.dict_majiang_south[desk_id]
        # 游戏桌子id 和西家麻将列表{'1':(手牌[],打出去的牌[],碰牌[],杠牌[])}
        del self.dict_majiang_west[desk_id]
        # 游戏桌子id 和北家麻将列表{'1':(手牌[],打出去的牌[],碰牌[],杠牌[])}
        del self.dict_majiang_north[desk_id]
        # 游戏座位和麻将{'id_0':东家麻将}
        for i in range(4):
            del self.dict_sit_majiang[desk_id + "_" + str(i)]


if __name__ == '__main__':

    server=Server()
    server.main()


