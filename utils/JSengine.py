from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import *
import sys



class TInteractObj(QObject):
    SigReceivedMessFromJS = pyqtSignal(str)
    SigSendMessageToJS = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(str)
    def JSSendMessage(self, strParameter):
        print('JSSendMessage(%s) from Html' % strParameter)
        self.SigReceivedMessFromJS.emit(strParameter)

    @pyqtSlot(result=str)
    def fun(self):
        print('TInteractObj.fun()')
        return 'hello'

class TMainWindow(QDialog):
    SigSendMessageToJS = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # ---Qt widget and layout---
        self.mpQtContentTextEdit = QPlainTextEdit(self)
        self.mpQtContentTextEdit.setMidLineWidth(400)
        self.mpQtContentTextEdit.setReadOnly(True)

        self.mpQtSendLineEdit = QLineEdit(self)

        self.mpQtSendBtnByInteractObj = QPushButton('Send', self)
        self.mpQtSendBtnByInteractObj.setToolTip('Send message by Interact object style')

        self.mpQtSendBtnByJavaScript = QPushButton('Send2', self)
        self.mpQtSendBtnByJavaScript.setToolTip('Send message by runJavaScript style')

        self.pQtSendHLayout = QHBoxLayout()
        self.pQtSendHLayout.setSpacing(0)
        self.pQtSendHLayout.addWidget(self.mpQtSendLineEdit)
        self.pQtSendHLayout.addSpacing(5)
        self.pQtSendHLayout.addWidget(self.mpQtSendBtnByInteractObj)
        self.pQtSendHLayout.addSpacing(5)
        self.pQtSendHLayout.addWidget(self.mpQtSendBtnByJavaScript)

        self.pQtTotalVLayout = QVBoxLayout()
        self.pQtTotalVLayout.setSpacing(0)
        self.pQtTotalVLayout.addWidget(self.mpQtContentTextEdit)
        self.pQtTotalVLayout.setSpacing(5)
        self.pQtTotalVLayout.addLayout(self.pQtSendHLayout)

        self.pQtGroup = QGroupBox('Qt View', self)
        self.pQtGroup.setLayout(self.pQtTotalVLayout)

        # ---Web widget and layout---
        self.mpJSWebView = QWebEngineView(self)
        self.pWebChannel = QWebChannel(self.mpJSWebView.page())
        self.pInteractObj = TInteractObj(self)
        self.pWebChannel.registerObject("interactObj", self.pInteractObj)

        self.mpJSWebView.page().setWebChannel(self.pWebChannel)

        self.url = 'file:///JSTest.html'
        self.mpJSWebView.page().load(QUrl(self.url))
        self.mpJSWebView.show()

        self.pJSTotalVLayout = QVBoxLayout()
        self.pJSTotalVLayout.setSpacing(0)
        self.pJSTotalVLayout.addWidget(self.mpJSWebView)
        self.pWebGroup = QGroupBox('Web View', self)
        self.pWebGroup.setLayout(self.pJSTotalVLayout)

        # ---TMainWindow total layout---
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.pQtGroup)
        self.mainLayout.setSpacing(5)
        self.mainLayout.addWidget(self.pWebGroup)
        self.setLayout(self.mainLayout)
        self.setMinimumSize(1130, 680)

        self.mpQtSendBtnByInteractObj.clicked.connect(self.OnSendMessageByInteractObj)
        self.mpQtSendBtnByJavaScript.clicked.connect(self.OnSendMessageByJavaScript)
        self.pInteractObj.SigReceivedMessFromJS.connect(self.OnReceiveMessageFromJS)
        self.SigSendMessageToJS.connect(self.pInteractObj.SigSendMessageToJS)

    def OnReceiveMessageFromJS(self, strParameter):
        print('OnReceiveMessageFromJS()')
        if not strParameter:
            return
        self.mpQtContentTextEdit.appendPlainText(strParameter)

    def OnSendMessageByInteractObj(self):
        strMessage = self.mpQtSendLineEdit.text()
        if not strMessage:
            return
        self.SigSendMessageToJS.emit(strMessage)

    def OnSendMessageByJavaScript(self):
        strMessage = self.mpQtSendLineEdit.text()
        if not strMessage:
            return
        strMessage = 'Received string from Qt:' + strMessage
        self.mpJSWebView.page().runJavaScript("output(%s)" % strMessage)
        self.mpJSWebView.page().runJavaScript("showAlert()")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    dlg = TMainWindow()
    dlg.show()

    app.exec_()