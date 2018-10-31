from widgets.bwidget import *
from cefpython3 import cefpython as cef
import platform,ctypes
import sys

WINDOWS = (platform.system() == "Windows")

class CefWidget(QWidget):

    is_first = False

    def __init__(self, parent=None):
        super(CefWidget, self).__init__(parent)
        self.parent = parent
        self.browser = None
        self.hidden_window = None  # Required for PyQt5 on Linux
        self.show()

    def focusInEvent(self, event):
        # This event seems to never get called on Linux, as CEF is
        # stealing all focus due to Issue #284.
        if self.browser:
            cef.WindowUtils().OnSetFocus(self.getHandle(), 0, 0, 0)
            self.browser.SetFocus(True)

    def focusOutEvent(self, event):
        # This event seems to never get called on Linux, as CEF is
        # stealing all focus due to Issue #284.
        if self.browser:
            self.browser.SetFocus(False)

    # 第一次打开
    def embedBrowser(self,url):
        # 获取组件
        window_info = cef.WindowInfo()

        rect = [0, 0, self.width(),self.height()]
        window_info.SetAsChild(self.getHandle(), rect)
        # 初始化浏览器环境
        self.browser = cef.CreateBrowserSync(window_info=window_info,url=url)
        # self.browser.SetClientHandler(LoadHandler(self.parent.navigation_bar))
        self.browser.SetClientHandler(FocusHandler(self))
        self.is_first = True

    # 后面打开新网页
    def load_new_url(self,url):
        if self.browser:
            self.browser.LoadUrl(url)

    def load(self,url):
        # 已完成初始化
        if self.browser:
            if self.is_first:
                self.load_new_url(url)
            else:
                self.embedBrowser(url)
        else:
            self.embedBrowser(url)

    def reload(self):
        if self.browser:
            self.browser.Reload()

    def getHandle(self):
        if self.hidden_window:
            # PyQt5 on Linux
            return int(self.hidden_window.winId())
        try:
            # PyQt4 and PyQt5
            return int(self.winId())
        except:
            # PySide:
            # | QWidget.winId() returns <PyCObject object at 0x02FD8788>
            # | Converting it to int using ctypes.
            if sys.version_info[0] == 2:
                # Python 2
                ctypes.pythonapi.PyCObject_AsVoidPtr.restype = (
                        ctypes.c_void_p)
                ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = (
                        [ctypes.py_object])
                return ctypes.pythonapi.PyCObject_AsVoidPtr(self.winId())
            else:
                # Python 3
                ctypes.pythonapi.PyCapsule_GetPointer.restype = (
                        ctypes.c_void_p)
                ctypes.pythonapi.PyCapsule_GetPointer.argtypes = (
                        [ctypes.py_object])
                return ctypes.pythonapi.PyCapsule_GetPointer(
                        self.winId(), None)

    def moveEvent(self, _):
        self.x = 0
        self.y = 0
        if self.browser:
            if WINDOWS:
                cef.WindowUtils().OnSize(self.getHandle(), 0, 0, 0)
            self.browser.NotifyMoveOrResizeStarted()

    def resizeEvent(self, event):
        size = event.size()
        if self.browser:
            if WINDOWS:
                cef.WindowUtils().OnSize(self.getHandle(), 0, 0, 0)
            self.browser.NotifyMoveOrResizeStarted()


    def closeEvent(self, event):
        if self.browser:
            self.browser.CloseBrowser(True)
            # self.clear_browser_references()
            self.browser = None

class LoadHandler(object):
    def __init__(self, navigation_bar):
        self.initial_app_loading = True
        self.navigation_bar = navigation_bar

    def OnLoadingStateChange(self, **_):
        self.navigation_bar.updateState()

    def OnLoadStart(self, browser, **_):
        self.navigation_bar.url.setText(browser.GetUrl())
        if self.initial_app_loading:
            self.navigation_bar.cef_widget.setFocus()

class FocusHandler(object):
    def __init__(self, cef_widget):
        self.cef_widget = cef_widget

    def OnSetFocus(self, **_):
        pass

    def OnGotFocus(self, browser, **_):
        # Temporary fix no. 1 for focus issues on Linux (Issue #284)
        pass

