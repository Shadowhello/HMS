from widgets.browser import *
from widgets.bwidget import *

class OaUI(TabWebView):

    def __init__(self,parent=None):
        super(OaUI, self).__init__(parent)

        ####第一个tab
        self.webview = WebEngineView(self)   #self必须要有，是将主窗口作为参数，传给浏览器
        self.webview.load(QUrl("http://sso.auxgroup.com/login?service=https://newoa.auxgroup.com/index.jsp"))
        self.addPage(self.webview)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QCoreApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)   #这句解决错误警告：ERROR:gl_context_wgl.cc(78)] Could not share GL contexts.
    the_mainwindow = OaUI()
    the_mainwindow.show()
    sys.exit(app.exec_())
