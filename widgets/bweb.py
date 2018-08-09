from PyQt5.QtWebEngineWidgets import *
from widgets.bwidget import *

class WebEngine(QWebEngineView):

    def load(self,url:str):
        self.setUrl(QUrl(url))

    def setJS(self):
        settings = QWebEngineSettings.globalSettings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)