# 浏览器工具栏 后退、前进、刷新、URL地址栏
class NavigationBar(QFrame):

    def __init__(self, cef_widget):
        # noinspection PyArgumentList
        super(NavigationBar, self).__init__()
        self.cef_widget = cef_widget

        # Init layout
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Back button
        self.back = QPushButton(Icon('back'),"back")
        # noinspection PyUnresolvedReferences
        self.back.clicked.connect(self.onBack)
        # noinspection PyArgumentList
        layout.addWidget(self.back, 0, 0)

        # Forward button
        self.forward = QPushButton(Icon('forward'),"forward")
        # noinspection PyUnresolvedReferences
        self.forward.clicked.connect(self.onForward)
        # noinspection PyArgumentList
        layout.addWidget(self.forward, 0, 1)

        # Reload button
        self.reload = QPushButton(Icon('reload'),"reload")
        # noinspection PyUnresolvedReferences
        self.reload.clicked.connect(self.onReload)
        # noinspection PyArgumentList
        layout.addWidget(self.reload, 0, 2)

        # Url input
        self.url = QLineEdit("")
        # noinspection PyUnresolvedReferences
        self.url.returnPressed.connect(self.onGoUrl)
        # noinspection PyArgumentList
        layout.addWidget(self.url, 0, 3)

        # Layout
        self.setLayout(layout)
        self.updateState()

    def onBack(self):
        if self.cef_widget.browser:
            self.cef_widget.browser.GoBack()

    def onForward(self):
        if self.cef_widget.browser:
            self.cef_widget.browser.GoForward()

    def onReload(self):
        if self.cef_widget.browser:
            self.cef_widget.browser.Reload()

    def onGoUrl(self):
        if self.cef_widget.browser:
            self.cef_widget.browser.LoadUrl(self.url.text())

    def updateState(self):
        browser = self.cef_widget.browser
        if not browser:
            self.back.setEnabled(False)
            self.forward.setEnabled(False)
            self.reload.setEnabled(False)
            self.url.setEnabled(False)
            return
        self.back.setEnabled(browser.CanGoBack())
        self.forward.setEnabled(browser.CanGoForward())
        self.reload.setEnabled(True)
        self.url.setEnabled(True)
        self.url.setText(browser.GetUrl())

class QBrowser(QDialog):

    open_url = pyqtSignal(str,str) # 标题和url

    def __init__(self,parent):
        super(QBrowser,self).__init__(parent)
        self.setMinimumHeight(800)
        self.setMinimumWidth(800)
        self.initUI()
        self.open_url.connect(self.load)
        self.show()

    def initUI(self):
        lt_main = QHBoxLayout()
        self.browser = CefWidget(self)
        lt_main.addWidget(self.browser)
        self.setLayout(lt_main)

    def load(self,title,url):
        self.setWindowTitle(title)
        if self.browser.is_first:
            self.browser.load_new_url(url)
        else:
            self.browser.embedBrowser(url)

class CefApplication(QApplication):
    def __init__(self, args):
        super(CefApplication, self).__init__(args)
        if not cef.GetAppSetting("external_message_pump"):
            self.timer = self.createTimer()
        # self.setupIcon()

    def createTimer(self):
        timer = QTimer()
        # noinspection PyUnresolvedReferences
        timer.timeout.connect(self.onTimer)
        timer.start(10)
        return timer

    def onTimer(self):
        cef.MessageLoopWork()

    def stopTimer(self):
        # Stop the timer after Qt's message loop has ended
        self.timer.stop()

    def setupIcon(self):
        icon_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 "resources", "{0}.png".format(sys.argv[1]))
        if os.path.exists(icon_file):
            self.setWindowIcon(QIcon(icon_file))

# demo
def open_url_demo(url,title):
    # To shutdown all CEF processes on error
    sys.excepthook = cef.ExceptHook
    cef.Initialize()
    cef.CreateBrowserSync(url=url,window_title=title)
    cef.MessageLoop()
    cef.Shutdown()

if __name__ =='__main__':
    pass

