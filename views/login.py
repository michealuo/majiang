import json

from regist import *
from entergame import *
class Login(QDialog):

    def __init__(self,s,regist,app):
        super().__init__()
        self.initUI()
        self.s =s
        self.regist=regist
        self.app=app
    def login(self):
        self.frame = QFrame(self)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.frame.move(200, 200)

        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setPlaceholderText("请输入账号")
        # self.lineEdit_account.resize(250, 150)
        self.lineEdit_account.move(150, 120)
        self.verticalLayout.addWidget(self.lineEdit_account)

        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText("请输入密码")
        # self.lineEdit_password.resize(250, 150)
        self.lineEdit_password.move(150, 120)
        self.verticalLayout.addWidget(self.lineEdit_password)

        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        # 文字显示居中
        self.lineEdit_account.setAlignment(Qt.AlignCenter)
        self.lineEdit_password.setAlignment(Qt.AlignCenter)

        # 登录注册按钮
        self.button_login = QPushButton("登录", self)
        self.button_regist = QPushButton("注册", self)

        self.button_login.setGeometry(150, 300, 100, 40)
        self.button_regist.setGeometry(300, 300, 100, 40)
        self.button_login.clicked.connect(self.on_click_check)
        self.button_regist.clicked.connect(self.on_click_regist)
        self.show()

    #初始化界面
    def initUI(self):

        self.setWindowTitle("血流成河")
        self.setWindowIcon(QIcon('../img/hongzhong.jpg'))
        self.center()
        self.resize(550, 450)
        # 设置对象名称
        self.setObjectName("MainWindow")
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # #todo 1 设置窗口背景图片
        self.setStyleSheet("#MainWindow{border-image:url(../img/background.jpg);}")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @pyqtSlot()
    def on_click_regist(self):
        signup = SignUpWidget(self.s)
        signup.usernameLineEdit.textChanged.connect(self.username_inner_slot)
        signup.passwordLineEdit.textChanged.connect(self.password_inner_slot)

    @pyqtSlot()
    def on_click_check(self):
        #用户名
        username = self.lineEdit_account.text()
        #密码
        pwd = self.lineEdit_password.text()
        #点击登录按钮发送服务器进入游戏请求
        json_info = {'protocol':'L','username':username,'password':pwd}
        #去服务器校验用户名密码是否正确
        self.s.send(json.dumps(json_info).encode())
        #返回校验值
        data = json.loads(self.s.recv(1024).decode())

        #校验失败
        if data['protocol'] =='Lno':
            QMessageBox.question(self, "Message", '登录失败:错误的用户名或密码',
                                 QMessageBox.Ok, QMessageBox.Ok)
        #校验成功
        elif data['protocol'] =='Lyes':

            # 跳转到进入游戏界面
            self.jump_to_EnterGame(username)

    # 跳转到进入游戏界面
    def jump_to_EnterGame(self,username):

        self.hide()
        enter = EnterGame(self.s,username)
        enter.initUI()
        enter.show()
        enter.exec_()
        self.show()

    def username_inner_slot(self, date):
        self.lineEdit_account.setText(str(date))

    def password_inner_slot(self, date):
        self.lineEdit_password.setText(str(date))
