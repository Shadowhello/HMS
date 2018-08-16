from widgets.cwidget import *
from widgets.bweb import *
from .model import *

class ReportReviewUI(Widget):

    def __init__(self,parent=None):
        super(ReportReviewUI,self).__init__(parent)
        self.initUI()
        self.initParas()

    def initParas(self):
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()
        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)

        self.gp_where_search.s_dwbh.setValues(self.dwmc_bh,self.dwmc_py)

    def initUI(self):
        lt_main = QHBoxLayout()
        lt_left = QVBoxLayout()
        self.btn_query = ToolButton(Icon('query'), '查询')
        self.gp_where_search = BaseCondiSearchGroup(1)
        self.gp_where_search.setText('审核日期')
        self.gp_where_search.setNoChoice()
        # 报告状态
        self.cb_report_state = ReportStateGroup()
        self.cb_report_state.addStates(['所有','未审阅','已审阅'])
        self.cb_report_type = ReportTypeGroup()
        self.cb_user = UserCombox()
        self.cb_user.addItems(['所有',self.login_name])
        # 区域
        self.cb_area = AreaGroup()
        self.cb_user = UserGroup('审阅护士')
        self.cb_user.addUsers(['所有',self.login_name])
        self.gp_where_search.addItem(self.cb_area, 0, 3, 1, 2)
        self.gp_where_search.addItem(self.cb_report_state, 1, 3, 1, 2)
        self.gp_where_search.addItem(self.cb_user, 0, 5, 1, 2)
        self.gp_where_search.addItem(self.cb_report_type, 1, 5, 1, 2)
        # 按钮
        self.gp_where_search.addWidget(self.btn_query, 0, 7, 2, 2)
        self.gp_quick_search = QuickSearchGroup()
        self.table_report_review_cols = OrderedDict([
            ('bgzt', '报告状态'),
            ('tjbh', '体检编号'),
            ('xm', '姓名'),
            ('xb', '性别'),
            ('nl', '年龄'),
            ('qdrq','签到日期'),
            ('jcys','检查医生'),
            ('jcqy', '检查区域'),
            ('fpath', '文件路径')
        ])
        # 待审阅列表
        self.table_report_equip = ReportReviewTable(self.table_report_review_cols)
        self.gp_table = QGroupBox('审阅完成列表（0）')
        lt_table = QHBoxLayout()
        lt_table.addWidget(self.table_report_equip)
        self.gp_table.setLayout(lt_table)
        # 审阅信息
        self.gp_review_user = ReportReviewUser()
        # 添加布局
        lt_left.addWidget(self.gp_where_search,1)
        lt_left.addWidget(self.gp_quick_search,1)
        lt_left.addWidget(self.gp_table,7)
        lt_left.addWidget(self.gp_review_user,1)

        ####################右侧布局#####################
        self.wv_report_equip = WebView()
        lt_right = QHBoxLayout()
        lt_right.addWidget(self.wv_report_equip)
        gp_right = QGroupBox('报告预览')
        gp_right.setLayout(lt_right)
        lt_main.addLayout(lt_left,1)
        lt_main.addWidget(gp_right,2)

        self.setLayout(lt_main)

# 报告审阅列表
class ReportReviewTable(TableWidget):

    tjqy = None  # 体检区域
    tjlx = None  # 体检类型

    def __init__(self, heads, parent=None):
        super(ReportReviewTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # 字典载入
        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)                # 插入一行
            for col_index, col_name in enumerate(heads.keys()):
                item = QTableWidgetItem(row_data[col_name])
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)
        # 布局
        self.setColumnWidth(0, 70)  # 设备名称
        self.setColumnWidth(1, 70)  # 体检编号
        self.setColumnWidth(2, 50)  # 姓名
        self.setColumnWidth(3, 80)  # 检查日期
        self.setColumnWidth(4, 70)  # 检查姓名
        self.setColumnWidth(5, 100) # 检查区域
        self.horizontalHeader().setStretchLastSection(True)

class ReportReviewUser(QGroupBox):

    def __init__(self):
        super(ReportReviewUser,self).__init__()
        self.setTitle('审阅信息')
        lt_main = QGridLayout()
        self.review_user = ReviewLabel()
        self.review_time = ReviewLabel()
        self.review_comment = QPlainTextEdit()
        # self.review_comment.setFixedHeight(80)
        self.review_comment.setStyleSheet('''border: 1px solid;font: 75 12pt \"微软雅黑\";height:20px;''')
        self.btn_review_sure = QPushButton('完成审阅')
        self.btn_review_cancle = QPushButton('取消审阅')

        ###################基本信息  第一行##################################
        lt_main.addWidget(QLabel('审阅者：'), 0, 0, 1, 1)
        lt_main.addWidget(self.review_user, 0, 1, 1, 1)
        lt_main.addWidget(QLabel('审阅时间：'), 0, 2, 1, 1)
        lt_main.addWidget(self.review_time, 0, 3, 1, 1)
        # 按钮
        lt_main.addWidget(self.btn_review_sure, 0, 4, 1, 1)
        lt_main.addWidget(self.btn_review_cancle, 0, 6, 1, 1)
        ###################基本信息  第二行##################################
        lt_main.addWidget(QLabel('审阅备注：'), 1, 0, 2, 2)
        lt_main.addWidget(self.review_comment, 1, 1, 2, 7)


        lt_main.setHorizontalSpacing(10)            #设置水平间距
        lt_main.setVerticalSpacing(10)              #设置垂直间距
        lt_main.setContentsMargins(10, 10, 10, 10)  #设置外间距
        lt_main.setColumnStretch(6, 1)             #设置列宽，添加空白项的
        self.setLayout(lt_main)

    # 清空数据
    def clearData(self):
        self.review_user.setText('')
        self.review_time.setText('')
        self.review_comment.setText('')
        self.btn_review_sure.setEnabled(True)
        self.btn_review_cancle.setEnabled(False)

    # 设置数据
    def setData(self,data:dict):
        self.review_user.setText(data['user'])
        self.review_time.setText(data['time'])
        self.review_comment.setText(data['comment'])
        self.review_comment.setEnabled(False)
        self.btn_review_sure.setEnabled(False)
        self.btn_review_cancle.setEnabled(True)

class ReviewLabel(QLabel):

    def __init__(self,p_str=None,parent=None):
        super(ReviewLabel,self).__init__(p_str,parent)
        self.setStyleSheet('''border: 1px solid;font: 75 12pt \"微软雅黑\";''')
        self.setMinimumWidth(80)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = ReportReviewUI()
    ui.show()
    app.exec_()