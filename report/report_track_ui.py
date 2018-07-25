from widgets.cwidget import *
from report.model import *



# 报告追踪
class ReportTrackUI(Widget):

    def __init__(self):
        super(ReportTrackUI, self).__init__()
        self.initUI()

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_top = QHBoxLayout()
        lt_middle = QHBoxLayout()
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox()
        #############################################
        gp_search = QGroupBox('条件检索')

        self.btn_query = ToolButton(Icon('query'),'查询')
        self.btn_export = ToolButton(Icon('导出'), '导出')
        # 追踪类型
        self.cb_track_type = TrackTypeGroup()
        # 报告类型
        self.cb_report_type = ReportTypeGroup()

        self.lt_where_search = WhereSearchGroup()
        self.lt_where_search.addWidget(QLabel(), 0, 4, 1, 1)
        self.lt_where_search.addItem(self.cb_track_type, 0, 5, 1, 2)
        self.lt_where_search.addItem(self.cb_report_type, 0, 7, 1, 2)
        self.lt_where_search.addWidget(self.btn_query, 0, 9, 2, 2)
        self.lt_where_search.addWidget(self.btn_export, 0, 11, 2, 2)

        gp_search.setLayout(self.lt_where_search)

        gp_search2 = QGroupBox('快速检索')
        self.lt_quick_search = QuickSearchGroup()
        gp_search2.setLayout(self.lt_quick_search)

        # 上布局
        lt_top.addWidget(gp_search)
        lt_top.addWidget(gp_search2)
        ##########################################
        self.table_track_cols = OrderedDict([('tjzt','体检状态'),
                                             ('tjlx','客户类型'),
                                             ('tjqy','体检区域'),
                                             ('tjbh','体检编号'),
                                             ('xm','姓名'),
                                             ('xb','性别'),
                                             ('nl','年龄'),
                                             ('sfzh', '身份证号'),
                                             ('sjhm','手机号码'),
                                             ('dwmc', '单位名称'),
                                             ('depart', '部门'),
                                             ('qdrq', '签到日期'),
                                             ('wjxm', '未结束项目')
                                            ])

        self.table_track = ReportTrackTable(self.table_track_cols)
        lt_middle.addWidget(self.table_track)

        # 按钮功能区
        self.btn_item = QPushButton(Icon('项目'), '项目查看')  # 查看 LIS 结果
        self.btn_lis = QPushButton(Icon('lis'),'检验系统')          # 查看 LIS 结果
        self.btn_pacs = QPushButton(Icon('pacs'),'检查系统')        # 查看 PACS 结果
        self.btn_pis = QPushButton(Icon('pis'),'病理系统')          # 查看 病理结果
        self.btn_equip = QPushButton(Icon('pis'), '设备系统')  # 查看 病理结果
        self.btn_phone = QPushButton(Icon('电话'),'电话记录')       # 查看电话记录
        self.btn_mes = QPushButton(Icon('短信'),'短信记录')         # 查看短信记录
        self.btn_sd = QPushButton(Icon('体检收单'),'导检收单')      # 导检收单
        self.btn_djd = QPushButton(Icon('体检收单'),'电子导检单')   # 有拒检项目查看电子导检单
        lt_bottom.addWidget(self.btn_item)
        lt_bottom.addWidget(self.btn_lis)
        lt_bottom.addWidget(self.btn_pacs)
        lt_bottom.addWidget(self.btn_pis)
        lt_bottom.addWidget(self.btn_equip)
        lt_bottom.addWidget(self.btn_phone)
        lt_bottom.addWidget(self.btn_mes)
        lt_bottom.addWidget(self.btn_sd)
        lt_bottom.addWidget(self.btn_djd)
        gp_bottom.setLayout(lt_bottom)
        # 整体布局
        lt_main.addLayout(lt_top)
        lt_main.addLayout(lt_middle)
        lt_main.addWidget(gp_bottom)

        self.setLayout(lt_main)



