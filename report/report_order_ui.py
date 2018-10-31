from .report_progress import *

#报告整理：刷单、首行展示、人员信息、报告信息、手工单信息、胶片信息、
class ReportOrderUI(UI):

    def __init__(self):
        super(ReportOrderUI,self).__init__("报告整理")
        self.initUI()

    def initUI(self):
        self.left_group.setMinimumWidth(200)
        ###################### 左 ##########################
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
        self.gp_report_order = QGroupBox('整理列表(0)')
        lt_report_order = QHBoxLayout()
        lt_report_order.addWidget(self.table_report_order)
        self.gp_report_order.setLayout(lt_report_order)
        self.left_layout.addWidget(gp_search)
        self.left_layout.addWidget(self.gp_report_order)
        ######################## 中 ################################
        # 人员信息  报告信息    手工单 胶片信息
        gp_middle_top = QGroupBox('人员信息')
        lt_middle_top = QGridLayout()
        ########################人员信息#####################################
        self.lb_user_id   = Lable()          #  体检编号
        self.lb_user_id.setMinimumWidth(70)
        self.lb_user_name = Lable()          #  姓名
        self.lb_user_sex  = Lable()          #  性别
        self.lb_user_age  = Lable()          #  年龄->自动转换出生年月
        self.lb_user_type = Lable()          #  体检类型
        self.lb_user_dwmc = Lable()          #  单位名称
        self.lb_user_bmmc = Lable()          #  部门
        self.lb_user_tjrq = Lable()          #  签到日期，默认当天
        self.lb_user_sjhm = Lable()          #  手机号码
        self.lb_user_sjhm.setMinimumWidth(90)
        self.lb_user_sfzh = Lable()          #  身份证号
        self.lb_user_pic  = PicLable()       # 身份证号照片
        ###################基本信息  第一行##################################
        lt_middle_top.addWidget(QLabel('体检编号：'), 0, 0, 1, 1)
        lt_middle_top.addWidget(self.lb_user_id, 0, 1, 1, 1)
        lt_middle_top.addWidget(QLabel('姓    名：'), 0, 2, 1, 1)
        lt_middle_top.addWidget(self.lb_user_name, 0, 3, 1, 1)
        lt_middle_top.addWidget(QLabel('性    别：'), 0, 4, 1, 1)
        lt_middle_top.addWidget(self.lb_user_sex, 0, 5, 1, 1)
        lt_middle_top.addWidget(QLabel('年    龄：'), 0, 6, 1, 1)
        lt_middle_top.addWidget(self.lb_user_age, 0, 7, 1, 1)
        # lt_middle_top.addWidget(self.lb_user_pic, 0, 8, 3, 3)
        ###################基本信息  第二行##################################
        lt_middle_top.addWidget(QLabel('单位名称：'), 1, 0, 1, 1)
        lt_middle_top.addWidget(self.lb_user_dwmc, 1, 1, 1, 6)
        ###################基本信息  第三行##################################
        lt_middle_top.addWidget(QLabel('手机号码：'), 2, 0, 1, 1)
        lt_middle_top.addWidget(self.lb_user_sjhm, 2, 1, 1, 1)
        lt_middle_top.addWidget(QLabel('身份证号：'), 2, 2, 1, 1)
        lt_middle_top.addWidget(self.lb_user_sfzh, 2, 3, 1, 3)

        lt_middle_top.setHorizontalSpacing(10)            #设置水平间距
        lt_middle_top.setVerticalSpacing(10)              #设置垂直间距
        lt_middle_top.setContentsMargins(10, 10, 10, 10)  #设置外间距
        lt_middle_top.setColumnStretch(12, 1)             #设置列宽，添加空白项的
        gp_middle_top.setLayout(lt_middle_top)
        ##############
        gp_middle_middle = QGroupBox('报告信息')
        lt_middle_middle = QHBoxLayout()
        self.lb_bgsy = Lable()
        self.lb_bgdy = Lable()
        self.lb_bgzl = Lable()
        self.lb_bglq = Lable()
        lt_middle_middle.addWidget(QLabel('报告审阅：'))
        lt_middle_middle.addWidget(self.lb_bgsy)
        lt_middle_middle.addWidget(QLabel('报告打印：'))
        lt_middle_middle.addWidget(self.lb_bgdy)
        lt_middle_middle.addStretch()
        gp_middle_middle.setLayout(lt_middle_middle)
        ##############
        self.gp_middle_bottom = QGroupBox('胶片信息(0)')
        lt_middle_bottom = QHBoxLayout()
        self.lb_count_dr = FilmLable()
        self.lb_count_ct = FilmLable()
        self.lb_count_mri = FilmLable()
        self.lb_count_rx = FilmLable()
        lt_middle_bottom.addWidget(QLabel('DR：'))
        lt_middle_bottom.addWidget(self.lb_count_dr)
        lt_middle_bottom.addSpacing(10)
        lt_middle_bottom.addWidget(QLabel('CT：'))
        lt_middle_bottom.addWidget(self.lb_count_ct)
        lt_middle_bottom.addSpacing(10)
        lt_middle_bottom.addWidget(QLabel('MRI：'))
        lt_middle_bottom.addWidget(self.lb_count_mri)
        lt_middle_bottom.addWidget(QLabel('钼靶：'))
        lt_middle_bottom.addWidget(self.lb_count_rx)
        lt_middle_bottom.addSpacing(10)
        lt_middle_bottom.addStretch()
        self.gp_middle_bottom.setLayout(lt_middle_bottom)
        ##############
        self.gp_middle_bottom2 = QGroupBox('手工单信息')
        lt_middle_bottom2 = QHBoxLayout()
        self.lb_manual = QLabel()
        self.lb_manual.setWordWrap(True)
        self.lb_manual.setStyleSheet('''color: rgb(0, 85, 255);''')
        lt_middle_bottom2.addWidget(self.lb_manual)
        self.gp_middle_bottom2.setLayout(lt_middle_bottom2)
        ####### 添加布局
        self.middle_layout.addWidget(gp_middle_top)
        self.middle_layout.addWidget(gp_middle_middle)
        self.middle_layout.addWidget(self.gp_middle_bottom)
        self.middle_layout.addWidget(self.gp_middle_bottom2)
        self.middle_layout.addStretch()
        ######################## 右 ################################
        lt_right_top = QHBoxLayout()
        gp_right_top = QGroupBox('检索条件')
        self.report_dwmc = TUint({}, {})  # 体检单位
        self.cb_qd = QCheckBox()
        self.cb_qd.setChecked(False)
        self.dg_qdrq = DateGroup(30)
        self.dg_qdrq.setNoChoice(True)

        self.btn_query = QPushButton(Icon('query'),'查询')
        self.btn_export = QPushButton(Icon('导出'), '导出')
        lt_right_top.addWidget(QLabel('单位名称：'))
        lt_right_top.addWidget(self.report_dwmc)
        lt_right_top.addWidget(self.cb_qd)
        lt_right_top.addLayout(self.dg_qdrq)
        lt_right_top.addWidget(self.btn_query)
        lt_right_top.addWidget(self.btn_export)
        gp_right_top.setLayout(lt_right_top)
        ################## 指标栏 ######################
        lt_right_middle = QHBoxLayout()
        self.gp_right_middle = QGroupBox('单位体检进度')
        self.table_report_progress_cols = OrderedDict([
            ('sum', '总数'),
            ('tjqx', '已取消'),
            ('tjdj', '已登记'),
            ('tjqd', '已签到'),
            ('tjzz', '追踪中'),
            ('tjzj', '已总检'),
            ('tjsh', '已审核'),
            ('tjsy', '已审阅'),
            ('tjdy', '已打印'),
            ('tjzl', '已整理'),
            ('tjlq', '已领取')
        ])
        self.table_report_progress = ReportProgressTable(self.table_report_progress_cols)
        # 添加布局
        lt_right_middle.addWidget(self.table_report_progress)
        self.gp_right_middle.setLayout(lt_right_middle)
        self.gp_right_middle.setMinimumHeight(120)
        self.gp_right_middle.setMaximumHeight(150)

        lt_right_bottom = QHBoxLayout()
        self.gp_right_bottom = QGroupBox('详细列表（0）')
        # 关注
        self.table_report_detail_cols = OrderedDict([
            ('tjbh', '体检编号'),
            ('xm', '姓名'),
            ('xb', '性别'),
            ('nl', '年龄'),
            ('ysje', '应收金额'),
            ('djrq', '登记日期'),
            ('qdrq', '签到日期'),
            ('zjrq', '总检日期'),
            ('shrq', '审核日期'),
            ('syrq', '三审日期'),
            ('dyrq', '打印日期'),
            ('zlrq', '整理日期'),
            ('lqrq', '领取日期'),
            ('dwmc', '单位名称')
        ])
        self.table_report_detail = ReportDetailTable(self.table_report_detail_cols)
        lt_right_bottom.addWidget(self.table_report_detail)
        self.gp_right_bottom.setLayout(lt_right_bottom)
        ############
        lt_right_btns = QHBoxLayout()
        self.gp_right_btns = QGroupBox()
        self.btn_review = ToolButton(Icon('全屏'), '报告审阅')
        self.btn_view = ToolButton(Icon('预览'), '报告预览')
        self.btn_print = ToolButton(Icon('报告打印'), '报告打印')
        self.btn_down = ToolButton(Icon('down'), '报告下载')
        self.btn_order = ToolButton(Icon('报告整理'), '报告整理')
        self.btn_receive = ToolButton(Icon('报告领取'), '报告领取')
        lt_right_btns.addWidget(self.btn_review)
        lt_right_btns.addSpacing(10)
        lt_right_btns.addWidget(self.btn_view)
        lt_right_btns.addSpacing(10)
        lt_right_btns.addWidget(self.btn_print)
        lt_right_btns.addSpacing(10)
        lt_right_btns.addWidget(self.btn_down)
        lt_right_btns.addSpacing(10)
        lt_right_btns.addWidget(self.btn_order)
        lt_right_btns.addSpacing(10)
        lt_right_btns.addWidget(self.btn_receive)
        lt_right_btns.addSpacing(10)
        lt_right_btns.addStretch()
        self.gp_right_btns.setLayout(lt_right_btns)
        # 添加布局
        self.right_layout.addWidget(gp_right_top)
        self.right_layout.addWidget(self.gp_right_middle)
        self.right_layout.addWidget(self.gp_right_bottom)
        self.right_layout.addWidget(self.gp_right_btns)

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
        self.setColumnWidth(1, 70)  # 体检编号
        self.setColumnWidth(2, 50)  # 姓名
        # self.horizontalHeader().setStretchLastSection(True)


class PicLable(QLabel):

    def __init__(self):
        super(PicLable,self).__init__()
        self.setText('身\n份\n证\n照\n片')
        self.setAlignment(Qt.AlignCenter)
        # 一寸照大小
        self.setFixedWidth(102)
        self.setFixedHeight(126)
        self.setFrameShape(QFrame.Box)
        self.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);")

    def show2(self,datas):
        # write_file(datas, filename)
        p = QPixmap()
        p.loadFromData(datas)          # 数据不落地,高效
        self.setPixmap(p)

class FilmLable(QLabel):

    def __init__(self):
        super(FilmLable,self).__init__()
        # self.setMinimumWidth(50)
        self.setStyleSheet('''font: 75 14pt \"微软雅黑\";color: rgb(0, 85, 255);''')