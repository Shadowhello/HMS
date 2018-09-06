from widgets.cwidget import *
from .model import *

JXZD = {

}

class AchievementsNurse(Widget):

    def __init__(self,parent=None):
        super(AchievementsNurse,self).__init__(parent)
        self.initUI()
        # 绑定信号槽
        self.btn_query.clicked.connect(self.on_btn_query_click)
        self.table_achieve_sum.itemClicked.connect(self.on_table_achieve_sum_click)
        self.table_achieve_group.itemClicked.connect(self.on_table_achieve_group_click)
        # 特殊变量 ，用于快速获取
        self.cur_start_time =None       # 当前选择开始时间
        self.cur_end_time = None        # 当前选择结束时间
        self.cur_yggh = None            # 当前选择工号

    def initUI(self):
        lt_main = QVBoxLayout()
        ################# 条件检索 ##############################
        lt_top = QHBoxLayout()
        self.de_start = QDateEdit(QDate.currentDate())
        self.de_end = QDateEdit(QDate.currentDate().addDays(1))
        self.de_start.setCalendarPopup(True)
        self.de_start.setDisplayFormat("yyyy-MM-dd")
        self.de_end.setCalendarPopup(True)
        self.de_end.setDisplayFormat("yyyy-MM-dd")
        self.cb_user = QComboBox()
        self.cb_user.addItems([self.login_name,'所有'])
        self.btn_query = QPushButton(Icon('query'),'查询')
        self.btn_export = QPushButton(Icon('导出'), '导出')
        lt_top.addWidget(QLabel("操作时间："))
        lt_top.addWidget(self.de_start)
        lt_top.addWidget(QLabel('-'))
        lt_top.addWidget(self.de_end)
        lt_top.addWidget(QLabel('护士：'))
        lt_top.addWidget(self.cb_user)
        lt_top.addWidget(self.btn_query)
        lt_top.addWidget(self.btn_export)
        lt_top.addStretch()
        ####################################################

        lt_middle = QHBoxLayout()
        self.gp_middle_left = QGroupBox('绩效汇总')
        lt_middle_left = QHBoxLayout()
        self.gp_middle_middle = QGroupBox('绩效分组汇总')
        lt_middle_middle = QHBoxLayout()
        self.gp_middle_right = QGroupBox('绩效明细')
        lt_middle_right = QHBoxLayout()
        # 绩效总汇总
        self.table_achieve_sum_cols = OrderedDict([
            ('yggh', '工号'),
            ('ygxm', '姓名'),
            ('jxjj', '绩效'),
            ('gwgz', '岗位'),
            ('gzzh', '合计'),
        ])
        self.table_achieve_sum = AchieveSumTable(self.table_achieve_sum_cols)
        lt_middle_left.addWidget(self.table_achieve_sum)
        self.gp_middle_left.setLayout(lt_middle_left)
        # 绩效分汇总
        self.table_achieve_group_cols = OrderedDict([
            ('jxbh', '绩效编号'),
            ('jxmc', '绩效名称'),
            ('jxxs', '绩效系数'),
            ('jxsl', '工作量'),
            ('jxxj', '绩效小计'),
        ])
        self.table_achieve_group = AchieveGroupTable(self.table_achieve_group_cols)
        lt_middle_middle.addWidget(self.table_achieve_group)
        self.gp_middle_middle.setLayout(lt_middle_middle)
        # 绩效明细
        # 绩效分汇总
        self.table_achieve_detail_cols = OrderedDict([
            ('tjbh', '体检编号'),
            ('mxbh', '明细编号'),
            ('czsj', '操作时间'),
            ('czqy', '操作区域'),
            ('jlmc', '操作名称'),
        ])
        # results = self.session.query(MT_TJ_CZJLWHB).all()
        # self.table_achieve_cols = OrderedDict([(result.czdzd,result.czbh) for result in results])
        self.table_achieve_detail =AchieveDetailTable(self.table_achieve_detail_cols)
        lt_middle_right.addWidget(self.table_achieve_detail)
        self.gp_middle_right.setLayout(lt_middle_right)
        lt_middle.addWidget(self.gp_middle_left)
        lt_middle.addWidget(self.gp_middle_middle)
        lt_middle.addWidget(self.gp_middle_right)
        lt_middle.addStretch()

        lt_main.addLayout(lt_top)
        lt_main.addLayout(lt_middle)
        self.setLayout(lt_main)

    def on_btn_query_click(self):
        self.cur_start_time = self.de_start.text()
        self.cur_end_time = self.de_end.text()
        sql = get_nurse_sum_sql(self.cur_start_time,self.cur_end_time)
        results = self.session.execute(sql).fetchall()
        self.table_achieve_sum.load(results)
        self.gp_middle_left.setTitle(" 绩效汇总 (%s 人) " %self.table_achieve_sum.rowCount())

    # 单击 汇总数据
    def on_table_achieve_sum_click(self,QTableWidgetItem):
        yggh = self.table_achieve_sum.getItemValueOfKey(QTableWidgetItem.row(), 'yggh')
        self.cur_yggh = yggh
        ygxm = self.table_achieve_sum.getItemValueOfKey(QTableWidgetItem.row(), 'ygxm')
        jxjj = self.table_achieve_sum.getItemValueOfKey(QTableWidgetItem.row(), 'jxjj')
        sql = get_nurse_group_sql(self.cur_start_time,self.cur_end_time,yggh)
        results = self.session.execute(sql).fetchall()
        self.table_achieve_group.load(results)
        self.gp_middle_middle.setTitle(" 绩效分组汇总 (姓名：%s 奖金：%s) " %(ygxm,jxjj))

    # 单击 分组数据
    def on_table_achieve_group_click(self,QTableWidgetItem):
        jxbh = self.table_achieve_group.getItemValueOfKey(QTableWidgetItem.row(), 'jxbh')
        sql = get_nurse_detail_sql(self.cur_start_time,self.cur_end_time,self.cur_yggh,jxbh)
        results = self.session.execute(sql).fetchall()
        self.table_achieve_detail.load(results)
        self.gp_middle_right.setTitle(" 绩效明细 (%s) " %self.table_achieve_detail.rowCount())


class AchieveDetailTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(AchieveDetailTable, self).__init__(heads, parent)

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

# 汇总
class AchieveSumTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(AchieveSumTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(row_index)
            for col_index, col_value in enumerate(row_data):
                if col_index==0:
                    item = QTableWidgetItem(str(col_value))
                elif col_index==1:
                    item = QTableWidgetItem(str2(col_value))
                elif col_index==2:
                    item = QTableWidgetItem(str(round(col_value,1)))
                elif col_index==4:
                    item = QTableWidgetItem(str(round(row_data[2],1)))
                else:
                    item = QTableWidgetItem()

                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

        self.setColumnWidth(0, 80)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 50)
        self.setColumnWidth(3, 50)
        self.setColumnWidth(4, 50)

# 分组汇总
class AchieveGroupTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(AchieveGroupTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(row_index)
            for col_index, col_value in enumerate(row_data):
                if col_index == len(self.heads)-1:
                    item = QTableWidgetItem(str(round(col_value, 1)))
                else:
                    item = QTableWidgetItem(str2(col_value))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)