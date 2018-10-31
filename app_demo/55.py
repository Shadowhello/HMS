from PyQt5.QtWidgets import QWidget,QLabel,QVBoxLayout,QPushButton,QMessageBox
from PyQt5.QtCore import pyqtSignal,QTimer
from PyQt5.QtGui import QPixmap,QPainter, QColor
from PyQt5.QtCore import QCoreApplication,pyqtSignal,QObject,Qt

class LoadingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.cnt=0
        self.pix=QPixmap('1.png')
        #setAttribute(Qt::WA_DeleteOnClose)
        self.setWindowOpacity(1)
        #窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        #self.showFullScreen()
        # 新建一个QTimer对象
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.start()
        # 信号连接到槽
        self.timer.timeout.connect(self.onTimerOut)

    # 定义槽
    def onTimerOut(self):
        self.update()

    def paintEvent(self, paintEvent):
        painter = QPainter(self)
        painter.setBrush(QColor("#CCCCFF"))
        painter.setPen(QColor("#00FF00"))
        painter.setRenderHint(QPainter.Antialiasing) ## 抗锯齿
        painter.drawRoundedRect(0,0,self.width()-1,self.height() -1,20,20)
        painter.translate(self.width()/2,self.height()/2)
        painter.rotate(self.cnt)
        painter.translate(-self.width()/2,-self.height()/2)
        painter.drawPixmap(0,0,self.width(),self.height(),self.pix)

        if self.cnt >= 360:
            self.cnt=0
        else:
            self.cnt +=1
