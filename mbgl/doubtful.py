from widgets.cwidget import *
from mbgl.model import *
from functools import partial


# 四高+甲状腺结节 疑似筛选
class Doubtful(Widget):

    def __init__(self):
        super(Doubtful,self).__init__()
        self.initParas()
        self.initUI()
        # 绑定信号
        self.cb_is_gxy.stateChanged.connect(partial(self.onCheckState, 'IS_GXY'))
        self.cb_is_gxz.stateChanged.connect(partial(self.onCheckState, 'IS_GXZ'))
        self.cb_is_gxt.stateChanged.connect(partial(self.onCheckState, 'IS_GXT'))
        self.cb_is_gns.stateChanged.connect(partial(self.onCheckState, 'IS_GNS'))
        self.cb_is_jzx.stateChanged.connect(partial(self.onCheckState, 'IS_JZX'))
        #
        self.gp_quick_search.returnPressed.connect(self.on_quick_search)  # 快速检索
        self.table.itemClicked.connect(self.on_table_set)
        self.btn_export.clicked.connect(self.on_btn_export_click)
        self.btn_query.clicked.connect(self.on_btn_query)

    def initParas(self):
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()

        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)

        ###################################################
        self.where_jb = {}
        self.where_rq = ''
        self.where_je = ''

    # 设置快速检索文本
    def on_table_set(self, tableWidgetItem):
        row = tableWidgetItem.row()
        tjbh = self.table.item(row, 0).text()
        xm = self.table.item(row, 1).text()
        sfzh = self.table.item(row, 5).text()
        sjhm = self.table.item(row, 4).text()
        self.gp_quick_search.setText(tjbh, xm, sjhm, sfzh)

    #快速检索
    def on_quick_search(self,p1_str,p2_str):
        if p1_str == 'tjbh':
            results = self.session.query(MT_MB_YSKH).filter(MT_MB_YSKH.tjbh == p2_str).all()
        elif p1_str == 'sjhm':
            results = self.session.query(MT_MB_YSKH).filter(MT_MB_YSKH.sjhm == p2_str).all()
        elif p1_str == 'sfzh':
            results = self.session.query(MT_MB_YSKH).filter(MT_MB_YSKH.sfzh == p2_str).all()
        else:
            results = self.session.query(MT_MB_YSKH).filter(MT_MB_YSKH.xm == p2_str).all()
        tmp = [result.to_dict for result in results]
        self.table.load(tmp)
        mes_about(self,'共检索出 %s 条数据！' %self.table.rowCount())

    # 导出功能
    def on_btn_export_click(self):
        self.table.export()

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_top = QHBoxLayout()
        search_group = QGroupBox('条件检索')
        search_layout = QGridLayout()

        self.cb_is_gxy = QCheckBox('疑似高血压')
        self.cb_is_gxz = QCheckBox('疑似高血脂')
        self.cb_is_gxt = QCheckBox('疑似高血糖')
        self.cb_is_gns = QCheckBox('疑似高尿酸')
        self.cb_is_jzx = QCheckBox('疑似甲状腺')



        self.dg_rq = DateGroup()       # 检索时间
        self.dg_rq.jsrq.clear()
        self.dg_rq.jsrq.addItems(['签到日期','总检日期','审核日期'])
        self.mg_je = MoneyGroup()      # 检索金额
        self.tj_dw = TUintGroup(self.dwmc_bh,self.dwmc_py)       # 体检单位

        self.btn_query = ToolButton(Icon('query'),'查询')

        self.btn_query.setFixedWidth(64)
        self.btn_query.setFixedHeight(64)
        self.btn_query.setAutoRaise(False)
        # self.btn_export.setFixedWidth(64)
        # self.btn_export.setFixedHeight(64)
        # self.btn_export.setAutoRaise(False)

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

        search_layout.setHorizontalSpacing(10)            #设置水平间距
        search_layout.setVerticalSpacing(10)              #设置垂直间距
        search_layout.setContentsMargins(10, 10, 10, 10)  #设置外间距
        search_layout.setColumnStretch(11, 1)             #设置列宽，添加空白项的

        search_group.setLayout(search_layout)


        self.gp_quick_search = QuickSearchGroup()
        
        lt_top.addWidget(search_group)
        lt_top.addWidget(self.gp_quick_search)
        # lt_top.addStretch()

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
        #### 刷选表格 ###########################################
        self.table = SlowHealthTable(self.cols)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)              ######允许右键产生子菜单
        self.table.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单
        self.gp_middle = QGroupBox('疑似列表(0)')
        lt_middle = QHBoxLayout()
        lt_middle.addWidget(self.table)
        self.gp_middle.setLayout(lt_middle)
        ########### 功能区 #################
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox()
        # 按钮功能区
        self.btn_item = QPushButton(Icon('项目'), '项目查看')         # 查看 LIS 结果
        self.btn_czjl = QPushButton(Icon('操作'), '操作记录')         # 查看体检记录
        self.btn_his_visit = QPushButton(Icon('就诊'), '历史就诊')      # 查看历史就诊
        self.btn_cur_visit = QPushButton(Icon('就诊'), '预约就诊')      # 查看体检记录
        self.btn_phone = QPushButton(Icon('电话'),'电话记录')         # 查看电话记录
        self.btn_sms = QPushButton(Icon('短信'),'短信记录')           # 查看短信记录
        self.btn_export = QPushButton(Icon('导出'), '数据导出')       # 数据导出

        lt_bottom.addWidget(self.btn_item)
        lt_bottom.addWidget(self.btn_czjl)
        lt_bottom.addWidget(self.btn_his_visit)
        lt_bottom.addWidget(self.btn_cur_visit)
        lt_bottom.addWidget(self.btn_phone)
        lt_bottom.addWidget(self.btn_sms)
        lt_bottom.addWidget(self.btn_export)
        gp_bottom.setLayout(lt_bottom)
        # 添加布局
        lt_main.addLayout(lt_top)
        #lt_main.addStretch()
        lt_main.addWidget(self.gp_middle)
        lt_main.addWidget(gp_bottom)
        self.setLayout(lt_main)

    def onCheckState(self,p_str,is_check:int):
        if is_check == 2:
            # 添加
            self.where_jb[p_str] = '1'
        elif is_check == 0:
            if p_str in list(self.where_jb.keys()):
                self.where_jb.pop(p_str)

    # 查询
    def on_btn_query(self):
        cols = ['tjbh','xm','xb','nl','sfzh','sjhm','dwmc','ysje','is_gxy','is_gxz','is_gxt','is_gns'
            ,'is_jzx','glu','is_yc_glu','glu2','is_yc_glu2','hbalc','is_yc_hbalc','ua','is_yc_ua','tch'
            ,'is_yc_tch','tg','is_yc_tg','hdl','is_yc_hdl','ldl','is_yc_ldl','hbp','is_yc_hbp','lbp','is_yc_lbp']
        sql = get_mbgl_sql()
        if self.dg_rq.where_date:
            sql = sql + self.dg_rq.where_date
        if self.mg_je.get_where_text():
            sql = sql + self.mg_je.get_where_text()
        if self.tj_dw.where_dwbh:
            sql = sql + ''' AND DWBH = '%s' ''' %self.tj_dw.where_dwbh
        if self.where_jb:
            sql = sql + ''' AND %s ''' %' AND '.join(["%s = '%s' " %(key,value) for key,value in self.where_jb.items()])
        # print(sql)
        # return
        results = self.session.execute(sql).fetchall()
        new_results = [dict(zip(cols,result)) for result in results]
        self.table.load(new_results)
        self.gp_middle.setTitle('疑似列表(%s)' %self.table.rowCount())
        mes_about(self, '检索出 %s 条数据！' %self.table.rowCount())

        # results = self.session.query(MT_MB_YSKH).filter(MT_MB_YSKH.qdrq == '2018-06-30').all()
        # tmp = [result.to_dict for result in results]
        # self.table.load(tmp)

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
            # item1 = menu.addAction(Icon("短信"), "发送预约短信")
            # item2 = menu.addAction(Icon("短信"), "编辑预约短信")
            # item3 = menu.addAction(Icon("预约"), "设置预约客户")
            # item4 = menu.addAction(Icon("预约"), "电话记录")
            # item5 = menu.addAction(Icon("预约"), "本次体检结果")
            # item6 = menu.addAction(Icon("预约"), "历年体检结果")
            # item7 = menu.addAction(Icon("预约"), "浏览体检报告")
            # item8 = menu.addAction(Icon("预约"), "下载电子报告")

            action = menu.exec_(self.table.mapToGlobal(pos))
