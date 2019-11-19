import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget,QMainWindow
from PyQt5.QtGui import QIcon

class Majiang(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("界面背景图片设置")
        self.setWindowIcon(QIcon('hongzhong.jpg'))
        self.resize(550, 450)
        # 设置对象名称
        self.setObjectName("MainWindow")

        # #todo 1 设置窗口背景图片
        self.setStyleSheet("#MainWindow{border-image:url(background.jpg);}")

        # todo 2 设置窗口背景色
        # win.setStyleSheet("#MainWindow{background-color: yellow}")
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Majiang()
    sys.exit(app.exec_())