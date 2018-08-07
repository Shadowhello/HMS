from widgets.bwidget import *
from utils.readparas import GolParasMixin,GolParasMixin2
from utils.base import str2
from functools import partial
from utils.readcard import IdCard

# 加粗字体
def get_font():
    font = QFont()
    font.setBold(True)
    font.setWeight(75)
    return font

# 定制化组件
class Lable(QLabel):

    def __init__(self):
        super(Lable,self).__init__()
        self.setMinimumWidth(75)
        self.setStyleSheet('''font: 75 11pt '黑体';color: rgb(0, 85, 255);''')

# 身份证字体 绝对定位
class IdCardLable(QLabel):

    def __init__(self,parent,left:int,top:int, width:int, height:int):
        super(IdCardLable,self).__init__(parent)
        self.setGeometry(QRect(left,top, width, height))
        self.setStyleSheet('''font: 75 14pt \"微软雅黑\";color: rgb(255, 0, 0);''')

class IdCardLable2(QTextEdit):
    def __init__(self,parent,left:int,top:int, width:int, height:int):
        super(IdCardLable2,self).__init__(parent)
        self.setGeometry(QRect(left,top, width, height))
        self.setStyleSheet('''font: 75 14pt \"微软雅黑\";color: rgb(255, 0, 0);''')


# 窗口带日志、登录信息、数据库链接功能
class Widget(GolParasMixin,QWidget):

    def __init__(self,parent=None):
        super(Widget,self).__init__(parent)
        self.init()

# 窗口带日志、登录信息、数据库链接功能
class Dialog(GolParasMixin, QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.init()

# 窗口带日志、登录信息、数据库链接功能
class PacsWidget(GolParasMixin2, QWidget):
    def __init__(self, parent=None):
        super(PacsWidget, self).__init__(parent)
        self.init()

# 体检编号
class QTJBH(QLineEdit):

    def __init__(self,parent=None):
        super(QTJBH,self).__init__(parent)

        self.setPlaceholderText("输体检编号回车")
        regx=QRegExp("[0-9]+$")
        validator=QRegExpValidator(regx,self)
        self.setValidator(validator)              #根据正则做限制，只能输入数字

        # self.returnPressed.connect(self.validate)

    def validate(self):
        print(self.text())
        if len(self.text())!=9:
            mes_about(self, "体检编号：%s不是9位，请重新输入！" %self.text())
            self.setText('')

# 体检姓名
class QXM(QLineEdit):

    def __init__(self, parent=None):
        super(QXM, self).__init__(parent)

        self.setPlaceholderText("输姓名回车，支持模糊匹配")
        # regx = QRegExp("[0-9]+$")
        # validator = QRegExpValidator(regx, self)
        # self.setValidator(validator)  # 根据正则做限制，只能输入数字

# 手机号码
class QSJHM(QLineEdit):

    def __init__(self, parent=None):
        super(QSJHM, self).__init__(parent)

        self.setPlaceholderText("输手机号码回车")
        regx = QRegExp("[0-9]+$")
        validator = QRegExpValidator(regx, self)
        self.setValidator(validator)  # 根据正则做限制，只能输入数字

        self.returnPressed.connect(self.validate)

    def validate(self):
        pass

# 身份证号
class QSFZH(QLineEdit):

    def __init__(self, parent=None):
        super(QSFZH, self).__init__(parent)

        self.setPlaceholderText("输入身份证号回车，支持读卡")
        regx = QRegExp("[0-9]+$")
        validator = QRegExpValidator(regx, self)
        self.setValidator(validator)  # 根据正则做限制，只能输入数字

        self.returnPressed.connect(self.validate)

    def validate(self):
        pass

# 序列号：体检编号/条码号均可以
class QSerialNo(QLineEdit):

    def __init__(self,parent=None):
        super(QSerialNo,self).__init__(parent)
        self.setPlaceholderText("扫描体检编号/条码号即可")
        regx=QRegExp("[0-9]+$")
        validator=QRegExpValidator(regx,self)
        self.setValidator(validator)              #根据正则做限制，只能输入数字

class SerialNoButton(QToolButton):

    int_x = 0
    int_y = 0
    collect_cancle = False  # 样本拒检状态，默认未拒检  True 拒检
    collect_state = False   # 样本采集状态，默认未采集  True 采集
    collect_type = False    # 样本采集类型，默认抽血样本  True 留样
    collect_tjbh = ''       # 样本采集编号，即体检编号
    collect_no = ''         # 样本采集编号，即条码号
    collect_txt = ''        # 样本采集文本，即条码上项目名称
    collect_color = ''      # 样本采集颜色，

    def __init__(self,icon,name):
        super(SerialNoButton,self).__init__()
        self.initUI(icon,name)

    def initUI(self,icon,name):
        self.setIcon(Icon(icon))
        self.setIconSize(QSize(150,66))
        self.setToolTip(name)
        self.collect_txt = name
        self.ab(name)
        self.setMinimumWidth(152)
        self.setMinimumHeight(72)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setAutoRaise(True)

    # 设置本按钮采集状态
    def setCollectState(self,state=False):
        self.collect_state = state

    # 获取采集状态
    @property
    def collectState(self):
        return self.collect_state

    # 设置按钮拒检状态
    def setCollectCancle(self,state=False):
        self.collect_cancle = state

    # 获取采集状态
    @property
    def collectCancle(self):
        return self.collect_cancle

    # 设置本按钮采集类型
    def setCollectType(self, ctype=False):
        self.collect_type = ctype

    # 获取采集类型
    @property
    def collectType(self):
        return self.collect_type

    #设置采集 条码编号
    def setCollectNo(self,number:str):
        self.collect_no = number

    #获取采集 条码编号
    @property
    def collectNo(self):
        return self.collect_no

    #设置采集 体检编号
    def setCollectTJBH(self,number:str):
        self.collect_tjbh = number

    #获取采集 体检编号
    @property
    def collectTJBH(self):
        return self.collect_tjbh

    # 设置采集位置
    def setCollectPos(self, int_p1,int_p2):
        self.int_x = int_p1
        self.int_y = int_p2

    # 获取采集坐标 X
    @property
    def collectPos_X(self):
        return self.int_x

    # 获取采集坐标 Y
    @property
    def collectPos_Y(self):
        return self.int_y

    # 获取采集文本名称
    @property
    def collectTxt(self):
        return self.collect_txt

    # 缩写
    def ab(self,p_text):
        if len(p_text)<8:
            self.setText(p_text)
        else:
            self.setText("%s..." %p_text[0:8])

    #设置管子颜色
    def setCollectColor(self,color:str):
        self.collect_color = color

    @property
    def collectColor(self):
        return self.collect_color

# C13/14 项目对象(同一类对象同时存在且需要不同状态)
class C13Item(object):

    def __init__(self,tjbh,data=None):
        self.tjbh = tjbh            # 体检编号
        self.data = None            # 数据                # 解决乱码问题
        self.state = 1              # 状态：1,2,3,4
        self.simpleNo = None        # 样本号：对应吹气试纸

    def setData(self,data:dict):
        self.data = data

    def getData(self):
        return self.data

    def setState(self,state):
        self.state = state

    def getState(self):
        return self.state

    # 设置样本编号
    def setSimpleNo(self,sno):
        self.simpleNo = sno

    def getSimpleNo(self):
        return self.simpleNo

# C13/14 呼气试验 搜索列表
class C13InspectTable(TableWidget):

    # 自定义信号：删除项目信号  体检编号+区域：生成样本号
    itemDroped = pyqtSignal(list)

    def __init__(self, heads, parent=None):
        super(C13InspectTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(row_index)
            for col_index, col_value in enumerate(row_data):
                item = QTableWidgetItem(str2(col_value))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

        self.setColumnWidth(0, 70)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 30)
        self.setColumnWidth(3, 30)
        self.horizontalHeader().setStretchLastSection(True)

    # 插入到 吹气列表
    def insert2(self,data):
        self.insertRow(self.rowCount())
        for col_index, col_value in enumerate(data):
            if col_index== 6 :
                lb_timer = TimerLabel()
                lb_timer.timer_out.connect(partial(self.dropRow,data))     # 必须传递唯一的值
                self.setCellWidget(self.rowCount()-1,col_index,lb_timer)
            else:
                item = QTableWidgetItem(col_value)
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(self.rowCount() - 1, col_index, item)

        self.horizontalHeader().setStretchLastSection(True)

    # 插入到完成列表
    def insert3(self,data):
        self.insertRow(self.rowCount())
        for col_index, col_value in enumerate(data):
            item = QTableWidgetItem(col_value)
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(self.rowCount() - 1, col_index, item)

        self.horizontalHeader().setStretchLastSection(True)

    # 增量增加，不清除原来的数据
    def insertMany(self,datas):
        # old_row = self.rowCount()
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(self.rowCount())
            for col_index, col_value in enumerate(row_data):
                item = QTableWidgetItem(str2(col_value))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(self.rowCount() - 1, col_index, item)

        self.setColumnWidth(0, 70)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 60)
        self.setColumnWidth(3, 30)
        self.setColumnWidth(4, 30)
        self.horizontalHeader().setStretchLastSection(True)

    # 删除行
    def dropRow(self,data:list):
        tjbh = data[0]
        items = self.findItems(tjbh, Qt.MatchContains)
        for item in items:
            p_tjbh = self.item(item.row(), 0).text()
            self.removeRow(item.row())
            self.itemDroped.emit(data)


