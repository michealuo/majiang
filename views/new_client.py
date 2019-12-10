from login import *
from socket import *

HOST = '127.0.0.1'
PORT = 8000
ADDR = (HOST, PORT)

class Client:
    def __init__(self):
        self.ADDR = ADDR
        self.create_sockfd()

    def create_sockfd(self):
        self.s = socket()
        self.s.connect(self.ADDR)

    def login(self):
        app = QApplication(sys.argv)
        regist = SignUpWidget(self.s)
        ex = Login(self.s, regist,app)
        res = ex.login()
        ex.button_regist.clicked.connect(regist.show)
        sys.exit(app.exec_())


if __name__ == '__main__':

    client = Client()
    client.login()