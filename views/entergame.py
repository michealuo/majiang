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
            self.playgame(data)
        elif data['protocol'] == 'Outtime':
            QMessageBox.question(self, "Message", '连接超时',
                                 QMessageBox.Ok, QMessageBox.Ok)

    def playgame(self,first_data):
        #第一次出牌
        self.putresult = g.choicebox(
            '您的麻将是:\n%s\n%s\n%s\n碰：%s\n杠：%s\n请选择要打的麻将' % \
            (str(first_data['wan']), str(first_data['tiao']), str(first_data['bing']),
             str(first_data['peng_majiang']), str(first_data['angang_majiang'])), '打麻将',
            first_data['majiang'])
        while True:
            data = json.loads(self.s.recv(1024).decode())