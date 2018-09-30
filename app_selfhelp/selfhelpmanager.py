from widgets.cwidget import *

class selfHelpManager(Widget):

    def __init__(self,parent=None):
        super(selfHelpManager,self).__init__(parent)
        # 载入样式
        self.stylesheet = file_style(gol.get_value('file_qss', 'mztj.qss'))
        with open(self.stylesheet) as f:
            self.setStyleSheet(f.read())
        self.initUI()

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_top = QHBoxLayout()
        lt_middle = QHBoxLayout()
        lt_bottom = QHBoxLayout()
        # 头部：体检中心名称、时间
        # lb_title = TitleLabel('明州国际医疗保健')
        # lb_time = TimerLabel()
        # lt_top.addWidget(lb_title)
        # lt_top.addWidget(lb_time)
        # 中部 功能区
        lt_btns = QGridLayout()
        self.btn_order = selfButton(Icon('取号'),'签到取号')
        self.btn_report = selfButton(Icon('报告'),'体检报告')
        self.btn_charge = selfButton(Icon('缴费'),'自助缴费')
        self.btn_mydpj = selfButton(Icon('评价'),'服务评价')
        lt_btns.addWidget(self.btn_order, 0, 0, 1, 1)
        lt_btns.addWidget(self.btn_report, 0, 1, 1, 1)
        lt_btns.addWidget(self.btn_charge, 1, 0, 1, 1)
        lt_btns.addWidget(self.btn_mydpj, 1, 1, 1, 1)
        lt_btns.setHorizontalSpacing(50)  # 设置水平间距
        lt_btns.setVerticalSpacing(50)  # 设置垂直间距
        lt_btns.setContentsMargins(50, 50, 50, 50)  # 设置外间距
        lt_btns.setColumnStretch(3, 1)  # 设置列宽，添加空白项的
        lt_middle.addStretch()
        lt_middle.addLayout(lt_btns)
        lt_middle.addStretch()
        lt_main.addStretch()
        lt_main.addLayout(lt_middle)
        lt_main.addStretch()
        self.setLayout(lt_main)

    def setBackgroundImage(self):
        palette=QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(file_ico("mztjbj.jpg"))))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def initTop(self):
        pass

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.drawPixmap(0,0,self.width(),self.height(),QPixmap(file_ico("mztjbj.jpg")))


class TitleLabel(QLabel):

    def __init__(self,p_str):
        super(TitleLabel,self).__init__()
        self.setText(p_str)
        self.setStyleSheet('''font: 75 20pt \"微软雅黑\";color:  rgb(215, 202, 153);''')

class TimeLabel(QLabel):

    def __init__(self):
        super(TimeLabel,self).__init__()
        #定时器
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.on_time_show)

    def on_time_show(self):
        now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.setText("当前时间：%s" %now)

class selfButton(QToolButton):

    def __init__(self,icon,name):
        super(selfButton,self).__init__()
        self.setIcon(icon)
        self.setText(name)
        self.setIconSize(QSize(128,128))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setAutoRaise(True)
        self.setObjectName("toolB")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = selfHelpManager()
    ui.showMaximized()
    app.exec_()