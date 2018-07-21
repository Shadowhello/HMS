from widgets.cwidget import *
from mbgl.model import *
from functools import partial


# 四高+甲状腺结节 疑似筛选
class Doubtful(Widget):

    def __init__(self):
        super(Doubtful,self).__init__()
        self.initParas()
        self.initUI()


    def initParas(self):
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()

        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)

        # results = self.session.query(MT_MB_YSKH).filter(MT_MB_YSKH.qdrq == '2018-06-30').all()
        # tmp = [result.to_dict for result in results]
        # self.table.load(tmp)

        ###################################################
        self.where_jb = ''
        self.where_rq = ''
        self.where_je = ''

    def initUI(self):
        main_layout = QVBoxLayout()
        lt_top = QHBoxLayout()
        lt_bottom = QHBoxLayout()
        search_group = QGroupBox('条件检索')
        search_layout = QGridLayout()

        self.cb_is_gxy = QCheckBox('疑似高血压')
        self.cb_is_gxz = QCheckBox('疑似高血脂')
        self.cb_is_gxt = QCheckBox('疑似高血糖')
        self.cb_is_gns = QCheckBox('疑似高尿酸')
        self.cb_is_jzx = QCheckBox('疑似甲状腺')

        self.cb_is_gxy.stateChanged.connect(partial(self.onCheckState, '高血压'))
        self.cb_is_gxz.stateChanged.connect(partial(self.onCheckState, '高血脂'))
        self.cb_is_gxt.stateChanged.connect(partial(self.onCheckState, '高血糖'))
        self.cb_is_gns.stateChanged.connect(partial(self.onCheckState, '高尿酸'))
        self.cb_is_jzx.stateChanged.connect(partial(self.onCheckState, '甲状腺'))

        self.dg_rq = DateGroup()       # 检索时间
        self.mg_je = MoneyGroup()      # 检索金额
        self.tj_dw = TUintGroup(self.dwmc_bh,self.dwmc_py)       # 体检单位

        self.btn_query = ToolButton(Icon('query'),'查询')
        self.btn_export = ToolButton(Icon('导出'), '导出')
        self.btn_export.clicked.connect(self.on_btn_export)

        self.btn_query.setFixedWidth(64)
        self.btn_query.setFixedHeight(64)
        self.btn_query.setAutoRaise(False)
        self.btn_export.setFixedWidth(64)
        self.btn_export.setFixedHeight(64)
        self.btn_export.setAutoRaise(False)

        # 第一列
        search_layout.addWidget(self.cb_is_gxy, 0, 0, 1, 1)
        search_layout.addItem(self.tj_dw, 1, 0, 1, 5)
        # 第二列
        search_layout.addWidget(self.cb_is_gxt, 0, 1, 1, 1)

        # 第三列
        search_layout.addWidget(self.cb_is_jzx, 0, 2, 1, 1)
        # 第四列
        search_layout.addWidget(self.cb_is_gxz, 0, 3, 1, 1)
        # 第五列
        search_layout.addWidget(self.cb_is_gns, 0, 4, 1, 1)
        # 第六列
        search_layout.addItem(self.dg_rq, 0, 5, 1, 4)
        search_layout.addItem(self.mg_je, 1, 5, 1, 4)


        search_layout.addWidget(self.btn_query, 0, 9, 2, 2)

        search_layout.addWidget(self.btn_export, 0, 11, 2, 2)

        search_layout.setHorizontalSpacing(10)            #设置水平间距
        search_layout.setVerticalSpacing(10)              #设置垂直间距
        search_layout.setContentsMargins(10, 10, 10, 10)  #设置外间距
        search_layout.setColumnStretch(11, 1)             #设置列宽，添加空白项的

        search_group.setLayout(search_layout)

        search_group2 = QGroupBox('快速检索')
        search_layout2 = QuickSearchGroup()
        search_group2.setLayout(search_layout2)
        self.cols = OrderedDict([('tjbh','体检编号'),
                                 ('xm','姓名'),
                                 ('xb','性别'),
                                 ('nl','年龄'),
                                 ('sjhm','手机号码'),
                                 ('sfzh','身份证号'),
                                 ('ysje','体检金额'),
                                 ('is_gxy','疑似高血压'),
                                 ('is_gxz', '疑似高血脂'),
                                 ('is_gxt', '疑似高血糖'),
                                 ('is_gns', '疑似高尿酸'),
                                 ('is_jzx', '疑似甲状腺'),
                                 ('glu', '血糖'),
                                 ('glu2', '餐后2小时血糖'),
                                 ('hbalc', '糖化血红蛋白'),
                                 ('ua', '尿酸'),
                                 ('tch', '总胆固醇'),
                                 ('tg', '甘油三酯'),
                                 ('hdl', '高密度脂蛋白'),
                                 ('ldl', '低密度脂蛋白'),
                                 ('hbp', '收缩压'),
                                 ('lbp', '舒张压'),
                                 ('dwmc', '单位名称')
                                 ])
        self.table = SlowHealthTable(self.cols)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)              ######允许右键产生子菜单
        self.table.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单


        lt_bottom.addWidget(self.table)

        lt_top.addWidget(search_group)
        lt_top.addWidget(search_group2)

        main_layout.addLayout(lt_top)
        #main_layout.addStretch()
        main_layout.addLayout(lt_bottom)
        self.setLayout(main_layout)

    def onCheckState(self,p_str,is_check:int):

        print(is_check,p_str)

    # 查询
    def on_btn_query(self):
        pass

    # 导出功能
    def on_btn_export(self):
        self.table.export()

    # 右键功能
    def onTableMenu(self,pos):
        row_num = -1
        indexs=self.table.selectionModel().selection().indexes()
        if indexs:
            for i in indexs:
                row_num = i.row()

            menu = QMenu()
            item1 = menu.addAction(Icon("短信"), "发送预约短信")
            item2 = menu.addAction(Icon("短信"), "编辑预约短信")
            item3 = menu.addAction(Icon("预约"), "设置预约客户")
            item4 = menu.addAction(Icon("预约"), "电话记录")
            item5 = menu.addAction(Icon("预约"), "本次体检结果")
            item6 = menu.addAction(Icon("预约"), "历年体检结果")
            item7 = menu.addAction(Icon("预约"), "浏览体检报告")
            item8 = menu.addAction(Icon("预约"), "下载电子报告")

            action = menu.exec_(self.table.mapToGlobal(pos))
