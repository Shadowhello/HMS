from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os,sys,time
try:
    import cv2
except Exception as e:
    print(e)
    cv2 = None
from collections import OrderedDict
import pandas as pd
from utils.base import desktop
from queue import Queue
import numpy as np


def singleton(cls):
    '''
    :param cls:
    :return:
    '''
    instances = {}

    def _singleton(*args,**kw):
        if cls not in instances:
            instances[cls] = cls(*args,**kw)

        return instances[cls]

    return _singleton

'''
获取主执行文件路径的最佳方法是用sys.argv[0]，它可能是一个相对路径，所以再取一下abspath
__file__ 是用来获得模块所在的路径的，这可能得到的是一个相对路径
'''
#基础控件实现
def app_path(name):
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    return "%s%s" %(dirname,name)

def file_ico(name):
    #print("图标目标：%s" %os.path.join(app_path(r"\resource\image"),name))
    return os.path.join(app_path(r"\resource\image"),name)

def file_style(name):
    return os.path.join(app_path(r"\resource\style"),name)

def file_tmp(name):
    return os.path.join(app_path(r"\tmp"), name)

class Icon(QIcon):

    def __init__(self,name):
        super(Icon,self).__init__()
        self.addPixmap(QPixmap(file_ico(name)),QIcon.Normal,QIcon.On)

class MessageBox(QMessageBox):

    def __init__(self, *args, count=10, **kwargs):
        super(MessageBox, self).__init__(*args, **kwargs)
        self.setWindowTitle('明州体检')
        self.setWindowIcon(Icon('mztj'))
        self.count = count
        self.setStandardButtons(self.Close)  # 关闭按钮
        self.closeBtn = self.button(self.Close)  # 获取关闭按钮
        self.closeBtn.setText('关闭(%s)' % count)
        self._timer = QTimer(self, timeout=self.doCountDown)
        self._timer.start(1000)

    def doCountDown(self):
        self.closeBtn.setText('关闭(%s)' % self.count)
        self.count -= 1
        if self.count <= 0:
            self._timer.stop()
            self.accept()
            self.close()

def mes_about(parent,message):
    MessageBox(parent, text=message).exec_()
    # QMessageBox.about(parent, '明州体检', message)

def mes_warn(parent,message):
    button = QMessageBox.warning(parent,"明州体检", message,QMessageBox.Yes | QMessageBox.No)
    return button

# def mes_about(parent,message):
#     MessageBox(self, text=mes).exec_()
#     QMessageBox.about(parent, '明州体检', message)

# 自带检索按钮、清除按钮
class SearchLineEdit(QLineEdit):

    searchTextChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SearchLineEdit,self).__init__(parent)
        # 绑定信号槽
        self.clearButton.clicked.connect(self.clear)
        self.textChanged.connect(self.updateSearchText)

    def initUI(self):
        # 检索的文本
        self.searchText = ""
        # 清除按钮
        self.clearButton = QToolButton(self)
        self.clearButton.setIcon(Icon('清除'))
        self.clearButton.setCursor(Qt.ArrowCursor)
        self.clearButton.setStyleSheet("QToolButton { border: none; padding: 0px; }")
        self.clearButton.hide()
        # 检索按钮
        self.searchButton = QToolButton(self)
        self.searchButton.setIcon(Icon('查询'))
        self.searchButton.setStyleSheet("QToolButton { border: none; padding: 0px; }")

        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        buttonWidth = self.clearButton.sizeHint().width()
        self.setStyleSheet("QLineEdit { padding-left: %spx; padding-right: %spx; } " % (self.searchButton.sizeHint().width() + frameWidth + 1, buttonWidth + frameWidth + 1))
        msz = self.minimumSizeHint()
        self.setMinimumSize(max(msz.width(),self.searchButton.sizeHint().width() + buttonWidth + frameWidth * 2 + 2),
                            max(msz.height(), self.clearButton.sizeHint().height() + frameWidth * 2 + 2))
        self.setPlaceholderText("Search")
        # 设置快捷方式
        # focusShortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        # focusShortcut.activated.connect(self.setFocus)

    def resizeEvent(self, event):
        sz = self.clearButton.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.clearButton.move(self.rect().right() - frameWidth - sz.width(),(self.rect().bottom() + 1 - sz.height()) / 2)
        self.searchButton.move(self.rect().left() + 1, (self.rect().bottom() + 1 - sz.height()) / 2)

    def getSearchText(self):
        return self.searchText

    def updateSearchText(self, searchText):
        self.searchText = searchText
        self.searchTextChanged.emit(searchText)
        self.updateCloseButton(bool(searchText))

    def updateCloseButton(self, visible):
        self.clearButton.setVisible(visible)

