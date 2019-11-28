from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class EnterGame(QDialog):

    def __init__(self,s):
        self.s=s
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
        self.label=QLabel("欢迎加入游戏大厅",self)
        self.label.setGeometry(270, 10, 150, 80)
        #设置字体大小
        self.label.setFont(QFont("Microsoft YaHei",10,QFont.Bold))
        #设置颜色
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
    #按钮点击函数
    def on_click(self):

        self.s.send('ready'.encode())
        while True:
            data = self.s.recv(1024)

            if data.decode() == 'Pok':
                print(data.decode())
                #进入游戏界面
            elif data.decode() == 'longin':
                print(data.decode())

        # QMessageBox.question(self, "Message", 'You typed:' + username,
        #                      QMessageBox.Ok, QMessageBox.Ok)
        # QMessageBox.question(self, "Message", 'You typed:' + pwd,
        #                      QMessageBox.Ok, QMessageBox.Ok)
