from widgets.cwidget import *

# 报告追踪
class ReportTrackUI(Widget):

    def __init__(self):
        super(ReportTrackUI, self).__init__()
        self.initUI()

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_top = QHBoxLayout()
        lt_middle = QHBoxLayout()
        self.gp_middle = QGroupBox('追踪列表（0）')
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox()
        #############################################
        gp_search = QGroupBox('条件检索')

        self.btn_query = ToolButton(Icon('query'),'查询')
        self.btn_task = ToolButton(Icon('任务'), '领取')
        self.btn_myself = ToolButton(Icon('user'),'我的')
        self.btn_export = ToolButton(Icon('导出'), '导出')
        self.btn_receive = ToolButton(Icon('接收'),'结果接收')
        # 追踪类型
        self.cb_track_type = TrackTypeGroup()
        # 报告类型
        self.cb_report_type = ReportTypeGroup()
        # 报告追踪人员
        self.cb_report_track_person = UserGroup('追踪人员：')
        self.cb_report_track_person.addUsers(['所有',self.login_name])
        # 报告追踪时效
        self.cb_report_track_timerout = ReportTrackTimeroutGroup()
        # 加入布局
        self.lt_where_search = WhereSearchGroup()
        self.lt_where_search.addStates(['待追踪','追踪中','追踪完成'],True)
        self.lt_where_search.addWidget(QLabel(), 0, 4, 1, 1)
        self.lt_where_search.addItem(self.cb_track_type, 0, 5, 1, 2)
        self.lt_where_search.addItem(self.cb_report_type, 0, 7, 1, 2)
        # self.lt_where_search.addItem(self.cb_report_track_person, 0, 9, 1, 2)
        # self.lt_where_search.addItem(self.cb_report_track_timerout, 1, 9, 1, 2)
        # 按钮
        self.lt_where_search.addWidget(self.btn_query, 0, 11, 2, 2)
        self.lt_where_search.addWidget(self.btn_task, 0, 13, 2, 2)
        # self.lt_where_search.addWidget(self.btn_myself, 0, 15, 2, 2)
        self.lt_where_search.addWidget(self.btn_export, 0, 17, 2, 2)
        gp_search.setLayout(self.lt_where_search)

        # 快速检索
        self.gp_quick_search = QuickSearchGroup()


        # 上布局
        lt_top.addWidget(gp_search)
        lt_top.addWidget(self.gp_quick_search)
        ##########################################
        self.table_track_cols = OrderedDict([('XMZQ', '结果周期'),
                                             ('zzjd', '追踪进度'),
                                             ('zzzt', '追踪状态'),
                                             ('lqry', '追踪人'),
                                             ('tjzt','体检状态'),
                                             ('tjlx','类型'),
                                             ('tjqy','区域'),
                                             ('tjbh','体检编号'),
                                             ('xm','姓名'),
                                             ('xb','性别'),
                                             ('nl','年龄'),
                                             ('sfzh', '身份证号'),
                                             ('sjhm','手机号码'),
                                             ('dwmc', '单位名称'),
                                             ('qdrq', '签到日期'),
                                             ('wjxm', '未结束项目/退回原因')
                                            ])

        self.table_track = ReportTrackTable(self.table_track_cols)
        self.table_track.verticalHeader().setVisible(False)  # 列表头
        lt_middle.addWidget(self.table_track)
        self.gp_middle.setLayout(lt_middle)

        # 按钮功能区
        self.btn_item = QPushButton(Icon('项目'), '项目查看')         # 查看 LIS 结果
        self.btn_lis = QPushButton(Icon('lis'),'检验系统')            # 查看 LIS 结果
        self.btn_pacs = QPushButton(Icon('pacs'),'检查系统')          # 查看 PACS 结果
        self.btn_pis = QPushButton(Icon('pis'),'病理系统')            # 查看 病理结果
        self.btn_equip = QPushButton(Icon('pis'), '设备系统')         # 查看 病理结果
        self.btn_phone = QPushButton(Icon('电话'),'电话记录')       # 查看电话记录
        self.btn_sms = QPushButton(Icon('短信'),'短信记录')         # 查看短信记录
        self.btn_sd = QPushButton(Icon('体检收单'),'导检收单')      # 导检收单
        self.btn_djd = QPushButton(Icon('体检收单'),'纸质导检单')   # 有拒检项目查看电子导检单
        lt_bottom.addWidget(self.btn_item)
        lt_bottom.addWidget(self.btn_lis)
        lt_bottom.addWidget(self.btn_pacs)
        lt_bottom.addWidget(self.btn_pis)
        # lt_bottom.addWidget(self.btn_equip)
        lt_bottom.addWidget(self.btn_phone)
        lt_bottom.addWidget(self.btn_sms)
        # lt_bottom.addWidget(self.btn_sd)
        lt_bottom.addWidget(self.btn_djd)
        gp_bottom.setLayout(lt_bottom)
        # 整体布局
        lt_main.addLayout(lt_top)
        lt_main.addWidget(self.gp_middle)
        lt_main.addWidget(gp_bottom)

        self.setLayout(lt_main)