# 设备接口检查列表
class EquipInspectTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(EquipInspectTable, self).__init__(heads, parent)

    # 插入一行 实现
    def insert2(self,data:dict):
        self.insertRow(self.rowCount())  # 特别含义
        for col_index, col_name in enumerate(self.heads.keys()):
            item = QTableWidgetItem(data[col_name])
            if col_index ==0 and data[col_name]=='检查中':
                item.setBackground(QColor("#ff8c00"))               # 橘黄色

            self.setItem(self.rowCount() - 1, col_index, item)

        self.resizeColumnsToContents()  # 设置列适应大小

# 设备结果列表，追踪处用
class EquipResultTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(EquipResultTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # list 实现
        pass

# PACS检查列表
class PacsInspectResultTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(PacsInspectResultTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(row_index)
            for col_index, col_value in enumerate(row_data):
                if col_index == 0:
                    if col_value == '已审核':
                        item = QTableWidgetItem('已审核')
                    else:
                        item = QTableWidgetItem(col_value)
                        item.setBackground(QColor("#FF0000"))
                else:
                    if col_value:
                        item = QTableWidgetItem(str(col_value))
                        item.setTextAlignment(Qt.AlignCenter)
                    else:
                        item = QTableWidgetItem('')

                self.setItem(row_index, col_index, item)

# PIS检查列表
class PisInspectResultTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(PisInspectResultTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(row_index)
            for col_index, col_value in enumerate(row_data):
                if col_value:
                    item = QTableWidgetItem(str2(col_value))
                    item.setTextAlignment(Qt.AlignCenter)
                else:
                    item = QTableWidgetItem('')
                self.setItem(row_index, col_index, item)

# LIS检查列表 总列表
class MLisInspectResultTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(MLisInspectResultTable, self).__init__(heads, parent)

    def load_set(self, datas, heads=None):
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(row_index)
            for col_index, col_value in enumerate(row_data):
                if col_index == 0:
                    if col_value == '1':
                        item = QTableWidgetItem('已审核')
                    else:
                        item = QTableWidgetItem('未审核')
                        item.setBackground(QColor("#FF0000"))
                elif col_index == 2:
                    item = QTableWidgetItem(col_value)
                else:
                    item = QTableWidgetItem(str2(col_value))
                self.setItem(row_index, col_index, item)

        self.resizeColumnsToContents()  # 设置列适应大小

# LIS检查列表 结果详细列表
class DLisInspectResultTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(DLisInspectResultTable, self).__init__(heads, parent)

    def load_set(self, datas, heads=None):
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(row_index)
            if row_data[3]:
                for col_index, col_value in enumerate(row_data):
                    item = QTableWidgetItem(str2(col_value))
                    item.setBackground(QColor("#FF0000"))
                    self.setItem(row_index, col_index, item)
            else:
                for col_index, col_value in enumerate(row_data):
                    item = QTableWidgetItem(str2(col_value))
                    self.setItem(row_index, col_index, item)
        # self.resizeColumnsToContents()  # 设置列适应大小
        self.setColumnWidth(0, 70)
        self.setColumnWidth(1, 70)
        self.setColumnWidth(2, 70)
        self.setColumnWidth(3, 70)
        self.setColumnWidth(4, 70)
        self.setColumnWidth(5, 70)
        self.horizontalHeader().setStretchLastSection(True)

# 抽血历史采集筛选列表
class CollectHistoryTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(CollectHistoryTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):

        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)                # 插入一行
            for col_index, col_name in enumerate(heads.keys()):
                data = row_data.get(col_name,'')
                if col_name=='ck':
                    item = QTableWidgetItem('查看')
                    font = QFont()
                    font.setBold(True)
                    font.setWeight(75)
                    item.setFont(font)
                    item.setBackground(QColor(218,218,218))
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled )
                else:
                    item = QTableWidgetItem(data)

                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

# 抽血交接记录表 汇总
class CollectHandoverTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(CollectHandoverTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):

        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)  # 插入一行
            for col_index, col_value in enumerate(row_data):
                item = QTableWidgetItem(str2(col_value))

                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

        self.setColumnWidth(0, 70)
        self.setColumnWidth(1, 70)
        self.setColumnWidth(4, 50)

# 抽血交接记录表 详细
class CollectHandoverDTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(CollectHandoverDTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):

        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)  # 插入一行
            for col_index, col_name in enumerate(heads.keys()):
                item = QTableWidgetItem(row_data[col_name])
                if col_index == 5:
                    pass
                else:
                    item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

        self.setColumnWidth(0, 70)
        self.setColumnWidth(1, 70)
        self.setColumnWidth(2, 70)
        self.setColumnWidth(4, 50)


