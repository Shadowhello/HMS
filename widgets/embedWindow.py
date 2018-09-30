import win32gui,win32con
from widgets.bwidget import *

hwnd = win32gui.FindWindow("AcrobatSDIWindow","168160026.pdf - Adobe Reader")
print(hwnd)


class EmbedWindow(QDialog):

    click_opened = pyqtSignal(int)

    def __init__(self,parent=None):
        super(EmbedWindow,self).__init__(parent)
        self.setGeometry(parent.width()*2/3,50,parent.width()/3,parent.height())
        self.widget = None
        self.lt_main = QHBoxLayout()
        self.click_opened.connect(self.on_widget_open)

    def on_widget_open(self,hwnd:int):
        '''
        :param hwnd: 窗口句柄
        :return:
        '''
        if self.widget:
            self.widget.close()
            self.lt_main.removeWidget(self.widget)  # 从布局中移出
            self.widget.deleteLater()
        self.widget = QWidget.createWindowContainer(QWindow.fromWinId(hwnd))
        self.widget.hwnd = hwnd                                                         # 窗口句柄
        self.widget.phwnd = win32gui.GetParent(hwnd)                                    # 父窗口句柄
        self.widget.style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)            # 窗口样式
        self.widget.exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)        # 窗口额外样式
        self.lt_main.addWidget(self.widget)
        self.setLayout(self.lt_main)

    def closeEvent(self, QCloseEvent):
        if self.widget:
            self.widget.close()
            self.lt_main.removeWidget(self.widget)  # 从布局中移出
            self.widget.deleteLater()
        super(EmbedWindow,self).closeEvent(QCloseEvent)
