from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time

# 基础控件、基础组合控件 完全与业务无关

class SplashScreen(QSplashScreen):

    def __init__(self, splash_image):
        super(SplashScreen, self).__init__(splash_image)    # 启动程序的图片
        self.setWindowModality(Qt.ApplicationModal)

    def fadeTicker(self, keep_t):
        self.setWindowOpacity(0)
        t = 0
        while t <= 50:
            newOpacity = self.windowOpacity() + 0.02   # 设置淡入
            if newOpacity > 1:
                break
            self.setWindowOpacity(newOpacity)
            self.show()
            t -= 1
            time.sleep(0.04)
        self.show()
        time.sleep(keep_t)
        t = 0
        while t <= 50:
            newOpacity = self.windowOpacity() - 0.02   # 设置淡出
            if newOpacity < 0:
                self.close()
                break
            self.setWindowOpacity(newOpacity)
            self.show()
            t += 1
            time.sleep(0.04)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    splash = SplashScreen(QPixmap("login.png"))
    splash.fadeTicker(1)
    app.processEvents()
    mainwindow = QWidget()
    mainwindow.show()
    splash.finish(mainwindow)

    sys.exit(app.exec_())