# 抽血历史采集筛选列表
class ItemsStateTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(ItemsStateTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):

        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)                # 插入一行
            for col_index, col_name in enumerate(heads.keys()):
                data = row_data[col_name]
                item = QTableWidgetItem(data)
                if col_index == 0:
                    if data == '已小结':
                        pass
                    elif data in ['已检查','已抽血','已留样']:
                        item.setBackground(QColor("#f0e68c"))
                    elif data == '核实':
                        item.setBackground(QColor("#FF0000"))
                    elif data == '已拒检':
                        item.setBackground(QColor("#008000"))
                    elif data == '已接收':
                        item.setBackground(QColor("#b0c4de"))
                    elif data == '已回写':
                        item.setBackground(QColor("#1e90ff"))
                elif col_index == 4:
                    item = QTableWidgetItem('打印')
                    item.setFont(get_font())
                    item.setBackground(QColor(218, 218, 218))
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                elif col_index == 5:
                    if row_data[list(heads.keys())[0]] in ['已小结','已拒检']:
                        item = QTableWidgetItem('')
                    else:
                        item = QTableWidgetItem('拒检')
                        item.setFont(get_font())
                        item.setBackground(QColor(218, 218, 218))
                        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                elif col_index == 6:
                    if row_data[list(heads.keys())[0]] in ['已小结','已拒检']:
                        item = QTableWidgetItem('')
                    else:
                        item = QTableWidgetItem('核实')
                        item.setFont(get_font())
                        item.setBackground(QColor(218, 218, 218))
                        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)

                self.setItem(row_index, col_index, item)
                # 除第三列 都居中
                if col_index!= 3:
                    item.setTextAlignment(Qt.AlignCenter)

        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True)


# 报告追踪列表
class ReportTrackTable(TableWidget):

    tjqy = None      # 体检区域
    tjlx = None      # 体检类型

    def __init__(self, heads, parent=None):
        super(ReportTrackTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(row_index)
            for col_index, col_value in enumerate(row_data):
                if col_value:
                    if  col_index in [3,7,8,11,12]:
                        item = QTableWidgetItem(col_value)
                    else:
                        item = QTableWidgetItem(str2(col_value))
                    if col_index not in [9,10,12]:
                        item.setTextAlignment(Qt.AlignCenter)
                    # self.resizeColumnToContents()
                else:
                    item = QTableWidgetItem('')
                self.setItem(row_index, col_index, item)

        # 特殊设置
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontalHeader().setMinimumSectionSize(60)
        # self.horizontalHeader().setMaximumSectionSize(300)
        self.horizontalHeader().setStretchLastSection(True)
        # self.horizontalHeader().setResizeMode(QHeaderView.Stretch)



# 慢病疑似筛选列表
class SlowHealthTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(SlowHealthTable, self).__init__(heads,parent)

    # 具体载入逻辑实现
    def load_set(self,datas,heads=None):

        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)                # 插入一行
            for col_index, col_name in enumerate(heads.keys()):
                data = row_data[col_name]
                if col_name in ['is_gxy','is_gxz','is_gxt','is_gns','is_jzx']:
                    if data=='1':
                        item = QTableWidgetItem('√')
                        item.setTextAlignment(Qt.AlignCenter)
                    else:
                        item = QTableWidgetItem('')
                elif col_name in ['glu','glu2','hbalc','ua','tch','tg','hdl','ldl','hbp','lbp']:
                    if data:
                        item = QTableWidgetItem(str(data))
                        if row_data['is_yc_%s' %col_name]:  # 对应列异常
                            item.setBackground(QColor("#FF0000"))
                    else:
                        item = QTableWidgetItem('')
                else:
                    item = QTableWidgetItem(data)

                self.setItem(row_index, col_index, item)


# 检查表格
class CheckTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(CheckTable, self).__init__(heads,parent)

    def rowsHide(self,values:list,cvalue=None):
        '''
        :param values:  如果为空，说明
        :param cvalues:  额外补充的条件，验证用户 思考：如果是多条件如何更通用处理，表头下拉功能
        :return:
        '''
        if not cvalue:
            if values: # 此条件不做判断也可，只是作为优化的选择项
                for row_index in range(self.rowCount()):
                    state = self.item(row_index,0).text()
                    self.setRowHidden(row_index, state in values)
            else:
                for row_index in range(self.rowCount()):
                    if self.isRowHidden(row_index):
                        self.setRowHidden(row_index,False)
        else:
            for row_index in range(self.rowCount()):
                state = self.item(row_index, 0).text()
                jcys = self.item(row_index, 7).text()
                self.setRowHidden(row_index, state in values and jcys==cvalue)


    def load2(self,heads,rows,datas):
        self.clear()
        self.setSortingEnabled(False)  # 避免点击排序造成BUG
        self.setColumnCount(len(heads))
        self.setRowCount(rows)

        self.setHorizontalHeaderLabels(heads.values())  # 行表头
        for row_index, row_data in enumerate(datas):
            # row_data:dict
            for col_index, col_name in enumerate(heads.keys()):
                data=row_data[col_name]
                item = QTableWidgetItem(data)
                if col_index==0:
                    if data=='核实':
                        item.setBackground(QColor("#FFD700"))
                    elif data=='已登记':
                        item.setBackground(QColor("#8B8386"))
                    elif data == '已拒检':
                        item.setBackground(QColor("#00CD00"))
                    elif data == '已检查':
                        item.setBackground(QColor("#008B00"))

                self.setItem(row_index, col_index, item)

        self.resizeColumnsToContents()  # 设置列适应大小

# 检查表格
class BloodTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(BloodTable, self).__init__(heads, parent)

    def rowsHide(self, values: list, cvalue=None):
        '''
        :param values:  如果为空，说明
        :param cvalues:  额外补充的条件，验证用户 思考：如果是多条件如何更通用处理，表头下拉功能
        :return:
        '''
        if not cvalue:
            if values:  # 此条件不做判断也可，只是作为优化的选择项
                for row_index in range(self.rowCount()):
                    state = self.item(row_index, 0).text()
                    self.setRowHidden(row_index, state in values)
            else:
                for row_index in range(self.rowCount()):
                    if self.isRowHidden(row_index):
                        self.setRowHidden(row_index, False)
        else:
            for row_index in range(self.rowCount()):
                state = self.item(row_index, 0).text()
                jcys = self.item(row_index, 7).text()
                self.setRowHidden(row_index, state in values and jcys == cvalue)

    def load2(self, heads, rows, datas):
        self.clear()
        self.setSortingEnabled(False)  # 避免点击排序造成BUG
        self.setColumnCount(len(heads))
        self.setRowCount(rows)

        self.setHorizontalHeaderLabels(heads.values())  # 行表头
        for row_index, row_data in enumerate(datas):
            # row_data:dict
            for col_index, col_name in enumerate(heads.keys()):
                data = row_data[col_name]
                item = QTableWidgetItem(data)
                #if col_index == 0:
                #    if data == '核实':
                #        item.setBackground(QColor("#FFD700"))
                #    elif data == '已登记':
                #        item.setBackground(QColor("#8B8386"))
                #    elif data == '已拒检':
                #        item.setBackground(QColor("#00CD00"))
                #    elif data == '已检查':
                #        item.setBackground(QColor("#008B00"))

                self.setItem(row_index, col_index, item)

        self.resizeColumnsToContents()  # 设置列适应大小



