#coding=utf-8
#导入核心模块
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
import markdown2 #用于Markdown的渲染

#MarkdownEditor类继承于QWidget
class MarkdownEditor(QWidget):

    def __init__(self):
        super(MarkdownEditor, self).__init__()
        self.initUI()

    def initUI(self):
        #创建一个横向布局
        hbox = QHBoxLayout(self)

        #添加一个文本输入框，并绑定TextChanged事件
        self.editor = QTextEdit(self)
        self.editor.setFrameShape(QFrame.StyledPanel)
        self.editor.textChanged.connect(self.onTextChanged)

        #添加QwebView，用于显示渲染后的HTML文档
        self.web = QWebEngineView()
        self.web.setHtml("start typing on the left pane")

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.web)

        #将控件添加到布局中
        hbox.addWidget(splitter)
        self.setLayout(hbox)

        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

        #设置窗口位置和大小
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('MarkdownEditor')
        self.show()

    #编写TextChanged响应函数：当文本编辑区的内容改变时执行渲染动作
    def onTextChanged(self):
        try:
            html = markdown2.markdown(self.editor.toPlainText())
        except:
            html = 'Error decoding '
        self.web.setHtml(html)

#定义主函数
def main():
    app = QApplication(sys.argv)
    ex = MarkdownEditor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()