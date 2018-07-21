from widgets.cwidget import *



# 报告追踪
class ReportTrackUI(Widget):

    def __init__(self):
        super(ReportTrackUI, self).__init__()
        self.initUI()

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_top = QHBoxLayout()
        lt_bottom = QHBoxLayout()
        #############################################
        gp_search = QGroupBox('条件检索')

        self.btn_query = ToolButton(Icon('query'),'查询')
        self.btn_export = ToolButton(Icon('导出'), '导出')
        # 追踪类型
        self.cb_track_type = TrackTypeGroup()
        # 报告类型
        self.cb_report_type = ReportTypeGroup()

        self.lt_search = WhereSearchGroup()
        self.lt_search.addWidget(QLabel(), 0, 4, 1, 1)
        self.lt_search.addItem(self.cb_track_type, 0, 5, 1, 2)
        self.lt_search.addItem(self.cb_report_type, 0, 7, 1, 2)
        self.lt_search.addWidget(self.btn_query, 0, 9, 2, 2)
        self.lt_search.addWidget(self.btn_export, 0, 11, 2, 2)

        gp_search.setLayout(self.lt_search)

        gp_search2 = QGroupBox('快速检索')
        self.lt_search2 = QuickSearchGroup()
        gp_search2.setLayout(self.lt_search2)

        # 上布局
        lt_top.addWidget(gp_search)
        lt_top.addWidget(gp_search2)
        ##########################################
        self.table_track_cols = OrderedDict([('tjzq','待追踪时长'),
                                             ('tjzx','状态'),
                                             ('tjlx','客户类型'),
                                             ('tjbh','体检编号'),
                                             ('xm','姓名'),
                                             ('xb','性别'),
                                             ('nl','年龄'),
                                             ('sjhm','手机号码'),
                                             ('sfzh','身份证号'),
                                             ('wjxm', '未结束项目'),
                                             ('bz', '说明'),
                                             ('ysje','体检金额'),
                                             ('dwmc', '单位名称'),
                                             ('depart', '部门')
                                            ])

        self.table_track = ReportTrackTable(self.table_track_cols)

        lt_bottom.addWidget(self.table_track)

        # 按钮功能区
        self.btn_lis = QPushButton()      #查看
        self.btn_pacs = QPushButton()
        self.btn_pis = QPushButton()
        self.btn_lis = QPushButton()

        # 整体布局
        lt_main.addLayout(lt_top)
        lt_main.addLayout(lt_bottom)

        self.setLayout(lt_main)