# 倒计时按钮
class TimerButton(QPushButton):

    def __init__(self,num:int,name:str,icon=None,parent=None):
        '''
        :param num: 倒计时时间
        :param icon: 按钮图标
        :param name: 按钮名称
        :param parent:
        '''
        super(TimerButton,self).__init__(name,parent)
        self.num=num
        self.btn_name=name
        if icon:
            self.setIcon(icon)
        self.setText('%s(%s)' % (self.btn_name, self.num))
        self.setDisabled(True)
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.on_state_change)

    def on_state_change(self):
        if self.num==1:
            self.timer.stop()
            self.setDisabled(False)
            self.setText(self.btn_name)
        else:
            self.num=self.num-1
            self.setText('%s(%s)'%(self.btn_name,self.num))

# 倒计时标签 15分钟
class TimerLabel(QLabel):

    timer_out = pyqtSignal()

    def __init__(self, num=10, icon=None, parent=None):
        '''
        :param num: 倒计时时间
        :param icon: 按钮图标
        :param parent:
        '''
        super(TimerLabel, self).__init__(parent)
        self.num = num
        self.setText(time.strftime('%M:%S', time.gmtime(self.num)))
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.on_timer_change)

    def on_timer_change(self):
        if self.num ==0 :
            self.setText(time.strftime('%H:%M:%S', time.gmtime(self.num)))
            self.timer.stop()
            self.timer_out.emit()
        else:
            self.setText(time.strftime('%H:%M:%S', time.gmtime(self.num)))
            self.num = self.num - 1



# # 复合控件，时间组 开始时间-结束时间
# class StartEndDate(QWidget):
#
#     def __init__(self,diff=1,parent=None):
#         super(StartEndDate,self).__init__(parent)
#         main_layout= QHBoxLayout()
#         group = QGroupBox()
#         layout = QHBoxLayout()
#         self.start=QDateEdit(QDate.currentDate())
#         self.start.setCalendarPopup(True)
#         self.start.setDisplayFormat("yyyy-MM-dd")
#
#         self.end=QDateEdit(QDate.currentDate().addDays(diff))
#         self.end.setCalendarPopup(True)
#         self.end.setDisplayFormat("yyyy-MM-dd")
#
#         layout.addWidget(self.start)
#         layout.addWidget(QLabel('-'))
#         layout.addWidget(self.end)
#
#         group.setLayout(layout)
#         main_layout.addWidget(group)
#
#         self.setLayout(main_layout)
#
#     def get_start_date(self):
#         return self.start.text()
#
#     def get_end_date(self):
#         return self.end.text()
#
#     def get_range_date(self):
#         return self.start.text(),self.end.text()

# 用户组件
class UserCombox(QComboBox):

    def __init__(self):
        super(UserCombox,self).__init__()
        self.setCurrentText('所有')

# 追踪类型
class TrackTypeGroup(QHBoxLayout):

    def __init__(self):
        super(TrackTypeGroup, self).__init__()
        # 初始化
        self.initUI()
        # 布局
        self.addWidget(self.is_check)
        self.addWidget(self.cb_track_type)
        # 信号 槽
        self.is_check.stateChanged.connect(self.on_cb_check)

    def initUI(self):
        self.is_check = QCheckBox('追踪类型：')
        self.cb_track_type = QComboBox()
        self.track_type = OrderedDict([('所有',0),('未收单',1),('未结束',2),('有错误',3),('审核退回',4),('审阅退回',5)])
        self.cb_track_type.addItems(list(self.track_type.keys()))
        self.cb_track_type.setDisabled(True)
        self.cb_track_type.setMinimumWidth(100)

    def on_cb_check(self,p_int):
        if p_int:
            self.cb_track_type.setDisabled(False)
        else:
            self.cb_track_type.setDisabled(True)

# 报告类型
class ReportTypeGroup(QHBoxLayout):

    def __init__(self):
        super(ReportTypeGroup, self).__init__()
        # 界面
        self.initUI()
        # 布局
        self.addWidget(self.is_check)
        self.addWidget(self.cb_report_type)
        #信号槽
        self.is_check.stateChanged.connect(self.on_cb_check)

    def initUI(self):
        self.is_check = QCheckBox('报告类型：')
        self.cb_report_type = QComboBox()
        # self.report_type = OrderedDict([('所有',0),('普通',1),('贵宾',1),('招工',2),('职业病',3),('外出',4),('加急',5)])
        self.cb_report_type.addItems(['所有','普通','招工','贵宾','职业病','从业','重点','投诉'])
        self.cb_report_type.setCurrentText('所有')
        self.cb_report_type.setDisabled(True)
        self.cb_report_type.setMinimumWidth(80)

    def on_cb_check(self, p_int):
        if p_int:
            self.cb_report_type.setDisabled(False)
        else:
            self.cb_report_type.setDisabled(True)

    @property
    def get_tjlx(self):
        return self.cb_report_type.currentText()

    @property
    def where_tjlx(self):
        if self.is_check.isChecked():
            if self.cb_report_type.currentText() == '所有':
                return False
            else:
                return ''' AND TJLX = '%s' ''' %self.cb_report_type.currentText()
        return False

# 采血区域
class CollectAreaGroup(QHBoxLayout):

    def __init__(self,areas=None):
        super(CollectAreaGroup, self).__init__()
        lb_1 = QLabel('采血区域：')
        self.cb_area = QComboBox()
        if areas:
            self.cb_area.addItems(areas)
        else:
            self.cb_area.addItems(['所有', '明州', '江东', '明州1楼', '明州2楼', '明州3楼'])
        self.cb_area.setMinimumWidth(80)
        self.addWidget(lb_1)
        self.addWidget(self.cb_area)

    @property
    def get_area(self):
        return self.cb_area.currentText()

    def set_area(self,area):
        self.cb_area.setCurrentText(area)


