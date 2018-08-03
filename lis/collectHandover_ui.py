from widgets.cwidget import *

class CollectHandover_UI(Widget):

    def __init__(self):

        super(CollectHandover_UI,self).__init__()
        self.initUI()

    # 初始化界面
    def initUI(self):
        lt_main = QVBoxLayout()                    # 主布局
        lt_top = QHBoxLayout()                     # 上布局
        lt_bottom = QHBoxLayout()                  # 下布局

        ############ 上布局 ########################
        gp_where_search = QGroupBox('条件检索')
        lt_where_search = QGridLayout()

        self.collect_time = DateTimeGroup()
        self.collect_user = UserCombox()
        self.collect_user.addItems(['配送大叔','%s'%self.login_name,'顾客'])
        self.collect_area = CollectAreaGroup(['明州','明州1楼','明州2楼','明州3楼','江东'])
        self.collect_area.set_area(self.login_area)

        self.btn_query = ToolButton(Icon('query'),'查询')
        self.btn_export = ToolButton(Icon('导出'), '导出')
        self.btn_handover = ToolButton(Icon('样本交接'), '样本交接')
        self.btn_receive = ToolButton(Icon('样本签收'), '样本签收')
        #self.btn_export.clicked.connect(self.on_btn_export)
        # 子布局 左
        lt_where_search.addItem(self.collect_time, 0, 0, 1, 5)
        lt_where_search.addWidget(QLabel('送检人员：'), 1, 0, 1, 1)
        lt_where_search.addWidget(self.collect_user, 1, 1, 1, 1)
        # lt_where_search.addWidget(QLabel('操作区域：'), 1, 2, 1, 1)
        lt_where_search.addItem(self.collect_area, 1, 2, 1, 2)
        lt_where_search.addWidget(self.btn_query, 0, 5, 2, 2)
        lt_where_search.addWidget(self.btn_export, 0, 7, 2, 2)
        lt_where_search.addWidget(self.btn_handover, 0, 9, 2, 2)
        lt_where_search.addWidget(self.btn_receive, 0, 11, 2, 2)
        lt_where_search.setHorizontalSpacing(10)            #设置水平间距
        lt_where_search.setVerticalSpacing(10)              #设置垂直间距
        lt_where_search.setContentsMargins(10, 10, 10, 10)  #设置外间距
        lt_where_search.setColumnStretch(11, 1)             #设置列宽，添加空白项的

        gp_where_search.setLayout(lt_where_search)
        # 子布局 右
        self.gp_quick_search = QuickSearchGroup()

        # 添加布局
        lt_top.addWidget(gp_where_search)
        lt_top.addWidget(self.gp_quick_search)
        ############ 下布局 ########################
        self.collect_cols = OrderedDict([
                                ("QSSJ", "开始时间"),
                                ("JSSJ", "结束时间"),
                                ("CZQY", "采集区域"),
                                ("SGYS", "试管颜色"),
                                ("SGSL", "试管数量"),
                                ("jjxm", "交接护士"),
                                ("jjsj", "交接时间"),
                                ("sjxm", "送检人员"),
                                ("qsxm", "签收人员"),
                                ("qssj", "签收时间"),
                            ])
        self.collect_detail_cols = OrderedDict([
                                ("tjbh", "体检编号"),
                                ("mxbh", "条码号"),
                                ("czsj", "采集时间"),
                                ("czqy", "采集区域"),
                                ("czxm", "采集区域"),
                                ("jlnr", "样本项目")
                            ])
        # 汇总
        self.table_handover_master = CollectHandoverTable(self.collect_cols)
        self.gp_bottom_left = QGroupBox('样本交接汇总')
        lt_bottom_left = QHBoxLayout()
        lt_bottom_left.addWidget(self.table_handover_master)
        self.gp_bottom_left.setLayout(lt_bottom_left)
        # 详细
        self.table_handover_detail = CollectHandoverDTable(self.collect_detail_cols)
        self.table_handover_detail.verticalHeader().setVisible(False)  # 列表头
        self.table_handover_detail.horizontalHeader().setStretchLastSection(True)
        self.gp_bottom_right = QGroupBox('样本交接详细')
        lt_bottom_right = QHBoxLayout()
        lt_bottom_right.addWidget(self.table_handover_detail)
        self.gp_bottom_right.setLayout(lt_bottom_right)

        #self.table_history.verticalHeader().setVisible(False)  # 去掉行头
        # 设置列宽
        # self.table_handover.setColumnWidth(0, 40)
        # self.table_handover.setColumnWidth(5, 150)
        lt_bottom.addWidget(self.gp_bottom_left,3)
        lt_bottom.addWidget(self.gp_bottom_right,2)

        # 添加主布局
        lt_main.addLayout(lt_top)
        lt_main.addLayout(lt_bottom)
        self.setLayout(lt_main)
