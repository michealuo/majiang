import json

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import easygui as g
import sys
# from winproblem import *
class EnterGame(QDialog):

    def __init__(self,s,name):
        self.s=s
        self.name=name
        super().__init__()
        self.initUI()

        # self.closeEvent(event=Event(s))

    def initUI(self):
        self.setWindowTitle("血流成河")
        # self.setWindowIcon(QIcon('hongzhong.jpg'))
        self.resize(640, 480)
        # 设置对象名称
        self.setObjectName("MainWindow")
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # #todo 1 设置窗口背景图片
        self.setStyleSheet("#MainWindow{border-image:url(../img/timg.jpeg);}")

        self.frame = QFrame(self)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.frame.move(200, 200)
        #添加标签
        self.label=QLabel("欢迎%s加入游戏大厅"%(self.name),self)
        self.label.setGeometry(270, 10, 150, 80)
        #设置字体大小
        self.label.setFont(QFont("Microsoft YaHei",10,QFont.Bold))
        #设置标签字体颜色
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.blue)
        self.label.setPalette(pe)
        #设置进入游戏按钮
        self.button_login = QPushButton("进入游戏", self)
        self.button_login.setGeometry(270, 350, 100, 40)
        # 绑定按钮点击函数
        self.button_login.clicked.connect(self.on_click)


        #居中设置
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.s.close()
            sys.exit(0)
        else:
            event.ignore()

    @pyqtSlot()
    def on_click(self):
        # 点击进入游戏,开始游戏,发送准备
        json_info = {'protocol': 'Ready'}

        self.s.send(json.dumps(json_info).encode())
        # 返回校验值
        data = json.loads(self.s.recv(1024).decode())
        #返回play 代表游戏已经开始
        if data['protocol'] == 'Play':
            self.init_game(data)
        elif data['protocol'] == 'Outtime':
            QMessageBox.question(self, "Message", '连接超时',
                                 QMessageBox.Ok, QMessageBox.Ok)

    def init_game(self,first_data):
        json_info = {}
        #协议
        json_info['protocol'] ='Play'
        #打出的麻将
        json_info['put_majiang'] = ''
        #是否是该玩家出的牌
        json_info['turns'] = 0
        #操作信息
        json_info['operation'] = 'init_over'
        #初始化天湖开局
        if first_data['operation'] == 'win':
            g.msgbox('玩家%s胡了！\n%s' % (first_data['user'], str(first_data['majiang_type']) + \
                                      3 * str(first_data['peng_majiang']) + 4 * str(first_data['angang_majiang'])))
            json_info['operation'] = 'over'
            self.s.send(json.dumps(json_info).encode())
        elif first_data['operation'] == 'angang':
            yngang = g.ynbox('是否杠%s？' % first_data['angang'])
            json_info['operation'] = 'angang'
            # 返回是否杠
            if yngang:
                json_info['angang'] = yngang
                self.s.send(json.dumps(json_info).encode())
            #不杠就打牌
            else:
                self.put_majiang(first_data,json_info)

        elif first_data['turns']:

            #东家初始化直接打牌
            self.put_majiang(first_data,json_info)

        else:
            #其他玩家看牌
            g.msgbox('您的麻将是:\n%s\n%s\n%s\n碰：%s\n杠：%s\n' % \
                (str(first_data['wan']), str(first_data['tiao']), str(first_data['bing']),
                 str(first_data['peng_majiang']), str(first_data['angang_majiang'])), '打麻将',
                )
            json_info['put_majiang'] = ''
            self.s.send(json.dumps(json_info).encode())

        self.playgame()

    def playgame(self):
        json_info = {}
        json_info['protocol'] = 'Play'

        while True:
            print('=====000====')
            data = json.loads(self.s.recv(1024).decode())
            print('=====111====',data)
            json_info['desk_id'] = data['desk_id']
            #判断操作
            if data['operation'] == 'win':
                g.msgbox('玩家%s胡了！\n%s' % (data['user'], str(data['majiang_type']) + \
                                          3 * str(data['peng_majiang']) + 4 * str(data['angang_majiang'])))
                json_info['operation'] = 'over'
            elif data['operation'] == 'angang':
                if data['turns']:
                    yngang = g.ynbox('是否杠%s？' % data['angang'])
                    json_info['operation'] = 'angang'
                    #返回是否杠
                    json_info['angang'] = yngang
                else:
                    g.msgbox('玩家%s杠了！\n%s' % (data['username'],data['angang_majiang']))
            elif data['operation'] == 'put_majiang':
                g.msgbox('您获得了%s' % data['get_majiang'])
                print('2222')
                self.put_majiang(data,json_info)


            self.s.send(json.dumps(json_info).encode())
    def put_majiang(self,data,json_info):
        putresult = g.choicebox(
            '您的麻将是:\n%s\n%s\n%s\n碰：%s\n杠：%s\n请选择要打的麻将' % \
            (str(data['wan']), str(data['tiao']), str(data['bing']),
             str(data['peng_majiang']), str(data['angang_majiang'])), '打麻将',
            data['majiang'])
        # 打出的麻将
        print(putresult,'打出的麻将是')
        json_info['put_majiang'] = putresult
        # 东家回消息打出麻将
        json_info['operation'] = 'put_majiang'
        # 是否是该玩家出的牌
        json_info['turns'] = 1
        json_info['desk_id'] = data['desk_id']

        self.s.send(json.dumps(json_info).encode())