class ToolButton(QToolButton):

    def __init__(self,icon,name):
        super(ToolButton,self).__init__()
        # self.setObjectName('toolB')
        self.setIcon(icon)
        self.setText(name)
        self.setIconSize(QSize(32,32))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setAutoRaise(True)

# 第一列加选择框
    # for(int i = 0; i < 10; ++i)
    # {
    #     QStandardItem *item = new QStandardItem();
    #     item->setCheckable(true);
    #     item->setCheckState(Qt::Unchecked);
    #     m_pModel->setItem(i, 0, item);
    # }

# 基础方法：
# self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch) #第二列扩展
class TableWidget(QTableWidget):

    def __init__(self,heads:dict,parent=None):
        super(TableWidget,self).__init__(parent)
        # 基本设置
        self.setShowGrid(True)
        self.setSortingEnabled(True)            # 字符串排序功能
        self.setFrameShape(QFrame.NoFrame)      # 设置无边框
        self.verticalHeader().setVisible(False)  # 列表头
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)   # 表格内容不能编辑
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选中一行
        self.setAlternatingRowColors(True)                       # 使用行交替颜色
        # 添加行头 必须先设置 setColumnCount
        self.setColumnCount(len(heads))
        self.setHorizontalHeaderLabels(heads.values())
        # self.horizontalHeader().setStyleSheet("QHeaderView::section{background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0.5 #054874 stop:1 #377277);}")  #设置表头背景色
        self.heads = heads
        self.setStyleSheet("QTableCornerButton::section{background-color:white;}")

        # 公共实现，载入数据
    def load(self,datas:list,heads=None):
        self.setSortingEnabled(False) #查询前，关闭排序，避免显示空白，BUG
        if not heads:
            heads = self.heads
            # 保留原来的行，清空内容
            self.clearContents()
        else:
            # 连行头一起清空
            self.clear()
        self.setRowCount(0)  # 清空行
        self.setColumnCount(len(heads))
        self.setHorizontalHeaderLabels(heads.values())  # 行表头

        # 具体实现逻辑
        self.load_set(datas,heads)
        # 恢复公共设置
        self.setSortingEnabled(True)  # 查询后设置True，开启排序
        # self.resizeColumnsToContents()  # 设置列适应大小    按需加，不要

    # 子控件 继承具体实现
    def load_set(self,datas,head):
        pass

    # 已经选择的行
    def isSelectRows(self):
        rows = []
        for item in self.selectedItems():
           if item.row() not in rows:
               rows.append(item.row())
        return rows

    # 获取已选择行的关键字的值
    def isSelectRowsValue(self,key):
        tmp = []
        for row in self.isSelectRows():
            tmp.append(self.getItemValueOfKey(row,key))
        return tmp

    # 插入一行 实现
    def insert(self,data):
        self.insertRow(self.rowCount())  # 特别含义
        if isinstance(data,dict):
            for col_index, col_name in enumerate(self.heads.keys()):
                item = QTableWidgetItem(data[col_name])
                self.setItem(self.rowCount()-1, col_index, item)
        elif isinstance(data,list):
            for col_index,col_value in enumerate(data):
                item = QTableWidgetItem(col_value)
                self.setItem(self.rowCount()-1, col_index, item)
        else:
            mes_about(self,'数据格式要求：dict或者list！')
        # self.resizeColumnsToContents()  # 设置列适应大小

    # 获取某行最后一列值
    def getLastItemValue(self,row:int):
        return self.item(row,self.columnCount()-1).text()

    #获取某行某列值
    def getItemValue(self,row:int,col:int):
        return self.item(row,col).text()

    def getLastCol(self):
        return len(self.heads)-1

    # 根据key 获取某行列的值
    def getItemValueOfKey(self,row:int,key:str):
        col = list(self.heads.keys()).index(key)
        return self.getItemValue(row,col)

    # 根据key 获取某行列的值
    def setItemValueOfKey(self,row:int,key:str,value:str,color=None):
        col = list(self.heads.keys()).index(key)
        self.item(row, col).setText(value)
        if color:
            self.item(row, col).setBackground(color)

    # 根据key 获取当前行列的值
    def getCurItemValueOfKey(self,key:str):
        col = list(self.heads.keys()).index(key)
        return self.getItemValue(self.currentRow(),col)

    # 根据key 获取当前行列的值
    def setCurItemValueOfKey(self,key:str,value:str):
        col = list(self.heads.keys()).index(key)
        self.item(self.currentRow(),col).setText(value)

    # 根据key 获取当前行列的值
    def setCurItemOfKey(self,key:str,value:str,color=None):
        col = list(self.heads.keys()).index(key)
        self.item(self.currentRow(),col).setText(value)
        if color:
            self.item(self.currentRow(),col).setBackground(color)

    # 设置列宽
    def setColWidth(self, key, p_int):
        if key in list(self.heads.keys()):
            col = list(self.heads.keys()).index(key)
            self.setColumnWidth(col,p_int)

    # 导出数据，对表格数据聚合
    def export(self):
        if self.rowCount():
            filename=self.setSaveFileName()
            if not filename:
                return
            heads = [self.horizontalHeaderItem(i).text() for i in range(self.columnCount())]
            datas = []
            for i in range(self.rowCount()):
                tmp = {}
                for j in range(self.columnCount()):
                    column_item = self.horizontalHeaderItem(j)
                    if column_item:
                        column = column_item.text()
                        data = self.item(i, j).text()
                        tmp[column] = data
                datas.append(tmp)
            df = pd.DataFrame(data=datas)
            df.to_excel(filename, columns=heads, index=False)
            mes_about(self, "导出完成！")
        else:
            mes_about(self, '没有内容！')

    def setSaveFileName(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "保存文件",
                                                  desktop(),
                                                  "Excel 2007 Files (*.xlsx)",
                                                  options=QFileDialog.DontUseNativeDialog)
        if fileName:
            return '%s.xlsx' % fileName

