import faulthandler
import os
import sys
import traceback

from PyQt5.QtCore import QThread, QSize, QCoreApplication
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QPushButton, QMessageBox,\
    QWidget, QVBoxLayout, QLabel


__version__ = "0.0.1"


class QtThread(QThread):
    '''
    Qt thread 异常捕捉
    '''

    def run(self):
        # 这里实在没有找到好的实例代码,将就使用这个来产生错误让faulthandler捕捉到
        # 此时这个错误sys.excepthook是无法捕捉到的
        # 该异常会弹出python.exe停止运行
        a = QCoreApplication(sys.argv)
        p = QPixmap(QSize(10, 10))
        a.exec_()


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(400, 200)
        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton("点击生成异常并再次运行程序查看",
                                     self, clicked=self.onMakeError))
        layout.addWidget(QPushButton("点击运行Qt子线程生成异常", self,
                                     clicked=self.onMakeThreadError))
        self.label = QLabel("test", self)
        layout.addWidget(self.label)

        self.pixmap = QPixmap(QSize(20, 20))

        # bug提交
        self.bugreport()

        #****重要的一句话****
        # 注释这句话当生成异常时会弹出python.exe停止运行的对话框
        # 开启这句话时则会捕捉异常并写入文件(实验中有些情况可能不会写入,具体看官方doc)
        # 捕捉异常并写入error.txt中
        faulthandler.enable(file=open("error.txt", "ab"), all_threads=True)

    def onMakeError(self):
        # 该错误可以直接被python层捕捉
        QPainter.drawEllipse(self.rect())

    def onMakeThreadError(self):
        self.thread = QtThread(self)
        self.thread.start()

    def bugreport(self):
        try:
            if not os.path.isfile("error.txt"):
                return
            data = open("error.txt", "rb").read().decode()
            if not data:
                return
            if QMessageBox.question(None, "异常反馈", data) == QMessageBox.Yes:
                print("联网提交错误日志")
        except Exception as e:
            print("bugreport eror: ", e)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        return sys.__excepthook__(exc_type, exc_value, exc_traceback)
    open("error.txt", "ab").write("".join(traceback.format_exception(
        exc_type, exc_value, exc_traceback)).encode())
    sys.exit(0)  # 一般app报错后会直接退出,这里模拟退出


# 配合使用捕捉python层异常
sys.excepthook = handle_exception

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("异常捕捉")
    w = Window()
    w.show()
    sys.exit(app.exec_())