# 楼层区域组件
class AreaGroup(QHBoxLayout):

    def __init__(self):
        super(AreaGroup,self).__init__()
        self.is_check = QCheckBox('体检区域：')
        self.is_check.stateChanged.connect(self.on_cb_check)
        self.cb_area = QComboBox()
        self.cb_area.addItems(['所有','明州', '江东', '明州1楼', '明州2楼', '明州3楼', '车管所', '外出', '其他'])
        self.cb_area.setCurrentText('所有')
        self.cb_area.setDisabled(True)
        self.cb_area.setMinimumWidth(80)
        self.addWidget(self.is_check)
        self.addWidget(self.cb_area)

    def on_cb_check(self,p_int):
        if p_int:
            self.cb_area.setDisabled(False)
        else:
            self.cb_area.setDisabled(True)

    @property
    def get_area(self):
        return self.cb_area.currentText()

    @property
    def where_tjqy(self):
        if self.is_check.isChecked():
            if self.cb_area.currentText() == '所有':
                return False
            elif self.cb_area.currentText() == '明州':
                return ''' AND TJQY IN ('明州1楼','明州1楼','明州3楼') '''
            else:
                return ''' AND TJQY='%s' ''' % self.cb_area.currentText()
        else:
            return False

class DepartGroup(QHBoxLayout):

    def __init__(self):
        super(DepartGroup,self).__init__()
        self.is_check = QCheckBox('部门名称：')
        self.is_check.stateChanged.connect(self.on_cb_check)
        self.cb_depart = QComboBox()
        self.cb_depart.addItems(['所有'])
        self.cb_depart.setCurrentText('所有')
        self.cb_depart.setDisabled(True)
        self.cb_depart.setMinimumWidth(100)

        self.addWidget(self.is_check)
        self.addWidget(self.cb_depart)

    def on_cb_check(self,p_int):
        if p_int:
            self.cb_depart.setDisabled(False)
        else:
            self.cb_depart.setDisabled(True)

# 复合控件，日期+时间组
class DateTimeGroup(QHBoxLayout):

    def __init__(self,diff=1,parent=None):
        super(DateTimeGroup,self).__init__(parent)
        main_layout= QHBoxLayout()

        self.start=QDateTimeEdit(QDateTime.currentDateTime())
        self.start.setTime(self.start.minimumTime())
        self.start.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.end=QDateTimeEdit(QDateTime.currentDateTime())
        self.end.setTime(self.end.maximumTime())
        self.end.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.addWidget(QLabel('采集时间：'))
        self.addSpacing(10)
        self.addWidget(self.start)
        self.addSpacing(10)
        self.addWidget(QLabel('-'))
        self.addSpacing(10)
        self.addWidget(self.end)

    def get_where_text(self):
        return self.start.text(),self.end.text()


# 复合控件，日期组 +
class DateGroup(QHBoxLayout):

    def __init__(self,diff=1,parent=None):
        super(DateGroup,self).__init__(parent)

        self.jsrq=QComboBox()
        self.jsrq.addItems(['登记日期','签到日期','收单日期','总检日期','审核日期'])
        self.jsrq.setCurrentText('签到日期')
        if diff>=0:
            self.start=QDateEdit(QDate.currentDate())
            self.end=QDateEdit(QDate.currentDate().addDays(diff))
        else:
            self.start=QDateEdit(QDate.currentDate().addDays(diff))
            self.end=QDateEdit(QDate.currentDate())

        self.start.setCalendarPopup(True)
        self.start.setDisplayFormat("yyyy-MM-dd")
        self.end.setCalendarPopup(True)
        self.end.setDisplayFormat("yyyy-MM-dd")
        self.addWidget(self.jsrq)
        self.addSpacing(10)
        self.addWidget(self.start)
        self.addSpacing(10)
        self.addWidget(QLabel('-'))
        self.addSpacing(10)
        self.addWidget(self.end)

    def setNoChoice(self,state=True):
        if state:
            self.jsrq.setDisabled(True)
        else:
            self.jsrq.setDisabled(False)


    @property
    def where_date(self):
        if self.jsrq.currentText() == '登记日期':
            return ''' DJRQ >= '%s' AND DJRQ <= '%s' ''' %(self.start.text(),self.end.text())

        elif self.jsrq.currentText() == '签到日期':
            return ''' QDRQ >= '%s' AND QDRQ <= '%s' ''' %(self.start.text(),self.end.text())

        elif self.jsrq.currentText() == '总检日期':
            return ''' ZJRQ >= '%s' AND ZJRQ <= '%s' ''' %(self.start.text(),self.end.text())

        elif self.jsrq.currentText() == '审核日期':
            return ''' SHRQ >= '%s' AND SHRQ <= '%s' ''' %(self.start.text(),self.end.text())
        else:
            return ''' TJRQ >= '%s' AND TJRQ <= '%s' ''' % (self.start.text(), self.end.text())

    @property
    def get_date_range(self):
        return self.start.text(), self.end.text()

# 复合控件，金额组
class MoneyGroup(QHBoxLayout):

    def __init__(self,parent=None):
        super(MoneyGroup,self).__init__(parent)

        self.is_check = QCheckBox('体检金额：')
        self.je_min = QSpinBox()
        self.je_min.setMinimum(0)
        self.je_min.setMaximum(999999)
        self.je_min.setValue(0)
        self.je_max = QSpinBox()
        self.je_max.setMinimum(0)
        self.je_max.setMaximum(999999)
        self.je_max.setValue(999999)
        self.je_min.setDisabled(True)
        self.je_max.setDisabled(True)

        self.addWidget(self.is_check)
        self.addSpacing(10)
        self.addWidget(self.je_min)
        self.addSpacing(10)
        self.addWidget(QLabel('-'))
        self.addSpacing(10)
        self.addWidget(self.je_max)

        self.is_check.stateChanged.connect(self.on_cb_click)

    def on_cb_click(self,p_int):
        if p_int:
            self.je_min.setDisabled(False)
            self.je_max.setDisabled(False)
        else:
            self.je_min.setDisabled(True)
            self.je_max.setDisabled(True)

    def get_where_text(self):
        if self.is_check.isChecked():
            return ''' YSJE >= '%s' AND YSJE <= '%s' ''' %(str(self.je_min.value()),str(self.je_max.value()))
        else:
            return ''

class TUintGroup(QHBoxLayout):

    def __init__(self,dwbhs:dict,dwmcs:dict):
        super(TUintGroup, self).__init__()

        self.cb_check = QCheckBox('单位名称')
        self.cb_check.stateChanged.connect(self.on_cb_check)
        self.unit = TUint(dwbhs,dwmcs)
        self.unit.setDisabled(True)
        self.addWidget(self.cb_check)
        self.addSpacing(10)
        self.addWidget(self.unit)

    def on_cb_check(self,p_int):
        if p_int:
            self.unit.setDisabled(False)
        else:
            self.unit.setDisabled(True)

    def setValues(self,p1_dict,p2_dict):
        self.unit.setBhs(p1_dict)
        self.unit.setPys(p2_dict)

    @property
    def where_dwmc(self):
        if self.cb_check.isChecked():
            return self.unit.where_dwmc
        else:
            return False