#隐藏控件的箭头按钮 左右
class ArrowButton(QPushButton):

    def __init__(self,name,parent=None):
        super(ArrowButton,self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setIcon(Icon(name))
        self.setFixedWidth(6)
        self.setMinimumWidth(6)
        self.setMaximumWidth(6)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("background: #E8E8E8; border: none; padding: 0px;")
        self.setObjectName(name)
# 上下
class ArrowButton2(QPushButton):

    def __init__(self,name,parent=None):
        super(ArrowButton2,self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setIcon(Icon(name))
        self.setFixedHeight(6)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("background: #E8E8E8; border: none; padding: 0px;")
        self.setObjectName(name)

class BrowserWidget(QWidget):
    status = False  # 是否被打开

    def __init__(self,parent=None):
        super(BrowserWidget,self).__init__(parent)

    def closeEvent(self, *args, **kwargs):
        self.status = True
        super(BrowserWidget, self).closeEvent(*args, **kwargs)

class UI(QSplitter):

    status = False          #是否被打开
    left_flag = False         #左边按钮，默认朝向左
    right_flag = False      #右边按钮，默认朝向右

    def __init__(self,title):
        super(UI,self).__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(Icon(title))

        self.setOrientation(Qt.Horizontal)
        self.setChildrenCollapsible(True)
        ############################控件区####################################
        self.left_layout=QVBoxLayout()
        self.left_group=QGroupBox()
        self.left_group.setLayout(self.left_layout)
        self.button1 = ArrowButton("left")
        self.middle_layout=QVBoxLayout()
        self.middle_group=QGroupBox()
        self.middle_group.setLayout(self.middle_layout)
        self.button2 = ArrowButton("right")
        self.right_layout=QVBoxLayout()
        self.right_group=QGroupBox()
        self.right_group.setLayout(self.right_layout)
        #########################添加控件##################################
        self.addWidget(self.left_group)
        self.addWidget(self.button1)
        self.addWidget(self.middle_group)
        self.addWidget(self.button2)
        self.addWidget(self.right_group)
        #########################布局######################################
        self.setStretchFactor(0, 2)   #第一个参数代表控件序号，第二个参数0表示不可伸缩，非0可伸缩
        self.setStretchFactor(1, 1)
        self.setStretchFactor(2, 6)
        self.setStretchFactor(3, 1)
        self.setStretchFactor(4, 5)
        ##########################自身样式########################################
        self.setHandleWidth(0)
        self.setMinimumWidth(6)
        self.setChildrenCollapsible(False)  # 控件调整成过小时是否会隐藏
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("QSplitter.handle{background:lightgray}")

        #信号按照其objectName连接到相应的槽上
        QMetaObject.connectSlotsByName(self)

    @pyqtSlot()
    def on_left_clicked(self):
        #箭头向右
        if self.left_flag:
            self.left_flag = False
            self.button1.setIcon(Icon("left"))
            self.left_group.setVisible(True)

        else:
            self.left_flag = True
            self.button1.setIcon(Icon("right"))
            self.left_group.setVisible(False)

    @pyqtSlot()
    def on_right_clicked(self):
        #箭头向右
        if self.right_flag:
            self.right_flag = False
            self.button2.setIcon(Icon("right"))
            self.right_group.setVisible(True)
        else:
            self.right_flag = True
            self.button2.setIcon(Icon("left"))
            self.right_group.setVisible(False)

    def closeEvent(self, *args, **kwargs):
        self.status = True
        super(UI, self).closeEvent(*args, **kwargs)


class TabWidget(QTabWidget):

    status = False            #是否被打开

    widget_queue = {}         # 控件队列 打开过的不允许新增

    def __init__(self,parent=None,lb_is_close = True):
        super(TabWidget, self).__init__(parent)
        self.setTabsClosable(lb_is_close)  # 关闭标签
        self.setMovable(True)       #tab可移动
        self.setMouseTracking(True)
        self.tabCloseRequested.connect(self.dropTab)

    def dropTab(self,index):
        self.removeTab(index)
        try:
            if not self.count():
                if self.parentWidget():
                    self.parentWidget().showTab()
        except Exception as e:
            print(e)

    def closeEvent(self, *args, **kwargs):
        self.status = True
        super(TabWidget, self).closeEvent(*args, **kwargs)

    def addPage(self, QWidget, QIcon, title):
        self.addTab(QWidget, QIcon, title)
        self.setCurrentWidget(QWidget)
        # widget = self.widget_queue.get(title,0)
        # if not widget:
        #     self.addTab(QWidget, QIcon, title)
        #     self.setCurrentWidget(QWidget)
        #     self.widget_queue[title] = QWidget
        # else:
        #     self.setCurrentWidget(widget)

class TreeWidget(QTreeWidget):

    def __init__(self,parent,titles):
        '''
        :param parent: 父窗口
        :param titles: 树节点标题
        '''
        super(TreeWidget,self).__init__(parent)
        self.parent=parent
        self.setHeaderHidden(True)                      #隐藏头部
        for title in titles:
            item = QTreeWidgetItem(self)
            item.setText(0,title)
            item.setIcon(0,Icon(title))
            item.setToolTip(0,title)

        itemStyle = '''font: 75 12pt \"微软雅黑\";'''
        self.setStyleSheet(itemStyle)

        self.itemDoubleClicked.connect(self.double_clicked_event)

    def double_clicked_event(self):
        title=self.currentItem().text(self.currentColumn())
        self.parent.addTab(title)

class PhotoUI(QLabel):

    def __init__(self,show_x=320,show_y=240,select_x=105,select_y=129,capture=0,fps=24):
        '''
        :param show_x:
        :param show_y:
        :param select_x:
        :param select_y:
        :param capture:
        :param fps:
        '''
        super(PhotoUI, self).__init__()
        self.resize(show_x,show_y)
        self.show_size=[show_x,show_y]
        self.mouse_x = show_x/2                #鼠标位置，初始化，控件大小中心
        self.mouse_y = show_y/2                #鼠标位置，初始化，控件大小中心
        self.sel_size= [select_x,select_y]
        self.select_x  = select_x/2
        self.select_y  = select_y/2

        self.setScaledContents(1)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onMenu)
        self.fps = fps
        self.cap = cv2.VideoCapture(capture)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, show_x)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, show_y)
        self.start()

    def start(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.onCapture)
        self.timer.start(1000 / self.fps)

    def onCapture(self):
        if self.cap.isOpened():
            ret,frame = self.cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
            self.setPixmap(QPixmap.fromImage(img,Qt.AutoColor))
        else:
            self.setText('打开失败，请检查配置！')
            self.setStyleSheet('''font: 75 14pt '黑体';color: rgb(204, 0, 0);''')

    def deleteLater(self):
        self.cap.release()
        super(PhotoUI, self).deleteLater()


    def onMenu(self,pos):
        menu = QMenu()
        item1 = menu.addAction(Icon("拍照"),"拍照")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == item1:
            ret,frame = self.cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
            xx=img.copy(self.mouse_x-self.select_x, self.mouse_y-self.select_y, self.sel_size[0], self.sel_size[1])
            xx.save("./tmp/temp.bmp" )



    def onTakeImage(self,name):
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
        xx = img.copy(self.mouse_x - self.select_x, self.mouse_y - self.select_y, self.sel_size[0], self.sel_size[1])
        xx.save(name)
        return xx

    def mouseMoveEvent(self, QMouseEvent):
        self.setMouseTracking(True)                         # 鼠标形状变化
        super(PhotoUI, self).mouseMoveEvent(QMouseEvent)
        pos = QMouseEvent.pos()
        self.mouse_x = pos.x()
        self.mouse_y = pos.y()

    def paintEvent(self, QPaintEvent):
        # 绘制工作在paintEvent的方法内部完成
        # 先绘制父对象内容，
        super(PhotoUI,self).paintEvent(QPaintEvent)
        # 再绘制自身
        painter = QPainter(self)
        # QPainter负责所有的绘制工作:在它的begin()与end()间放置了绘图代码。
        # 实际的绘制工作由drawText()方法完成。
        painter.begin(self)
        self.drawText(QPaintEvent, painter)
        painter.end()

    def drawText(self, event, painter):
        # 反走样
        painter.setRenderHint(QPainter.Antialiasing, True)
        # 设置画笔颜色、宽度
        painter.setPen(QPen(QColor(0, 160, 230), 2))
        # 设置画刷颜色
        #painter.setBrush(QColor(255, 160, 90))
        # 3*3 象限 ,不出边界
        # 实际选择区域左上角定点画出的是一个矩形，可以改进
        if self.mouse_x-self.select_x<=0:
            if self.mouse_y - self.select_y<=0:
                painter.drawRect(0, 0, self.sel_size[0], self.sel_size[1])
            elif 0<self.mouse_y - self.select_y<self.show_size[1]-self.sel_size[1]:
                painter.drawRect(0, self.mouse_y - self.select_y, self.sel_size[0], self.sel_size[1])
            else:
                painter.drawRect(0, self.show_size[1]-self.sel_size[1], self.sel_size[0], self.sel_size[1])
        elif 0<self.mouse_x-self.select_x<self.show_size[0]-self.sel_size[0]:
            if self.mouse_y - self.select_y<=0:
                painter.drawRect(self.mouse_x-self.select_x, 0, self.sel_size[0], self.sel_size[1])
            elif 0 < self.mouse_y - self.select_y < self.show_size[1]-self.sel_size[1]:
                painter.drawRect(self.mouse_x - self.select_x, self.mouse_y - self.select_y, self.sel_size[0], self.sel_size[1])
            else:
                painter.drawRect(self.mouse_x-self.select_x, self.show_size[1]-self.sel_size[1], self.sel_size[0],self.sel_size[1])
        else:
            if self.mouse_y - self.select_y <= 0:
                painter.drawRect(self.show_size[0] - self.sel_size[0], 0, self.sel_size[0],self.sel_size[1])
            elif 0 < self.mouse_y - self.select_y < self.show_size[1]-self.sel_size[1]:
                painter.drawRect(self.show_size[0]-self.sel_size[0], self.mouse_y - self.select_y, self.sel_size[0],self.sel_size[1])
            else:
                painter.drawRect(self.show_size[0] - self.sel_size[0], self.show_size[1]-self.sel_size[1], self.sel_size[0],self.sel_size[1])

