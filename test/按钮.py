import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()  # 界面绘制交给InitUi方法

    def initUI(self):
        # 设置窗口的位置和大小

        self.setGeometry(300, 300, 300, 220)

        # 设置窗口的标题

        self.setWindowTitle('QPushButton')

        # 控件QPushButton的定义和设置

        self.button = QPushButton(self)

        self.button.setStyleSheet("QPushButton{border-image: url(hongzhong.jpg)}"

                                  "QPushButton:hover{border-image: url(img/1_1.png)}"

                                  "QPushButton:pressed{border-image: url(img/1_1.png)}")

        # 设置控件QPushButton的位置和大小

        self.button.setGeometry(100, 100, 50, 50)


if __name__ == '__main__':
    # 创建应用程序和对象

    app = QApplication(sys.argv)

    ex = Example()

    ex.show()

    sys.exit(app.exec_())
