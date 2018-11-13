from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import time

class MyWindow(QPushButton):

    def __init__(self):
        QPushButton.__init__(self)
        self.setText("关闭窗口")
        self.clicked.connect(qApp.quit)

    def load_data(self, sp):
        for i in range(1, 3):              #模拟主程序加载过程
            time.sleep(2)                   # 加载数据
            sp.showMessage("加载... {0}%".format(i * 10), Qt.AlignHCenter |Qt.AlignBottom, Qt.black)
            qApp.processEvents()  # 允许主进程处理事件


class SplashScreen(QSplashScreen):

    def __init__(self,pixmap):
        super(SplashScreen,self).__init__()
        ProgressBar = QProgressBar()
        # 设置进度条的位置
        ProgressBar.setGeometry(0, pixmap.height() - 50, pixmap.width(), 30)
        # 设置进度条的样式
        ProgressBar.setStyleSheet("QProgressBar {color:black;font:30px;text-align:center; }QProgressBar::chunk {background-color: rgb(202, 165, 14);}")
        # 设置进度条的范围
        ProgressBar.setRange(0, 100)
        # 设置进度条的当前进度
        ProgressBar.setValue(0)
        # generateAscendRandomNumber()
        self.setProgress()

    def setProgress(self):
        timer = QTimer()



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap("login.png"))
    splash.showMessage("加载... 0%", Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
    splash.show()                           # 显示启动界面
    qApp.processEvents()                    # 处理主进程事件
    window = MyWindow()
    window.setWindowTitle("QSplashScreen类使用")
    window.resize(300, 30)
    window.load_data(splash)                # 加载数据
    window.show()
    splash.finish(window)                   # 隐藏启动界面