# 摄像头
class CameraUI(QLabel):

    def __init__(self,show_x=320,show_y=240,capture=0,fps=24):
        super(CameraUI, self).__init__()
        self.resize(show_x,show_y)
        self.setScaledContents(1)
        self.fps = fps
        self.cap = cv2.VideoCapture(capture)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, show_x)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, show_y)
        self.start()

    def start(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.onCapture)
        self.timer.start(1000 / self.fps)

    def onCapture(self):
        if self.cap.isOpened():
            ret,frame = self.cap.read()
            try:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                ##############处理旋转#####################################
                # rows,cols,count = frame.shape
                # M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 270, 1)
                # frame = cv2.warpAffine(frame, M, (cols, rows))
                img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
                self.setPixmap(QPixmap.fromImage(img,Qt.AutoColor))
            except Exception as e:
                mes_about(self,'类：CameraUI.onCapture() 执行出错！错误信息：%s' %e)
                self.timer.stop()
                #return
        else:
            self.setText('打开失败，请检查配置！')
            self.setStyleSheet('''font: 75 14pt '黑体';color: rgb(204, 0, 0);''')

    def onTakeImage(self,name):
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
        img.save(name)
        return img

    def deleteLater(self):
        self.timer.stop()
        self.cap.release()
        super(CameraUI, self).deleteLater()


