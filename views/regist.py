from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from sql.handle_sql import *

class SignUpWidget(QWidget):
    user_signup_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setUpUI()

    def setUpUI(self):

        self.setWindowTitle("血流成河")
        self.signUpLabel = QLabel("注   册")
        self.center()
        self.resize(550, 450)
        #背景
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("../img/background.jpg")))
        self.setPalette(palette)
        #居中
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


        self.signUpLabel.setAlignment(Qt.AlignCenter)
        self.signUpLabel.setFixedHeight(100)
        font = QFont()
        font.setPixelSize(36)
        lineEditFont = QFont()
        lineEditFont.setPixelSize(16)
        self.signUpLabel.setFont(font)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.signUpLabel, Qt.AlignHCenter)
        self.setLayout(self.layout)
        # 表单，包括名称,电话,密码,确认密码
        self.formlayout = QFormLayout()
        font.setPixelSize(18)
        # Row1
        self.usernameLabel = QLabel("名    称: ")
        self.usernameLabel.setFont(font)
        self.usernameLineEdit = QLineEdit()
        self.usernameLineEdit.setFixedWidth(180)
        self.usernameLineEdit.setFixedHeight(32)
        self.usernameLineEdit.setFont(lineEditFont)
        self.usernameLineEdit.setMaxLength(10)
        self.formlayout.addRow(self.usernameLabel, self.usernameLineEdit)

        # Row2
        self.phoneNumberLabel = QLabel("手机号: ")
        self.phoneNumberLabel.setFont(font)
        self.phoneNumberLineEdit = QLineEdit()
        self.phoneNumberLineEdit.setFixedHeight(32)
        self.phoneNumberLineEdit.setFixedWidth(180)
        self.phoneNumberLineEdit.setFont(lineEditFont)
        self.phoneNumberLineEdit.setMaxLength(12)
        self.formlayout.addRow(self.phoneNumberLabel, self.phoneNumberLineEdit)

        lineEditFont.setPixelSize(10)

        # Row3
        self.passwordLabel = QLabel("密    码: ")
        self.passwordLabel.setFont(font)
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setFixedWidth(180)
        self.passwordLineEdit.setFixedHeight(32)
        self.passwordLineEdit.setFont(lineEditFont)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordLineEdit.setMaxLength(16)
        self.formlayout.addRow(self.passwordLabel, self.passwordLineEdit)

        # Row4
        self.passwordConfirmLabel = QLabel("确认密码: ")
        self.passwordConfirmLabel.setFont(font)
        self.passwordConfirmLineEdit = QLineEdit()
        self.passwordConfirmLineEdit.setFixedWidth(180)
        self.passwordConfirmLineEdit.setFixedHeight(32)
        self.passwordConfirmLineEdit.setFont(lineEditFont)
        self.passwordConfirmLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordConfirmLineEdit.setMaxLength(16)
        self.formlayout.addRow(self.passwordConfirmLabel, self.passwordConfirmLineEdit)

        # Row5
        self.signUpbutton = QPushButton("注 册")
        self.signUpbutton.setFixedWidth(120)
        self.signUpbutton.setFixedHeight(30)
        self.signUpbutton.setFont(font)
        self.formlayout.addRow("", self.signUpbutton)
        widget = QWidget()
        widget.setLayout(self.formlayout)
        widget.setFixedHeight(250)
        widget.setFixedWidth(300)
        self.Hlayout = QHBoxLayout()
        self.Hlayout.addWidget(widget, Qt.AlignCenter)
        widget = QWidget()
        widget.setLayout(self.Hlayout)
        self.layout.addWidget(widget, Qt.AlignHCenter)

        self.signUpbutton.clicked.connect(self.SignUp)
        self.usernameLineEdit.returnPressed.connect(self.SignUp)
        self.phoneNumberLineEdit.returnPressed.connect(self.SignUp)
        self.passwordLineEdit.returnPressed.connect(self.SignUp)
        self.passwordConfirmLineEdit.returnPressed.connect(self.SignUp)

    #居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def SignUp(self):
        #获取 ip 名称 电话 密码 确认密码
        ip = get_host_ip()
        username = self.usernameLineEdit.text()
        phone_num = self.phoneNumberLineEdit.text()
        pwd = self.passwordLineEdit.text()
        pwd_confirm = self.passwordConfirmLineEdit.text()
        #进行校验

        msg = self.check_regist(username, phone_num, pwd, pwd_confirm)

        if msg == "注册成功":
            user_ = user(username,pwd,ip,phone_num)
            Handle_Sql().insert_one(user_)
            self.close()
        else:
            QMessageBox.question(self, "Message", '注册失败:'+msg,
                                 QMessageBox.Ok, QMessageBox.Ok)

    def check_regist(self,*args):
        #非空校验
        if not check_none(*args):
            return "注册信息不能为空"
        #密码确认密码校验
        if not check_password(args[2],args[3]):
            return "密码和确认密码不一致"
        #用户名是否重复校验
        if Handle_Sql().check(user(args[0])):
            return "用户名重复,请重新命名"
        return "注册成功"

