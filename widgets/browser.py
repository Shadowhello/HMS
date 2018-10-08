from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
import datetime,os


###创建浏览器
class WebEngineView(QWebEngineView):

    def __init__(self,parent):
        super(WebEngineView, self).__init__(parent)
        self.parent = parent
        ##############
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)      #支持视频播放
        self.page().windowCloseRequested.connect(self.on_windowCloseRequested)     #页面关闭请求
        self.page().profile().downloadRequested.connect(self.on_downloadRequested) #页面下载请求

    #  支持页面关闭请求
    def on_windowCloseRequested(self):
        the_index = self.parent.currentIndex()
        self.parent.removeTab(the_index)

    #  支持页面下载按钮
    def on_downloadRequested(self,downloadItem):
        if  downloadItem.isFinished()==False and downloadItem.state()==0:
            ###生成文件存储地址
            the_filename = downloadItem.url().fileName()
            if len(the_filename) == 0 or "." not in the_filename:
                cur_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                the_filename = "下载文件" + cur_time + ".xls"
            the_sourceFile = os.path.join(os.getcwd(), the_filename)

            ###下载文件
            # downloadItem.setSavePageFormat(QWebEngineDownloadItem.CompleteHtmlSaveFormat)
            downloadItem.setPath(the_sourceFile)
            downloadItem.accept()
            downloadItem.finished.connect(self.on_downloadfinished)


    #  下载结束触发函数
    def on_downloadfinished(self):
        js_string = '''alert("下载成功！");'''
        self.page().runJavaScript(js_string)

    # 重写createwindow()
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView(self.parent)
        self.parent.addPage(new_webview)

        return new_webview


class TabWebView(QTabWidget):

    status = False            #是否被打开

    widget_queue = {}         # 控件队列 打开过的不允许新增

    def __init__(self,parent=None,lb_is_close = True):
        super(TabWebView, self).__init__(parent)
        self.setTabsClosable(lb_is_close)  # 关闭标签
        self.setMovable(True)       #tab可移动
        self.setMouseTracking(True)
        self.tabCloseRequested.connect(self.dropTab)

    def dropTab(self,index):
        if self.count() > 1:
            self.removeTab(index)
        else:
            self.close()  # 当只有1个tab时，关闭主窗口

    def closeEvent(self, *args, **kwargs):
        self.status = True
        super(TabWebView, self).closeEvent(*args, **kwargs)

    #创建tab
    def addPage(self,webview):
        self.tab = QWidget()
        i = self.addTab(self.tab, "新标签页")
        self.setCurrentWidget(self.tab)
        self.webview.loadFinished.connect(lambda _, i=i, browser=self.webview:self.setTabText(i, self.webview.page().title()))
        lt_main = QHBoxLayout()
        lt_main.setContentsMargins(0, 0, 0, 0)
        lt_main.addWidget(webview)
        self.tab.setLayout(lt_main)