# 体检单位
class TUint(QLineEdit):

    def __init__(self,dwbhs:dict,dwmcs:dict):
        '''
        :param dwbhs: {'15555':'XXX单位',......,'16666':'XXX单位'}
        :param dwmcs:{'zhlgdx':'XXX单位',......,'zjyygz':'XXX单位'}
        '''
        super(TUint,self).__init__()
        self.dwmc_bh =  dwbhs
        self.dwmc_py = dwmcs
        self.setPlaceholderText('\ 按编号检索  . 按拼音检索  中文直接检索')
        self.model = QStringListModel()          # 完成列表的model
        self.listView = QListView()              # 完成列表
        self.listView.setWindowFlags(Qt.ToolTip)
        self.dwmcs =[]                           # 完成列表的单位

        self.textChanged.connect(self.on_dwmc_match)
        self.listView.clicked.connect(self.completeText)

    # 获取单位名称
    @property
    def where_dwmc(self):
        if self.text():
            return ''' AND DWMC = '%s' ''' %self.text()
        else:
            return False

    # 设置编号列表
    def setBhs(self,dwbhs):
        self.dwmc_bh = dwbhs

    # 设置拼音列表
    def setPys(self,dwmcs):
        self.dwmc_py = dwmcs

    #  点击完成列表中的项，使用此项自动完成输入
    def completeText(self,QModelIndex):
        self.setText(QModelIndex.data())
        self.listView.setHidden(True)

    # 匹配
    def on_dwmc_match(self,p_str):
        if p_str:
            self.dwmcs = []                                      # 清空上次匹配
            if p_str[0] == '\\':
                for dwbh in self.dwmc_bh.keys():
                    if p_str[1:] in dwbh:
                        self.dwmcs.append(self.dwmc_bh[dwbh])
            elif p_str[0] == '.':
                for dwpy in self.dwmc_py.keys():
                    if p_str[1:] in dwpy:
                        self.dwmcs.append(self.dwmc_py[dwpy])
            else:
                # 按中文检索
                pass

            self.model.setStringList(self.dwmcs)
            self.listView.setModel(self.model)
            if self.model.rowCount() == 0:
                return
            pos = QPoint(0,self.height())
            self.listView.setMinimumWidth(self.width())
            self.listView.setMaximumWidth(self.width())
            self.listView.move(self.mapToGlobal(pos).x(), self.mapToGlobal(pos).y())  # 绝对位置
            #self.listView.move(self.mapFromGlobal(pos).x(), self.mapFromGlobal(pos).y())  # 相对位置
            self.listView.show()
        else:
            self.listView.setHidden(True)

    def keyPressEvent(self,QKeyEvent):
        if not self.listView.isHidden():
            key = QKeyEvent.key()
            count = self.listView.model().rowCount()
            currentIndex = self.listView.currentIndex()
            if Qt.Key_Down == key:
                # 按向下方向键时，移动光标选中下一个完成列表中的项
                row = currentIndex.row() + 1
                if row >= count:
                    row = 0
                index = self.listView.model().index(row, 0)
                self.listView.setCurrentIndex(index)
            elif Qt.Key_Up == key:
                # 按向下方向键时，移动光标选中上一个完成列表中的项
                row = currentIndex.row() - 1
                if row < 0:
                    row = count - 1
                index = self.listView.model().index(row, 0)
                self.listView.setCurrentIndex(index)

            elif Qt.Key_Escape == key:
                # 按下Esc键时，隐藏完成列表
                self.listView.setHidden(True)

            elif (Qt.Key_Enter == key or Qt.Key_Return == key):
                # 按下回车键时，使用完成列表中选中的项，并隐藏完成列表
                if currentIndex.isValid():
                    text = self.listView.currentIndex().data()
                    self.setText(text)
                self.listView.setHidden(True)
            else:
                # 其他情况，隐藏完成列表，并使用QLineEdit的键盘按下事件
                self.listView.setHidden(True)

        super(TUint,self).keyPressEvent(QKeyEvent)


# 公共条件搜索
# 日期：签到、收单、总检、审核、审阅
# 单位：单位名称及部门名称
# 区域：明州、江东
# 定制类：
class WhereSearchGroup(QGridLayout):

    def __init__(self):
        super(WhereSearchGroup,self).__init__()

        self.s_date = DateGroup(-3)
        self.s_dwbh = TUintGroup({},{})
        self.s_depart = DepartGroup()
        self.s_area = AreaGroup()

        ###################基本信息  第一行##################################
        self.addItem(self.s_date, 0, 0, 1, 3)

        ###################基本信息  第二行##################################
        self.addItem(self.s_dwbh, 1, 0, 1, 5)
        self.addItem(self.s_depart, 1, 5, 1, 2)
        self.addItem(self.s_area, 1,7, 1, 2)

        self.setHorizontalSpacing(10)  # 设置水平间距
        self.setVerticalSpacing(10)  # 设置垂直间距
        self.setContentsMargins(10, 10, 10, 10)  # 设置外间距
        self.setColumnStretch(14, 1)  # 设置列宽，添加空白项的

    @property
    def date_range(self):
        return self.s_date.get_date_range

    @property
    def where_tjqy(self):
        return self.s_area.where_tjqy

    @property
    def where_dwmc(self):
        return self.s_dwbh.where_dwmc



# 快速检索组 体检编号、姓名、手机号码、身份证号
class QuickSearchGroup(QGroupBox):

    # 自定义 信号，封装对外使用
    returnPressed = pyqtSignal(str,str)

    def __init__(self):
        super(QuickSearchGroup,self).__init__()
        self.setTitle('快速检索')
        self.initUI()
        # 绑定信号槽
        self.s_tjbh.returnPressed.connect(partial(self.getText,'tjbh'))
        self.s_xm.returnPressed.connect(partial(self.getText, 'xm'))
        self.s_sjhm.returnPressed.connect(partial(self.getText,'sjhm'))
        self.s_sfzh.returnPressed.connect(partial(self.getText, 'sfzh'))

    def initUI(self):
        lt_main = QGridLayout()
        self.s_tjbh = QTJBH()
        self.s_xm = QXM()
        self.s_sjhm = QSJHM()
        self.s_sfzh = QSFZH()
        self.s_sfzh_read = QToolButton()
        self.s_sfzh_read.setText('...')

        ###################基本信息  第一行##################################
        lt_main.addWidget(QLabel('体检编号：'), 0, 0, 1, 1)
        lt_main.addWidget(self.s_tjbh, 0, 1, 1, 1)
        lt_main.addWidget(QLabel('姓    名：'), 0, 2, 1, 1)
        lt_main.addWidget(self.s_xm, 0, 3, 1, 1)

        ###################基本信息  第二行##################################
        lt_main.addWidget(QLabel('手机号码：'), 1, 0, 1, 1)
        lt_main.addWidget(self.s_sjhm, 1, 1, 1, 1)
        lt_main.addWidget(QLabel('身份证号：'), 1, 2, 1, 1)
        lt_main.addWidget(self.s_sfzh, 1, 3, 1, 2)
        lt_main.addWidget(self.s_sfzh_read, 1, 5, 1, 1)

        lt_main.setHorizontalSpacing(10)            #设置水平间距
        lt_main.setVerticalSpacing(10)              #设置垂直间距
        lt_main.setContentsMargins(10, 10, 10, 10)  #设置外间距
        lt_main.setColumnStretch(6, 1)             #设置列宽，添加空白项的
        self.setLayout(lt_main)

    def setText(self,p_tjbh=None,p_xm=None,p_sjhm=None,p_sfzh=None):
        self.s_tjbh.setText(p_tjbh)
        self.s_xm.setText(p_xm)
        self.s_sjhm.setText(p_sjhm)
        self.s_sfzh.setText(p_sfzh)

    def getText(self,p_key):
        if p_key == 'tjbh':
            p_text = self.s_tjbh.text()
        elif p_key == 'xm':
            p_text = self.s_xm.text()
        elif p_key == 'sjhm':
            p_text = self.s_sjhm.text()
        elif p_key == 'sfzh':
            p_text = self.s_sfzh.text()
        else:
            p_text = ''
        self.returnPressed.emit(p_key,p_text)

