from widgets.cwidget import *
from lis.model import *
from utils.buildbarcode import BarCodeBuild
# 留样

def unire_font():
    font = QFont()
    font.setBold(True)
    font.setWeight(75)
    font.setPixelSize(24)
    return font

class CollectUrine_UI(Widget):

    def __init__(self):

        super(CollectUrine_UI,self).__init__()
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        ####################左边布局#####################################
        gp_left = QGroupBox()
        lt_left = QVBoxLayout()
        lt_left_top = QHBoxLayout()
        self.lt_left_bottom = QGridLayout()
        gp_left_bottom = QGroupBox('留样详情')
        gp_left_bottom.setLayout(self.lt_left_bottom)

        label = QLabel('条码号：')
        self.tmbh = QSerialNo()
        self.tmbh.setFixedHeight(200)
        self.tmbh.setFont(QFont("微软雅黑" , 50,  QFont.Bold))
        label.setFont(QFont("微软雅黑" , 50,  QFont.Bold))
        self.urine_cols = OrderedDict([
                                ("cjzt", "状态"),
                                ("xm", "姓名"),
                                ("xb", "性别"),
                                ("nl", "年龄"),
                                ("tmbh", "条码号"),
                                ("tjbh","体检编号"),
                                ("xmhz", "条码项目")
                            ])
        self.table_urine = CollectUnireTable(self.urine_cols)
        # self.table_urine.verticalHeader().setVisible(False)  # 去掉行头
        self.table_urine.horizontalHeader().setStretchLastSection(True)
        self.table_urine.setColumnWidth(2, 70)
        self.table_urine.setColumnWidth(3, 70)
        self.table_urine.setColumnWidth(4, 180)
        self.table_urine.setColumnWidth(5, 180)
        self.table_urine.setStyleSheet('''
        QHeaderView{font-size:24px;}QTableView::item {font-size:18px;}
        ''')
        # lt_left_top.addWidget(label)
        lt_left_top.addWidget(self.tmbh)

        lt_left.addLayout(lt_left_top)
        lt_left.addWidget(gp_left_bottom)

        gp_left.setLayout(lt_left)
        ############################ 布局右边 ############################
        self.gp_right = QGroupBox('留样扫码')
        lt_right = QVBoxLayout()
        lt_right.addWidget(self.table_urine)
        self.gp_right.setLayout(lt_right)
        main_layout.addWidget(gp_left,1)
        main_layout.addWidget(self.gp_right,2)

        self.setLayout(main_layout)

class CollectUnireTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(CollectUnireTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(row_index)
            for col_index, col_value in enumerate(row_data):
                item = QTableWidgetItem(str2(col_value))
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(unire_font())
                self.setItem(row_index, col_index, item)

        # self.setColumnWidth(0, 70)
        # self.setColumnWidth(1, 60)
        # self.setColumnWidth(2, 30)
        # self.setColumnWidth(3, 30)
        self.horizontalHeader().setStretchLastSection(True)

    def insert(self,data):
        for col_index, col_value in enumerate(data):
            item = QTableWidgetItem(col_value)
            item.setFont(unire_font())
            self.setItem(self.rowCount() - 1, col_index, item)
