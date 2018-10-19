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

