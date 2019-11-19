import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon

class Majiang(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("血流成河")
        self.setWindowIcon(QIcon('hongzhong.jpg'))
        self.resize(550, 450)
        # 设置对象名称
        self.setObjectName("MainWindow")
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # #todo 1 设置窗口背景图片
        self.setStyleSheet("#MainWindow{border-image:url(background.jpg);}")

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
        self.frame.move(200,200)

        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setPlaceholderText("请输入账号")
        #self.lineEdit_account.resize(250, 150)
        self.lineEdit_account.move(150, 120)
        self.verticalLayout.addWidget(self.lineEdit_account)


        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText("请输入密码")
        #self.lineEdit_password.resize(250, 150)
        self.lineEdit_password.move(150, 120)
        self.verticalLayout.addWidget(self.lineEdit_password)
        #文字显示居中
        self.lineEdit_account.setAlignment(Qt.AlignCenter)
        self.lineEdit_password.setAlignment(Qt.AlignCenter)


        self.button_login = QPushButton("登录",self)
        self.button_regist = QPushButton("注册", self)


        self.button_login.setGeometry(150, 300, 100, 40)
        self.button_regist.setGeometry(300, 300, 100, 40)
        # connect button to function on_click
        self.button_login.clicked.connect(self.on_click)
        self.button_regist.clicked.connect(self.on_click)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @pyqtSlot()
    def on_click(self):
        username = self.lineEdit_account.text()
        pwd = self.lineEdit_password.text()
        QMessageBox.question(self, "Message", 'You typed:' + username,
                             QMessageBox.Ok, QMessageBox.Ok)
        QMessageBox.question(self, "Message", 'You typed:' + pwd,
                             QMessageBox.Ok, QMessageBox.Ok)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Majiang()
    sys.exit(app.exec_())