# 文档打印功能
class Printer(object):

    def __init__(self):
        self.printerInfo = QPrinterInfo()

    def all(self):
        return self.printerInfo.availablePrinterNames()

    def default(self):
        return self.printerInfo.defaultPrinterName()

# 右下角弹窗 -- 不适用 主窗口界面下弹窗
class PopupWidget(QWidget):

    def __init__(self,title:str,mes:str,times=5):
        '''

        :param mes:消息内容
        :param times:定时时间
        '''
        super(PopupWidget,self).__init__()
        self.title = title
        self.mes = mes
        self.times = times
        self.setWindowTitle('%s ( %s秒后关闭)' % (self.title, self.times))
        self.desktop = QDesktopWidget()
        self.setFixedHeight(200)
        self.setFixedWidth(300)
        self.move((self.desktop.availableGeometry().width()-self.width()-20),
                  self.desktop.availableGeometry().height()-self.height()-100)  # 初始化位置到右下角

        self.showAnimation()
        self.show()

    # 弹出动画
    def showAnimation(self):
        # 显示弹出框动画
        self.animation = QPropertyAnimation(self)
        #self.animation.setDuration(1000)
        self.animation.setStartValue(QPoint(self.x(), self.y()))
        self.animation.setEndValue(QPoint((self.desktop.availableGeometry().width() - self.width()), (
        self.desktop.availableGeometry().height() - self.height() )))
        self.animation.start()

        # 设置弹出框1秒弹出，然后渐隐
        self.remainTimer = QTimer()
        self.remainTimer.timeout.connect(self.closeAnimation)
        self.remainTimer.start(1000)  # 定时器10秒

    # 关闭动画
    @pyqtSlot()
    def closeAnimation(self):
        self.times = self.times - 1
        if self.times > 0:
            self.setWindowTitle('%s ( %s秒后自动关闭)' %(self.title,self.times))
            print(11111)
            return
        # 清除Timer和信号槽
        self.remainTimer.stop()
        self.remainTimer.timeout.disconnect(self.closeAnimation)
        # self.disconnect(self.remainTimer, SIGNAL("timeout()"), self, SLOT("closeAnimation()"))
        self.remainTimer.deleteLater()
        self.remainTimer = None
        # 弹出框渐隐
        self.animation = QPropertyAnimation(self, "windowOpacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()
        # 动画完成后清理
        self.animation.finished.connect(self.clearAll)
        #self.connect(self.animation, SIGNAL("finished()"), self, SLOT("clearAll()"))

    # 清理及退出
    @pyqtSlot()
    def clearAll(self):
        self.animation.finished.disconnect(self.clearAll)
        #self.disconnect(self.animation, SIGNAL("finished()"), self, SLOT("clearAll()"))
        self.close()


# 弹出框

class PreviewWidget(QWidget):

    def __init__(self,mes,times=6):
        super(PreviewWidget, self).__init__()
        self.mes =mes
        self.times =times
        self.initUI()

        #定时器
        self.ptimer = QTimer(self)
        self.ptimer.start(1000)
        self.ptimer.timeout.connect(self.on_time_show)


    def initUI(self):
        self.title = '明州体检'
        self.setWindowIcon(Icon('mztj'))
        lt_main = QHBoxLayout()
        lb_mes = QTextBrowser()
        lb_mes.setText(self.mes)
        lb_style = '''color: rgb(255, 0, 0);font: 75 16pt "微软雅黑";'''
        lb_mes.setStyleSheet(lb_style)
        lt_main.addWidget(lb_mes)
        self.setLayout(lt_main)
        # 移动位置
        desktop = QDesktopWidget()
        self.setFixedHeight(200)
        self.setFixedWidth(300)
        self.move((desktop.availableGeometry().width()-self.width()-20),
                  desktop.availableGeometry().height()-self.height()-60)  # 初始化位置到右下角
        # 设置标题
        self.setWindowTitle('%s (%s秒后自动关闭)' % (self.title, self.times))
        # 显示
        self.show()


    def on_time_show(self):
        self.times = self.times - 1
        if self.times > 0:
            self.setWindowTitle('%s ( %s秒后自动关闭)' %(self.title,self.times))
            return

        # 清除Timer和信号槽
        self.ptimer.stop()
        self.ptimer.timeout.disconnect(self.on_time_show)
        self.ptimer.deleteLater()
        self.ptimer = None

        self.close()


# 一个有信号槽机制的安全线程队列。
class QueueObject(QObject):

    add = pyqtSignal()

    def __init__(self):
        super(QueueObject, self).__init__()
        self.queue = Queue()

    def put(self, data):
        self.queue.put(data)
        self.add.emit()

    def get(self):
        if self.queue.empty():
            return 0

        return self.queue.get()



class SearchLineEdit2(QLineEdit):
    """创建一个可自定义图片的输入框。"""

    style = '''
            QPushButton {
            border-image: url(resource/search.png);
        }
        
        QLineEdit#SearchLine{
            margin-bottom: 1px;
            border: 4px solid #171719;
            border-radius: 10px;
            color: #555555;
            font: 75 9pt "黑体";
            background: #171719;
        }
        
        QLineEdit#SearchLine:pressed {
            color: #D0D0D1;
        }
    '''

    def __init__(self, parent=None):
        super(SearchLineEdit2, self).__init__(parent)
        self.setMinimumSize(218, 20)
        # with open('QSS/searchLine.qss', 'r') as f:
        self.setStyleSheet(self.style)

        self.button = QPushButton(self)
        self.button.setMaximumSize(13, 13)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))

        self.setTextMargins(3, 0, 19, 0)

        self.spaceItem = QSpacerItem(150, 10, QSizePolicy.Expanding)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addSpacerItem(self.spaceItem)
        # self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.button)
        self.mainLayout.addSpacing(10)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

    def setButtonSlot(self, funcName):
        self.button.clicked.connect(funcName)


