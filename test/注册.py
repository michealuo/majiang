__author__ = 'ayew'
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import*
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QHBoxLayout,  QVBoxLayout, QGridLayout, QFormLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QIcon,QPalette,QBrush,QPixmap

class login(QWidget):
    def __init__(self):
        super(login,self).__init__()
        self.initUi()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def initUi(self):
        self.setWindowTitle("血流成河")
        self.setWindowIcon(QIcon('../img/hongzhong.jpg'))
        layout = QGridLayout()
        self.setGeometry(600, 600, 400, 400)

        self.center()

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("../img/background.jpg")))
        self.setPalette(palette)

        nameLabel = QLabel("姓名")
        self.nameLineEdit = QLineEdit(" ")
        sexLabel = QLabel("性别")
        self.sexLineEdit = QLineEdit(" ")
        emitLabel = QLabel("手机号")
        self.phoneLineEdit = QLineEdit("")
        timeLabel = QLabel("邮箱")
        self.mailEdit = QLineEdit("")
        # layout.setSpacing(10)
        layout.addWidget(nameLabel,1,0)
        layout.addWidget(self.nameLineEdit,1,1)
        layout.addWidget(sexLabel, 2, 0)
        layout.addWidget(self.sexLineEdit, 2, 1)
        layout.addWidget(emitLabel,3,0)
        layout.addWidget(self.phoneLineEdit,3,1)
        layout.addWidget(timeLabel,4,0)
        layout.addWidget(self.mailEdit,4,1)
        layout.setColumnStretch(1, 10)

        save_Btn = QPushButton('提交')
        cancle_Btn = QPushButton('返回')

        cancle_Btn.clicked.connect(self.submit_click)
        save_Btn.clicked.connect(self.return_click)

        layout.addWidget(save_Btn)
        layout.addWidget(cancle_Btn)
        self.setLayout(layout)

    def return_click(self):
        self.close()


    def submit_click(self):
        name = self.nameLineEdit.text()  # 获取文本框内容
        sex = self.sexLineEdit.text()
        phone = self.phoneLineEdit.text()
        mail = self.mailEdit.text()
        print('姓名: %s 性别: %s 手机号: %s 邮箱: %s ' % (name,
                                                     sex, phone, mail))


app = QApplication(sys.argv)

res = login()
res.show()
sys.exit(app.exec_())