from widgets.cwidget import *

class CollectHandover_UI(Widget):

    def __init__(self):

        super(CollectHandover_UI,self).__init__()
        self.initUI()

    # 初始化界面
    def initUI(self):
        lt_main = QVBoxLayout()                    # 主布局
        lt_top = QHBoxLayout()                     # 上布局
        lt_bottom = QVBoxLayout()                  # 下布局

        ############ 上布局 ########################
        gp_where_search = QGroupBox('条件检索')
        lt_where_search = QGridLayout()

        self.collect_time = DateTimeGroup()
        self.collect_user = UserCombox()
        self.collect_user.addItems(['配送大叔','%s'%self.login_name])
        self.collect_user2 = UserCombox()
        self.collect_user2.addItems(['%s'%self.login_name,'所有'])
        self.collect_area = CollectAreaGroup(['明州','明州1楼','明州2楼','明州3楼','明州贵宾','江东'])
        self.collect_area.set_area(self.login_area)

        self.btn_query = ToolButton(Icon('query'),'查询')
        self.btn_export = ToolButton(Icon('导出'), '导出')
        self.btn_handover = ToolButton(Icon('样本交接'), '样本交接')
        self.btn_receive = ToolButton(Icon('样本签收'), '样本签收')
        #self.btn_export.clicked.connect(self.on_btn_export)
        # 子布局 左
        lt_where_search.addItem(self.collect_time, 0, 0, 1, 6)
        lt_where_search.addWidget(QLabel('送检人员：'), 1, 0, 1, 1)
        lt_where_search.addWidget(self.collect_user, 1, 1, 1, 1)
        lt_where_search.addItem(self.collect_area, 1, 2, 1, 2)
        lt_where_search.addWidget(QLabel('采集护士：'), 1, 4, 1, 1)
        lt_where_search.addWidget(self.collect_user2, 1, 5, 1, 1)
        lt_where_search.addWidget(self.btn_query, 0, 6, 2, 2)
        lt_where_search.addWidget(self.btn_export, 0, 8, 2, 2)
        lt_where_search.addWidget(self.btn_handover, 0,10, 2, 2)
        lt_where_search.addWidget(self.btn_receive, 0, 12, 2, 2)
        lt_where_search.setHorizontalSpacing(10)            #设置水平间距
        lt_where_search.setVerticalSpacing(10)              #设置垂直间距
        lt_where_search.setContentsMargins(10, 10, 10, 10)  #设置外间距
        lt_where_search.setColumnStretch(12, 1)             #设置列宽，添加空白项的

        gp_where_search.setLayout(lt_where_search)
        # 子布局 右
        self.gp_quick_search = QuickSearchGroup()

        # 添加布局
        lt_top.addWidget(gp_where_search)
        # lt_top.addWidget(self.gp_quick_search)
        lt_middle = QHBoxLayout()
        ############ 中间局 ########################
        self.collect_sum_cols = OrderedDict([
                                ("ybzt", "状态"),
                                ("SGYS", "试管"),
                                ("SGSL", "数量")
                            ])
        self.collect_cols = OrderedDict([
                                ("QSSJ", "开始时间"),
                                ("JSSJ", "结束时间"),
                                ("CZQY", "区域"),
                                ("SGYS", "试管"),
                                ("SGSL", "数量"),
                                ("jjxm", "交接护士"),
                                ("jjsj", "交接时间"),
                                ("qsxm", "签收人员"),
                                ("qssj", "签收时间"),
                            ])
        self.collect_detail_cols = OrderedDict([
                                ("tjbh", "体检编号"),
                                ("mxbh", "条码号"),
                                ("czsj", "采集时间"),
                                ("czqy", "采集区域"),
                                ("czxm", "采集护士"),
                                ("jlnr", "项目明细")
                            ])
        # 样本处理记录
        self.table_handover = CollectHandoverSTable(self.collect_sum_cols)
        self.gp_middle_left = QGroupBox('样本汇总')
        lt_middle_left = QVBoxLayout()
        lt_middle_left.addWidget(self.table_handover)
        self.gp_middle_left.setLayout(lt_middle_left)
        # 交接签收
        self.table_handover_master = CollectHandoverTable(self.collect_cols)
        self.gp_middle_middle = QGroupBox('样本交接签收')
        lt_middle_middle = QVBoxLayout()
        lt_middle_middle.addWidget(self.table_handover_master)
        self.gp_middle_middle.setLayout(lt_middle_middle)


        # 详细
        self.table_handover_detail = CollectHandoverDTable(self.collect_detail_cols)
        self.table_handover_detail.verticalHeader().setVisible(False)  # 列表头
        self.table_handover_detail.horizontalHeader().setStretchLastSection(True)
        self.gp_middle_right = QGroupBox('样本采集明细(0)')
        lt_middle_right = QHBoxLayout()
        lt_middle_right.addWidget(self.table_handover_detail)
        self.gp_middle_right.setLayout(lt_middle_right)
        ######### 添加中间布局
        lt_middle.addWidget(self.gp_middle_left)
        lt_middle.addWidget(self.gp_middle_middle)
        lt_middle.addWidget(self.gp_middle_right)
        # lt_middle.addStretch()
        ################################################################
        gp_sample_jj_sum = QGroupBox('样本待交接信息')
        gp_sample_jj_sum.setStyleSheet('''QGroupBox:title{font: 75 14pt '微软雅黑';color: rgb(0,128,0);}''')
        gp_sample_jj_sum.setMinimumHeight(50)
        self.lt_sample_jj_sum = FlowLayout(gp_sample_jj_sum,10,5)
        gp_sample_jj_sum.setLayout(self.lt_sample_jj_sum)

        gp_sample_qs_sum = QGroupBox('样本待签收信息')
        gp_sample_qs_sum.setStyleSheet('''QGroupBox:title{font: 75 14pt '微软雅黑';color: rgb(0,128,0);}''')
        gp_sample_qs_sum.setMinimumHeight(50)
        self.lt_sample_qs_sum = FlowLayout()
        gp_sample_qs_sum.setLayout(self.lt_sample_qs_sum)

        gp_sample_sum = QGroupBox('样本完成信息')
        gp_sample_sum.setStyleSheet('''QGroupBox:title{font: 75 14pt '微软雅黑';color: rgb(0,128,0);}''')
        gp_sample_sum.setMinimumHeight(50)
        self.lt_sample_sum = FlowLayout()
        gp_sample_sum.setLayout(self.lt_sample_sum)
        #self.table_history.verticalHeader().setVisible(False)  # 去掉行头
        # 设置列宽
        # self.table_handover.setColumnWidth(0, 40)
        # self.table_handover.setColumnWidth(5, 150)
        lt_bottom.addSpacing(10)
        lt_bottom.addWidget(gp_sample_jj_sum)
        lt_bottom.addSpacing(10)
        lt_bottom.addWidget(gp_sample_qs_sum)
        lt_bottom.addSpacing(10)
        lt_bottom.addWidget(gp_sample_sum)
        # self.gp_bottom_left.setLayout(lt_bottom_left)

        # 添加主布局
        lt_main.addLayout(lt_top)
        lt_main.addLayout(lt_middle)
        lt_main.addLayout(lt_bottom)
        self.setLayout(lt_main)