# 左右，左边是为目录，右边为TAB界面
class DirTabWidget(QSplitter):

    status = False
    left_flag = False  # 左边按钮，默认朝向左

    def __init__(self,title,nodes):
        '''
        :param title: 窗口标题
        :param nodes: 目录名称列表
        '''
        super(DirTabWidget,self).__init__()
        self.nodes = nodes
        self.setOrientation(Qt.Horizontal)
        self.setChildrenCollapsible(True)
        self.setHandleWidth(0)
        self.setMinimumWidth(0)
        self.setWindowTitle(title)
        # 初始化界面控件
        self.initUI()
        ##########################自身样式########################################
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("QSplitter.handle{background:lightgray}")

        #信号按照其objectName连接到相应的槽上
        QMetaObject.connectSlotsByName(self)

    def initUI(self):
        ################## 控件区 ########################################
        self.lwidget=TreeWidget(self,self.nodes)
        self.lwidget.setMaximumWidth(150)
        self.button = ArrowButton("left")
        self.rwidget=TabWidget(self)

        ########################添加控件##################################
        self.addWidget(self.lwidget)
        self.addWidget(self.button)
        self.addWidget(self.rwidget)

        #########################布局######################################
        self.setStretchFactor(0, 2)   #第一个参数代表控件序号，第二个参数0表示不可伸缩，非0可伸缩
        self.setStretchFactor(1, 1)
        self.setStretchFactor(2, 10)

    def closeEvent(self, *args, **kwargs):
        super(DirTabWidget,self).closeEvent(*args, **kwargs)
        self.status=True

    @pyqtSlot()
    def on_left_clicked(self):
        #箭头向右
        if self.left_flag:
            self.left_flag = False
            self.button.setIcon(Icon("left"))
            self.lwidget.setVisible(True)

        else:
            self.left_flag = True
            self.button.setIcon(Icon("right"))
            self.lwidget.setVisible(False)

    # 添加页签 TAB
    def addTab(self,title):
        if not self.left_flag:
            self.left_flag = True
            self.button.setIcon(Icon("right"))
            self.lwidget.setVisible(False)

    def showTab(self):
        if self.left_flag:
            self.left_flag = False
            self.button.setIcon(Icon("left"))
            self.lwidget.setVisible(True)

# 用户基础信息
class UserBaseGroup(QGroupBox):

    def __init__(self):
        super(UserBaseGroup,self).__init__()
        self.setTitle('人员信息')
        lt_main = QHBoxLayout()
        ########################控件区#####################################
        self.lb_user_id   = Lable()          # 体检编号
        self.lb_user_name = Lable()          # 姓名
        self.lb_user_sex =  Lable()          # 性别
        self.lb_user_age =  Lable()          # 年龄->自动转换出生年月
        self.lb_sjhm   =    Lable()          #手机号码
        self.lb_sfzh    =   Lable()          #身份证号

        lt_main.addWidget(QLabel('体检编号：'))
        lt_main.addWidget(self.lb_user_id)
        lt_main.addWidget(QLabel('姓名：'))
        lt_main.addWidget(self.lb_user_name)
        lt_main.addWidget(QLabel('性别：'))
        lt_main.addWidget(self.lb_user_sex)
        lt_main.addWidget(QLabel('年龄：'))
        lt_main.addWidget(self.lb_user_age)
        lt_main.addWidget(QLabel('手机号码：'))
        lt_main.addWidget(self.lb_sjhm)
        lt_main.addWidget(QLabel('身份证号：'))
        lt_main.addWidget(self.lb_sfzh)
        lt_main.addStretch()                  #设置列宽，添加空白项的
        self.setLayout(lt_main)

    # 赋值
    def setData(self,data:dict):
        self.clearData()
        self.lb_user_id.setText(data.get('tjbh','未获取到'))
        self.lb_user_name.setText(data.get('xm','未获取到'))
        self.lb_user_sex.setText(data.get('xb','未获取到'))
        self.lb_user_age.setText(data.get('nl','未获取到'))
        self.lb_sjhm.setText(data.get('sjhm','未获取到'))
        self.lb_sfzh.setText(data.get('sfzh','未获取到'))

    # 清空数据
    def clearData(self):
        self.lb_user_id.setText('')
        self.lb_user_name.setText('')
        self.lb_user_sex.setText('')
        self.lb_user_age.setText('')
        self.lb_sjhm.setText('')
        self.lb_sfzh.setText('')

# 用户详细信息
class UserDetailGroup(QGroupBox):

    def __init__(self):
        super(UserDetailGroup,self).__init__()
        self.setTitle('人员信息')
        lt_main = QGridLayout()
        
        ########################控件区#####################################
        self.lb_user_id   = Lable()       # 体检编号
        self.lb_user_name = Lable()          # 姓名
        self.lb_user_sex =  Lable()          # 性别
        self.lb_user_age =  Lable()          # 年龄->自动转换出生年月
        self.lb_depart   =  Lable()          #班级
        self.lb_dwmc    =   Lable()          #单位名称
        self.lb_tj_qdrq =   Lable()          # 签到日期，默认当天
        self.lb_sjhm   =    Lable()          #手机号码
        self.lb_sfzh    =   Lable()          #身份证号
        self.lb_tj_djrq =   Lable()          # 登记日期
        
        ###### 布局
        ###################基本信息  第一行##################################
        lt_main.addWidget(QLabel('体检编号：'), 0, 0, 1, 1)
        lt_main.addWidget(self.user_id, 0, 1, 1, 1)
        lt_main.addWidget(QLabel('姓    名：'), 0, 2, 1, 1)
        lt_main.addWidget(self.user_name, 0, 3, 1, 1)
        lt_main.addWidget(QLabel('性    别：'), 0, 4, 1, 1)
        lt_main.addWidget(self.user_sex, 0, 5, 1, 1)
        lt_main.addWidget(QLabel('年    龄：'), 0, 6, 1, 1)
        lt_main.addWidget(self.user_age, 0, 7, 1, 1)

        ###################基本信息  第二行##################################
        lt_main.addWidget(QLabel('部    门：'), 1, 0, 1, 1)
        lt_main.addWidget(self.depart, 1, 1, 1, 1)
        lt_main.addWidget(QLabel('单位名称：'), 1, 2, 1, 1)
        lt_main.addWidget(self.dwmc, 1, 3, 1, 3)
        lt_main.addWidget(QLabel('签到日期：'), 1, 6, 1, 1)
        lt_main.addWidget(self.tj_qdrq, 1, 7, 1, 1)

        ###################基本信息  第三行##################################
        lt_main.addWidget(QLabel('手机号码：'), 2, 0, 1, 1)
        lt_main.addWidget(self.sjhm, 2, 1, 1, 1)
        lt_main.addWidget(QLabel('身份证号：'), 2, 2, 1, 1)
        lt_main.addWidget(self.sfzh, 2, 3, 1, 3)
        lt_main.addWidget(QLabel('登记日期：'), 2, 6, 1, 1)
        lt_main.addWidget(self.tj_djrq, 2, 7, 1, 1)
        

        lt_main.setHorizontalSpacing(10)                 #设置水平间距
        lt_main.setVerticalSpacing(10)                   #设置垂直间距
        lt_main.setContentsMargins(10, 10, 10, 10)       #设置外间距
        lt_main.setColumnStretch(11, 1)                  #设置列宽，添加空白项的
        self.setLayout(lt_main)

