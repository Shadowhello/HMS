from widgets.cwidget import *

#报告整理：刷单、首行展示、人员信息、报告信息、手工单信息、胶片信息、
class ReportOrderUI(UI):

    def __init__(self,parent=None):
        super(ReportOrderUI,self).__init__(parent)
        self.initUI()

    def initUI(self):
        #######################################################
        self.le_tjbh = QTJBH()
        gp_search = QGroupBox('筛选条件')
        lt_search = QHBoxLayout()
        lt_search.addWidget(self.le_tjbh)
        gp_search.setLayout(lt_search)
        self.table_report_order_cols = OrderedDict([
            ('bgzt', '状态'),
            ('tjbh', '体检编号'),
            ('xm', '姓名')
        ])
        self.table_report_order = ReportOrderTable(self.table_report_order_cols)
        self.gp_report_order = QGroupBox('整理列表')
        lt_report_order = QHBoxLayout()
        lt_report_order.addWidget(self.table_report_order)
        self.gp_report_order.setLayout(lt_report_order)
        self.left_layout.addWidget(gp_search)
        self.left_layout.addWidget(self.gp_report_order)
        ###########################################################

# 报告审阅列表
class ReportOrderTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(ReportOrderTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        self.cur_data_set = []
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            tmp = []
            self.insertRow(row_index)
            for col_index, col_value in enumerate(row_data):
                item = QTableWidgetItem(str2(col_value))
                tmp.append(str2(col_value))
                if col_index==0:
                    if str2(col_value)=='已审核':
                        item.setBackground(QColor("#FF0000"))
                    else:
                        item.setBackground(QColor("#f0e68c"))

                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)
            self.cur_data_set.append(tmp)
        # 布局
        self.setColumnWidth(0, 50)  # 状态
        self.setColumnWidth(1, 50)  # 类型
        self.setColumnWidth(2, 55)  # 区域
        self.setColumnWidth(3, 75)  # 体检编号
        self.setColumnWidth(4, 60)  # 姓名
        self.setColumnWidth(5, 40)  # 性别
        self.setColumnWidth(6, 40)  # 年龄
        self.setColumnWidth(7, 100) # 审阅日期
        self.setColumnWidth(8, 60)  # 审阅人
        self.setColumnWidth(9, 100)  # 单位名称
        self.horizontalHeader().setStretchLastSection(True)