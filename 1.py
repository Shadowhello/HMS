from widgets.ui import *
from widgets.bwidget import *

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    splash = SplashScreen(QPixmap(file_ico("login.png")))
    splash.fadeTicker(0)
    app.processEvents()
    mainwindow = QWidget()
    mainwindow.show()
    splash.finish(mainwindow)

    sys.exit(app.exec_())