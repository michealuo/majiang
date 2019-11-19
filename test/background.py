import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QIcon
app = QApplication(sys.argv)
win = QMainWindow()

#设置窗口标题与初始大小
win.setWindowTitle("界面背景图片设置")
win.setWindowIcon(QIcon('hongzhong.jpg'))
win.resize(350, 250)
#设置对象名称
win.setObjectName("MainWindow")

# #todo 1 设置窗口背景图片
win.setStyleSheet("#MainWindow{border-image:url(hongzhong.jpg);}")

#todo 2 设置窗口背景色
#win.setStyleSheet("#MainWindow{background-color: yellow}")

win.show()
sys.exit(app.exec_())