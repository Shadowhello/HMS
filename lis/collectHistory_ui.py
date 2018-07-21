from widgets.cwidget import *

class CollectHistory_UI(Widget):

    def __init__(self):

        super(CollectHistory_UI,self).__init__()
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
        self.collect_area = AreaGroup()

        self.btn_query = ToolButton(Icon('query'),'查询')
        self.btn_export = ToolButton(Icon('导出'), '导出')
        #self.btn_export.clicked.connect(self.on_btn_export)
        # 子布局 左
        lt_where_search.addItem(self.collect_time, 0, 0, 1, 5)
        lt_where_search.addWidget(QLabel('操作人员：'), 1, 0, 1, 1)
        lt_where_search.addWidget(self.collect_user, 1, 1, 1, 1)
        # lt_where_search.addWidget(QLabel('操作区域：'), 1, 2, 1, 1)
        lt_where_search.addItem(self.collect_area, 1, 2, 1, 2)
        lt_where_search.addWidget(self.btn_query, 0, 5, 2, 2)
        lt_where_search.addWidget(self.btn_export, 0, 7, 2, 2)

        lt_where_search.setHorizontalSpacing(10)            #设置水平间距
        lt_where_search.setVerticalSpacing(10)              #设置垂直间距
        lt_where_search.setContentsMargins(10, 10, 10, 10)  #设置外间距
        lt_where_search.setColumnStretch(11, 1)             #设置列宽，添加空白项的

        gp_where_search.setLayout(lt_where_search)
        # 子布局 右
        gp_quick_search = QGroupBox('快速检索')
        lt_quick_search = QHBoxLayout()
        gp_quick_search.setLayout(lt_quick_search)

        # 添加布局
        lt_top.addWidget(gp_where_search)
        lt_top.addWidget(gp_quick_search)
        ############ 下布局 ########################
        self.collect_cols = OrderedDict([
                                ("zt", '状态'),
                                ("jllx", "样本类型"),
                                ("tjbh", "体检编号"),
                                ("tmbh", "条码号"),
                                ("czxm", "采集人员"),
                                ("czsj", "采集时间"),
                                ("czqy", "采集区域"),
                                ("jjxm", "交接护士"),
                                ("sjxm", "送检人员"),
                                ("sjsj", "送检时间"),
                                ("qsxm", "签收人员"),
                                ("qssj", "签收时间"),
                                ("ck", "")
                            ])
        self.table_history = CollectHistoryTable(self.collect_cols)
        #self.table_history.verticalHeader().setVisible(False)  # 去掉行头
        # 设置列宽
        self.table_history.setColumnWidth(0, 40)
        self.table_history.setColumnWidth(5, 150)

        lt_bottom.addWidget(self.table_history)


        # 添加主布局
        lt_main.addLayout(lt_top)
        lt_main.addLayout(lt_bottom)
        self.setLayout(lt_main)