# 头像标题
class HeadLabel(QLabel):

    def __init__(self, *args, antialiasing=True, **kwargs):
        super(HeadLabel, self).__init__(*args, **kwargs)
        self.Antialiasing = antialiasing
        self.setMaximumSize(200, 200)
        self.setMinimumSize(200, 200)
        self.radius = 100

        #####################核心实现#########################
        self.target = QPixmap(self.size())  # 大小和控件一样
        self.target.fill(Qt.transparent)  # 填充背景为透明
        # 加载图片并缩放和控件一样大
        p = QPixmap("head.jpg").scaled(200, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        painter = QPainter(self.target)
        if self.Antialiasing:
            # 抗锯齿
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

#         painter.setPen(# 测试圆圈
#             QPen(Qt.red, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)
        #**** 切割为圆形 ****#
        painter.setClipPath(path)
#         painter.drawPath(path)  # 测试圆圈

        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)
        #####################核心实现#########################


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.addWidget(HeadLabel(self))
        layout.addWidget(HeadLabel(self, antialiasing=False))
        self.setStyleSheet("background: black;")

# 流水布局，自动换行
class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margin, _, _, _ = self.getContentsMargins()

        size += QSize(2 * margin, 2 * margin)
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()

# 右下角弹出框 剥离业务
class PopWidget(QDialog):

    def __init__(self,parent=None,size=(300,400)):
        super(PopWidget, self).__init__(parent)
        self.setWindowIcon(Icon('mztj'))
        # 移动整体位置
        desktop = QDesktopWidget()
        self.setFixedHeight(size[0])
        self.setFixedWidth(size[1])
        self.move((desktop.availableGeometry().width()-self.width()-20),
                  desktop.availableGeometry().height()-self.height()-60)  # 初始化位置到右下角
        # #定时器
        # self.ptimer = QTimer(self)

    def on_time_start(self,title,times=10):
        # self.times=times
        # self.title = title
        # 设置标题
        self.setWindowTitle('%s' % title)
        # self.ptimer.start(1000)
        # self.ptimer.timeout.connect(self.on_time_show)

    # def on_time_show(self):
    #     self.times = self.times - 1
    #     if self.times > 0:
    #         self.setWindowTitle('%s (%s秒后关闭)' %(self.title,self.times))
    #         return
    #     # 清除Timer和信号槽
    #     self.ptimer.stop()
    #     self.ptimer.timeout.disconnect(self.on_time_show)
    #     # self.ptimer.deleteLater()
    #     # self.ptimer = None
    #     self.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     import sys
#     app = QApplication(sys.argv)
#     ui = PreviewWidget('111','11111')
#     ui.show()
#     app.exec_()