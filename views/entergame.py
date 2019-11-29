from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
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

        # todo 2 设置窗口背景色
        # win.setStyleSheet("#MainWindow{background-color: yellow}")
        # 控件QPushButton的定义和设置
        # 设置控件QPushButton的位置和大小
        # create textbox
        # self.textbox = QLineEdit(self)
        # self.textbox.move(20, 220)
        # self.textbox.resize(280, 40)

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
        print("=========")
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
        #点击进入游戏给服务器发送进入游戏的请求
        self.s.send('E ready'.encode())
        while True:
            data = self.s.recv(1024)

            if data.decode() == 'Pok':
                print(data.decode())
                #进入游戏界面
                # self.playgame()
            elif data.decode() == 'longin':
                print(data.decode())
    # def playgame(self):
    #
    #     # 初始化牌库
    #     majiang = []
    #     for i in range(3):
    #         for j in range(1, 10):
    #             for k in range(4):
    #                 if i == 0:
    #                     majiang.append(str(j) + "万")
    #                 if i == 1:
    #                     majiang.append(str(j) + "条")
    #                 if i == 2:
    #                     majiang.append(str(j) + "饼")
    #     wan = ['1万', '2万', '3万', '4万', '5万', '6万', '7万', '8万', '9万']
    #     tiao = ['1条', '2条', '3条', '4条', '5条', '6条', '7条', '8条', '9条']
    #     bing = ['1饼', '2饼', '3饼', '4饼', '5饼', '6饼', '7饼', '8饼', '9饼']
    #
    #     # 初始化牌库
    #     majiang_split = start()
    #
    #     # 初始化自己手牌
    #     me = Me(majiang_split[3])
    #     # 剩余牌库(将牌库给4个玩家后的麻将牌库)
    #     majiang = majiang[52:]
    #
    #     # 记录出牌顺序
    #     i = 0
    #     # 牌库还有牌继续
    #     while majiang != []:
    #         # 是否有杠
    #         gang_flag = 0
    #         try:
    #             # 获取牌并且返回一张牌
    #             put = me.get_majiang(majiang.pop(0))
    #
    #         except IndexError:
    #             # majiang[0]没有值,牌库空了
    #             g.msgbox('黄了！', '麻将三缺一')
    #             sys.exit(0)
        # QMessageBox.question(self, "Message", 'You typed:' + username,
        #                      QMessageBox.Ok, QMessageBox.Ok)
        # QMessageBox.question(self, "Message", 'You typed:' + pwd,
        #                      QMessageBox.Ok, QMessageBox.Ok)
