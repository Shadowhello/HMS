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
        self.btn_review_mode = ToolButton(Icon('全屏'), '进入审阅模式')
        self.gp_where_search = BaseCondiSearchGroup(1)
        self.gp_where_search.setText('审核日期')
        self.gp_where_search.setNoChoice()
        # 报告状态
        self.cb_report_state = ReportStateGroup()
        self.cb_report_state.addStates(['所有','未审阅','已审阅'])
        self.cb_report_type = ReportTypeGroup()
        # 区域
        self.cb_area = AreaGroup()
        # 人员
        self.cb_user = UserGroup('审阅护士：')
        self.cb_user.addUsers(['所有',self.login_name])
        # 添加布局
        self.gp_where_search.addItem(self.cb_area, 0, 3, 1, 2)
        self.gp_where_search.addItem(self.cb_report_state, 1, 3, 1, 2)
        self.gp_where_search.addItem(self.cb_user, 0, 5, 1, 2)
        self.gp_where_search.addItem(self.cb_report_type, 1, 5, 1, 2)
        # 按钮
        lt_1 = QHBoxLayout()
        self.gp_where_search.addWidget(self.btn_query, 0, 7, 2, 2)
        self.gp_quick_search = QuickSearchGroup(1)
        lt_1.addWidget(self.gp_quick_search)
        lt_1.addWidget(self.btn_review_mode)

        self.table_report_review_cols = OrderedDict([
            ('bgzt', '状态'),
            ('tjlx', '类型'),
            ('tjqy', '区域'),
            ('tjbh', '体检编号'),
            ('xm', '姓名'),
            ('xb', '性别'),
            ('nl', '年龄'),
            ('syrq','审阅日期'),
            ('syxm','审阅护士'),
            ('dwmc', '单位名称'),
            ('sybz', '审阅备注')
        ])
        # 待审阅列表
        self.table_report_review = ReportReviewTable(self.table_report_review_cols)
        self.gp_table = QGroupBox('审阅列表（0）')
        lt_table = QHBoxLayout()
        lt_table.addWidget(self.table_report_review)
        self.gp_table.setLayout(lt_table)
        # 审阅信息
        self.gp_review_user = ReportReviewUser()
        # 添加布局
        lt_left.addWidget(self.gp_where_search,1)
        lt_left.addLayout(lt_1,1)
        lt_left.addWidget(self.gp_table,7)
        lt_left.addWidget(self.gp_review_user,1)

        ####################右侧布局#####################
        self.wv_report_equip = WebView()
        # self.wv_report_page = self.wv_report_equip.page().mainFrame()
        # self.wv_report_page.setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)#去掉滑动条
        # self.wv_report_page.setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
        lt_right = QHBoxLayout()
        lt_right.addWidget(self.wv_report_equip)
        self.gp_right = QGroupBox('报告预览')
        self.gp_right.setLayout(lt_right)
        lt_main.addLayout(lt_left,1)
        lt_main.addWidget(self.gp_right,2)

        self.setLayout(lt_main)

# 报告审阅列表
class ReportReviewTable(TableWidget):

    tjqy = None  # 体检区域
    tjlx = None  # 体检类型

    def __init__(self, heads, parent=None):
        super(ReportReviewTable, self).__init__(heads, parent)
        self.table_where = None

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(row_index)
            for col_index, col_value in enumerate(row_data):
                item = QTableWidgetItem(str2(col_value))
                if col_index==0:
                    if str2(col_value)=='已审核':
                        item.setBackground(QColor("#FF0000"))
                    else:
                        item.setBackground(QColor("#f0e68c"))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)
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

    def add_query(self,where_str):
        self.table_where = where_str

class ReportReviewUser(QGroupBox):

    # 自定义 信号，封装对外使用
    btnClick = pyqtSignal(bool,int)

    def __init__(self):
        super(ReportReviewUser,self).__init__()
        self.initUI()
        self.btn_review.clicked.connect(self.on_btn_review_click)

    def initUI(self):
        self.setTitle('审阅信息')
        lt_main = QGridLayout()
        self.review_user = ReviewLabel()
        self.review_time = ReviewLabel()
        self.review_comment = QPlainTextEdit()
        self.review_comment.setStyleSheet('''font: 75 12pt '微软雅黑';color: rgb(255,0,0);height:20px;''')
        self.btn_review = Timer2Button(Icon('样本签收'),'完成审阅')
        ###################基本信息  第一行##################################
        lt_main.addWidget(QLabel('审阅者：'), 0, 0, 1, 1)
        lt_main.addWidget(self.review_user, 0, 1, 1, 1)
        lt_main.addWidget(QLabel('审阅时间：'), 1, 0, 1, 1)
        lt_main.addWidget(self.review_time, 1, 1, 1, 1)
        # 按钮
        lt_main.addWidget(self.btn_review, 0, 9, 2, 2)
        ###################基本信息  第二行##################################
        # lt_main.addWidget(QLabel('审阅备注：'), 0, 2, 2, 2)
        lt_main.addWidget(self.review_comment, 0, 2, 2, 7)

        lt_main.setHorizontalSpacing(10)            #设置水平间距
        lt_main.setVerticalSpacing(10)              #设置垂直间距
        lt_main.setContentsMargins(10, 10, 10, 10)  #设置外间距
        lt_main.setColumnStretch(6, 1)             #设置列宽，添加空白项的
        self.setLayout(lt_main)
        # 状态标签
        self.lb_review_bz = StateLable(self)
        self.lb_review_bz.show()


    # 清空数据
    def clearData(self):
        self.review_user.setText('')
        self.review_time.setText('')
        self.review_comment.setPlainText('')
        self.lb_review_bz.show2(False)

    # 设置数据
    def setData(self,data:dict):
        self.btn_review.stop()
        if data['syzt']=='已审核':
            self.lb_review_bz.show2(False)
            self.btn_review.start()
        else:
            self.lb_review_bz.show2()
            self.btn_review.setText('取消审阅')
        self.review_user.setText(data['syxm'])
        self.review_time.setText(data['syrq'])
        self.review_comment.setPlainText(data['sybz'])

    # 状态变更
    def statechange(self):
        # 从完成审阅 -> 取消审阅
        if '完成' in self.btn_review.text():
            self.btn_review.stop()
            self.btn_review.setText('取消审阅')
        else:
            pass

    # 获取审阅备注信息
    def get_sybz(self):
        return self.review_comment.toPlainText()

    # 按钮点击
    def on_btn_review_click(self):
        if '完成审阅' in self.btn_review.text():
            syzt = True
        else:
            syzt = False
        try:
            num = self.btn_review.num
        except Exception as e:
            num = 0
        self.btnClick.emit(syzt,num)


class ReviewLabel(QLabel):

    def __init__(self,p_str=None,parent=None):
        super(ReviewLabel,self).__init__(p_str,parent)
        self.setStyleSheet('''border: 1px solid;font: 75 12pt \"微软雅黑\";''')
        self.setMinimumWidth(80)

class StateLable(QLabel):

    def __init__(self,parent):
        super(StateLable,self).__init__(parent)
        self.setMinimumSize(200,200)
        self.setGeometry(200,-60,100,100)
        self.setStyleSheet('''font: 75 28pt "微软雅黑";color: rgb(255, 0, 0);''')
        self.setAttribute(Qt.WA_TranslucentBackground)                               #背景透明
        self.data = open(file_ico('已审核.png'),'rb').read()

    def show2(self,flag = True):
        if flag:
            p = QPixmap()
            p.loadFromData(self.data)
            self.setPixmap(p)
        else:
            self.clear()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = ReportReviewUI()
    ui.show()
    app.exec_()