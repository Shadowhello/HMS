from widgets.cwidget import *
from widgets.bweb import *

class ReportReviewUI(Widget):

    def __init__(self,parent=None):
        super(ReportReviewUI,self).__init__(parent)
        self.initUI()

    def initUI(self):
        lt_main = QHBoxLayout()
        lt_left = QVBoxLayout()
        self.gp_where_search = BaseCondiSearchGroup()
        self.gp_quick_search = QuickSearchGroup()
        self.table_report_review_cols = OrderedDict([
             ('tjzt', '体检状态'),
             ('bgzt', '报告状态'),
             ('tjlx','类型'),
             ('tjqy','区域'),
             ('tjbh','体检编号'),
             ('xm','姓名'),
             ('xb','性别'),
             ('nl','年龄'),
             ('sjhm','手机号码'),
             ('sfzh', '身份证号')
        ])
        # 待审阅列表
        self.table_report_review = ReportReviewTable(self.table_report_review_cols)
        gp_table = QGroupBox('待审阅列表（0）')
        lt_table = QHBoxLayout()
        lt_table.addWidget(self.table_report_review)
        gp_table.setLayout(lt_table)
        # 审阅信息
        self.gp_review_user = ReportReviewUser()
        # 添加布局
        lt_left.addWidget(self.gp_where_search,1)
        lt_left.addWidget(self.gp_quick_search,1)
        lt_left.addWidget(gp_table,7)
        lt_left.addWidget(self.gp_review_user,1)

        ####################右侧布局#####################
        self.report_web = WebView()
        lt_right = QHBoxLayout()
        lt_right.addWidget(self.report_web)
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
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(row_index)
            for col_index, col_value in enumerate(row_data):
                item = QTableWidgetItem(col_value)

                self.setItem(row_index, col_index, item)

        # 特殊设置
        if datas:
            # self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)         #所有列
            # self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            # self.horizontalHeader().setMinimumSectionSize(60)
            # self.horizontalHeader().setMaximumSectionSize(300)
            self.setColumnWidth(0, 60)  # 结果周期
            self.setColumnWidth(1, 60)  # 追踪进度
            self.setColumnWidth(2, 60)  # 追踪状态
            self.setColumnWidth(3, 50)  # 追踪人
            self.setColumnWidth(4, 60)  # 体检状态
            self.setColumnWidth(5, 50)  # 类型
            self.setColumnWidth(6, 60)  # 区域
            self.setColumnWidth(7, 70)  # 体检编号
            self.setColumnWidth(8, 60)  # 姓名
            self.setColumnWidth(9, 30)  # 性别
            self.setColumnWidth(10, 30)  # 年龄
            self.setColumnWidth(11, 120)  # 身份证号
            self.setColumnWidth(12, 80)  # 手机号码
            self.setColumnWidth(13, 180)  # 单位编号
            self.setColumnWidth(14, 70)  # 签到日期
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