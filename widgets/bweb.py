from widgets.bwidget import *
# 判断版本号
if PYQT_VERSION_STR =='5.5.1':
    from PyQt5.QtWebKit import *
    from PyQt5.QtWebKitWidgets import *
else:
    from PyQt5.QtWebEngineWidgets import *
    from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
    from PyQt5.QtWebEngineWidgets import QWebEngineSettings as QWebSettings

class WebView(QWebView):

    def load(self,url:str):
        self.setUrl(QUrl(url))
        if PYQT_VERSION_STR == '5.5.1':
            self.setJS2()
        else:
            self.setJS()

    # PyQt 5.6 以上设置
    def setJS(self):
        self.settings = QWebSettings.globalSettings()
        # self.settings.setAttribute(QWebSettings.JavascriptEnabled, True)
        self.settings.setAttribute(QWebSettings.LocalContentCanAccessFileUrls, True)
        self.settings.setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)

    # PyQt5.5 版本中设置
    def setJS2(self):
        self.settings = QWebSettings.globalSettings()
        self.settings.setAttribute(QWebSettings.LocalContentCanAccessFileUrls, True)
        self.settings.setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings.setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

    # def resizeEvent(self,event):
    #     self.resize(500,1000)