# 读取身份证显示界面
class ReadChinaIdCard_UI(QDialog):

    # 自定义 信号，封装对外使用
    sendIdCard = pyqtSignal(str)

    widget_style = '''
        font: 75 14pt \"微软雅黑\";
        background-image: url(:/resource/image/sfzback.png);'''

    def __init__(self,parent=None):
        super(ReadChinaIdCard_UI,self).__init__(parent)
        self.setWindowTitle('明州体检')
        self.setFixedSize(498,394)
        self.setStyleSheet(self.widget_style)
        self.initUI()
        self.readidcard()
        # 绑定信号槽
        self.buttonBox.accepted.connect(self.on_sure)
        self.buttonBox.rejected.connect(self.close)

    def initUI(self):
        # 给窗体再加一个widget控件，对widget设置背景图片
        self.widget=QWidget(self)
        self.widget.setFixedSize(498,394)
        palette=QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(file_ico("sfzback.png"))))
        self.widget.setPalette(palette)
        self.widget.setAutoFillBackground(True)
        # 采用绝对位置 控件组
        self.lb_user_name = IdCardLable(self,110, 62, 61, 21)               # 姓名
        self.lb_user_sex = IdCardLable(self,110, 84, 31, 21)                # 性别
        self.lb_user_nation = IdCardLable(self,190, 86, 31, 21)             # 名族
        self.lb_user_birth = IdCardLable(self,110, 111, 101, 16)            # 出生
        self.lb_user_addr = IdCardLable(self,110, 134, 311, 16*4)             # 地址
        self.lb_user_card = IdCardLable(self,172, 180, 271, 16)             # 身份证号
        self.lb_user_qfjg = IdCardLable(self, 130, 220, 271, 16)            # 签发机关
        self.lb_user_yxqx = IdCardLable(self, 130, 247, 271, 16)            # 有效期限
        self.lb_user_zxzz = IdCardLable(self, 130, 268, 311, 21)            # 最新住址
        # 消息 ：错误信息
        self.lb_message = IdCardLable(self, 10, 360, 281, 21)
        self.lb_message.setText('请放卡...')
        # 按钮框
        self.buttonBox=QDialogButtonBox(self)
        self.buttonBox.addButton("确定",QDialogButtonBox.YesRole)
        self.buttonBox.addButton("取消", QDialogButtonBox.NoRole)
        self.buttonBox.setGeometry(QRect(320, 345, 100, 50))
        #self.buttonBox.setCenterButtons(True)

    def readidcard(self):
        self.cur_thread = ReadThread()
        self.cur_thread.signalPost.connect(self.setData, type=Qt.QueuedConnection)
        self.cur_thread.signalError.connect(self.showMes, type=Qt.QueuedConnection)
        self.cur_thread.start()

    def setData(self,data:list):
        self.lb_user_name.setText(data[0])
        self.lb_user_sex.setText(data[1])
        self.lb_user_nation.setText(data[2])
        self.lb_user_birth.setText(data[3])
        self.lb_user_addr.setText(data[4])
        self.lb_user_addr.setWordWrap(True)
        self.lb_user_addr.setAlignment(Qt.AlignTop)
        self.lb_user_card.setText(data[5])
        self.lb_user_qfjg.setText(data[6])
        self.lb_user_qfjg.adjustSize()
        self.lb_user_yxqx.setText(data[7])
        self.lb_user_zxzz.setText(data[8])

    # 确定
    def on_sure(self):
        self.sendIdCard.emit(self.lb_user_card.text())
        self.accept()
        self.close()

    def showMes(self,message:str):
        self.lb_message.setText(message)

    def closeEvent(self, *args, **kwargs):
        super(ReadChinaIdCard_UI, self).closeEvent(*args, **kwargs)
        if self.cur_thread:
            self.cur_thread.stop()

class ReadThread(QThread):

    # 定义信号,定义参数为str类型
    signalError = pyqtSignal(str)     # 错误信息
    signalPost = pyqtSignal(list)     # 更新界面
    signalExit = pyqtSignal()

    def __init__(self):
        super(ReadThread,self).__init__()
        self.file_wx = os.path.join(os.environ["TMP"], 'chinaidcard\wz.txt')
        self.file_zp = os.path.join(os.environ["TMP"], 'chinaidcard\zp.bmp')
        self.c_obj = IdCard()
        self.runing = True

    def stop(self):
        self.runing = False

    def run(self):
        while self.runing:
            if self.c_obj.dll_obj:
                open_state = self.c_obj.open()
                if open_state == 1:
                    legal_state = self.c_obj.legal()
                    if legal_state == 1:
                        if self.c_obj.read(4) == 1:
                            user_info = open(self.file_wx).read().split('\n')
                            self.signalPost.emit(user_info)
                            os.remove(self.file_wx)
                            os.remove(self.file_zp)
                            self.signalError.emit('读卡成功！')
                        else:
                            self.signalError.emit('读卡失败！')
                    elif legal_state == 2:
                        self.signalError.emit('请重新放卡...')
                    elif legal_state == 3:
                        self.signalError.emit('选卡失败！')
                    else:
                        self.signalError.emit('初始化失败！')
                else:
                    self.signalError.emit('动态库加载失败/端口打开失败！')
            else:
                self.signalError.emit('动态库加载失败！')

            time.sleep(0.3)





if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    # 倒计时按钮
    # ui = TimerButton(30,'审阅')
    # 一组日期
    #ui = StartEndDate()
    # data1=  {'10000': '社区', '10001': '社区2', '10501': '新社区'}
    # data2 = {'sq': '社区', 'sq2': '社区2', 'xsq': '新社区'}
    # ui = TUint(data1,data2)
    ui = UserBaseGroup()
    ui.show()
    app.exec_()