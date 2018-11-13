from widgets.utils import *

class OaUI(BrowserWidget):

    def __init__(self,parent=None):
        super(OaUI,self).__init__(parent)
        self.setWindowTitle("OA系统")
        self.show()
        self.initUI()


    def initUI(self):
        lt_main = QHBoxLayout()
        self.browser = CefWidget(self)
        lt_main.addWidget(self.browser)
        self.setLayout(lt_main)

    # 载入必须在整体控件show后面，不是仅仅show后面
    def load(self):
        self.browser.embedBrowser("http://sso.auxgroup.com/login?service=https://newoa.auxgroup.com/index.jsp")


class PhonePlatUI(BrowserWidget):

    def __init__(self,parent=None):
        super(PhonePlatUI,self).__init__(parent)
        self.setWindowTitle("电话平台")
        self.show()
        self.initUI()


    def initUI(self):
        lt_main = QHBoxLayout()
        self.browser = CefWidget(self)
        lt_main.addWidget(self.browser)
        self.setLayout(lt_main)

    # 载入必须在整体控件show后面，不是仅仅show后面
    def load(self):
        self.browser.embedBrowser("http://10.8.103.211:8088/ec2")


class JHJKGLUI(BrowserWidget):

    def __init__(self,parent=None):
        super(JHJKGLUI,self).__init__(parent)
        self.setWindowTitle("检后健康")
        self.show()
        self.initUI()


    def initUI(self):
        lt_main = QHBoxLayout()
        self.browser = CefWidget(self)
        lt_main.addWidget(self.browser)
        self.setLayout(lt_main)

    # 载入必须在整体控件show后面，不是仅仅show后面
    def load(self):
        self.browser.embedBrowser("http://10.7.200.198:4415/Login.aspx")


class MediaUI(BrowserWidget):

    def __init__(self,parent=None):
        super(MediaUI,self).__init__(parent)
        self.setWindowTitle("多媒体屏")
        self.show()
        self.initUI()


    def initUI(self):
        lt_main = QHBoxLayout()
        self.browser = CefWidget(self)
        lt_main.addWidget(self.browser)
        self.setLayout(lt_main)

    # 载入必须在整体控件show后面，不是仅仅show后面
    def load(self):
        self.browser.embedBrowser("http://10.8.200.104/admin/index/logon/")