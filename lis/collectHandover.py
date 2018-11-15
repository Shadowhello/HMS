from lis.collectHandover_ui import *
from lis.model import *
from collections import Counter

class CollectHandover(CollectHandover_UI):

    def __init__(self):

        super(CollectHandover,self).__init__()
        self.initParas()
        self.btn_query.clicked.connect(self.on_btn_query_click)
        self.gp_quick_search.returnPressed.connect(self.on_quick_search)         # 快速检索
        self.table_handover_master.itemClicked.connect(self.on_table_handover_master_clicked)
        self.table_handover.itemClicked.connect(self.on_table_handover_clicked)
        self.btn_handover.clicked.connect(self.on_collect_handover)
        self.btn_receive.clicked.connect(self.on_collect_receive)
        # 新增抽血取消功能
        self.table_handover_detail.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.table_handover_detail.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单

        # 特殊变量
        self.sgys = None    # 试管
        self.datas = None   # 总汇总

    def initParas(self):
        pass

    # #快速检索
    def on_quick_search(self,p1_str,p2_str):
        pass
    #     if p1_str == 'tjbh':
    #         where_str = " a.TJBH = '%s' " % p2_str
    #     else:
    #         where_str = " b.XM = '%s' " % p2_str
    #     results = self.session.execute(get_report_review_sql2(where_str)).fetchall()
    #     self.table_report_review.load(results)
    #     mes_about(self,'共检索出 %s 条数据！' %self.table_report_review.rowCount())

    # 表格右键功能
    def onTableMenu(self,pos):
        row_num = -1
        indexs=self.table_handover_detail.selectionModel().selection().indexes()
        if indexs:
            for i in indexs:
                row_num = i.row()
            menu = QMenu()
            item1 = menu.addAction(Icon("取消"), "取消抽血")
            action = menu.exec_(self.table_handover_detail.mapToGlobal(pos))
            tjbh = self.table_handover_detail.getCurItemValueOfKey('tjbh')
            mxbh = self.table_handover_detail.getCurItemValueOfKey('mxbh')
            czsj = self.table_handover_detail.getCurItemValueOfKey('czsj')
            czxm = self.table_handover_detail.getCurItemValueOfKey('czxm')
            # 按钮功能
            if action == item1:
                button = mes_warn(self, "当前条码已抽血，是否取消该次扫描工作！")
                if button == QMessageBox.Yes:
                    qxbz = '取消当前条码扫描，操作人：%s，操作时间：%s，操作区域：%s 。' % (self.login_name, cur_datetime(), self.login_area)
                    try:
                        self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.tjbh == tjbh,
                                                               MT_TJ_CZJLB.mxbh == mxbh,
                                                               MT_TJ_CZJLB.czsj == czsj,
                                                               MT_TJ_CZJLB.czxm == czxm
                                                               ).update({MT_TJ_CZJLB.jllx: '0000', MT_TJ_CZJLB.bz: qxbz})
                        self.session.commit()
                        mes_about(self,"取消成功！请重新刷新！")
                    except Exception as e:
                        self.session.rollback()
                        mes_about(self, '取消该条码出错！错误信息：%s' % e)

    # 样本交接
    def on_collect_handover(self):
        rows = self.table_handover_master.isSelectRows()
        if not rows:
            mes_about(self, '请选择需要交接的样本！')
            return

        if self.table_handover_master.getCurItemValueOfKey('jjxm'):
            mes_about(self,'当前选中的样本已交接，请勿重复进行样本交接！')
            return
        button = mes_warn(self, "您确认交接%s份样本？" %self.table_handover_detail.rowCount())
        if button != QMessageBox.Yes:
            return
        # 操作时间
        operate_time = cur_datetime()
        for row in range(self.table_handover_detail.rowCount()):
            tjbh = self.table_handover_detail.getItemValueOfKey(row,'tjbh')
            mxbh = self.table_handover_detail.getItemValueOfKey(row,'mxbh')

            self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.tjbh == tjbh,MT_TJ_CZJLB.mxbh == mxbh).update({
                MT_TJ_CZJLB.jjxm: self.login_name,
                MT_TJ_CZJLB.jjsj: operate_time,
                MT_TJ_CZJLB.sjfs: self.collect_user.currentText()
            })
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.log.info(e)
            mes_about(self, '更新数据库TJ_CZJLB 出错！错误信息：%s' % e)
            return
        # 刷新控件
        self.table_handover_master.setCurItemValueOfKey('jjxm',self.login_name)
        self.table_handover_master.setCurItemValueOfKey('jjsj',operate_time)
        mes_about(self, '样本交接成功！')

    # 样本签收
    def on_collect_receive(self):
        rows = self.table_handover_master.isSelectRows()
        if not rows:
            mes_about(self, '请选择需要签收的样本！')
            return
        if not self.table_handover_master.getCurItemValueOfKey('jjxm'):
            mes_about(self,'当前选中的样本还未交接，不允许进行签收！')
            return
        if self.table_handover_master.getCurItemValueOfKey('qsxm'):
            mes_about(self,'当前选中的样本已签收，请勿重复进行样本签收！')
            return
        button = mes_warn(self, "您确认签收%s份样本？" %self.table_handover_detail.rowCount())
        if button != QMessageBox.Yes:
            return
        # 操作时间
        operate_time = cur_datetime()
        for row in range(self.table_handover_detail.rowCount()):
            tjbh = self.table_handover_detail.getItemValueOfKey(row,'tjbh')
            mxbh = self.table_handover_detail.getItemValueOfKey(row,'mxbh')

            self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.tjbh == tjbh,MT_TJ_CZJLB.mxbh == mxbh).update({
                MT_TJ_CZJLB.jsxm: self.login_name,
                MT_TJ_CZJLB.jssj: operate_time
            })
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.log.info(e)
            mes_about(self, '更新数据库TJ_CZJLB 出错！错误信息：%s' % e)
            return
        # 刷新控件
        self.table_handover_master.setCurItemValueOfKey('qsxm',self.login_name)
        self.table_handover_master.setCurItemValueOfKey('qssj',operate_time)
        mes_about(self, '样本签收成功！')

    # 条件查询
    def on_btn_query_click(self):
        self.sgys = None
        self.on_btn_query()
        self.on_table_handover_load()

    def on_btn_query(self):
        collect_time = self.collect_time.get_where_text()
        if self.collect_user2.currentText() =='所有':
            where_collect_user2 = ' AND 1 = 1 '
        else:
            where_collect_user2 = "AND CZGH = '%s' " %self.login_id
        # 判断试管
        if self.sgys:
            where_collect_user2 = where_collect_user2 + " AND CAST(BZ AS VARCHAR)= '%s' " %self.sgys

        # 检索条件
        try:
            if self.collect_area.get_area == '明州':
                results = self.session.execute(get_handover2_sql(collect_time[0], collect_time[1], self.collect_area.get_area,where_collect_user2)).fetchall()
            else:
                results = self.session.execute(get_handover_sql(collect_time[0],collect_time[1],self.collect_area.get_area,where_collect_user2)).fetchall()
        except Exception as e:
            mes_about(self,'执行查询出错，错误信息：%s'%e)
            results = []
        self.table_handover_master.load(results)
        rowcount = self.table_handover_master.rowCount()
        self.gp_middle_middle.setTitle('样本交接签收明细(%s)' %rowcount)
        self.datas = self.table_handover_master.status()
        self.table_handover_detail.load([])
        mes_about(self, '共检索出 %s 行数据！' % rowcount)

    def on_table_handover_load(self):
        # 2018-11-13 采用表格展示
        self.table_handover.load(merge_by_key(self.datas))
        self.gp_middle_left.setTitle('样本汇总(%s)' % self.table_handover.rowCount())
        # 按钮组 形式展示 无法对齐，较丑
        # self.on_btn_query_detail(v1, v2, v3)

    # 查看交接、签收明细
    def on_table_handover_clicked(self,QTableWidgetItem):
        # 设置试管
        self.sgys = self.table_handover.getItemValueOfKey(QTableWidgetItem.row(),'sgys')
        self.on_btn_query()


    # 查看采集详细
    def on_table_handover_master_clicked(self,QTableWidgetItem):
        t_start = self.table_handover_master.item(QTableWidgetItem.row(),0).text()
        t_end = self.table_handover_master.item(QTableWidgetItem.row(), 1).text()
        czqy = self.table_handover_master.item(QTableWidgetItem.row(),2).text()
        sgys = self.table_handover_master.item(QTableWidgetItem.row(), 3).text()
        jjxm = self.table_handover_master.item(QTableWidgetItem.row(), 5).text()
        jjsj = self.table_handover_master.item(QTableWidgetItem.row(), 6).text()
        if not jjxm:
            jjxm = None
        if not jjsj:
            jjsj = None
        # 条件：用户与区域
        if self.collect_user2.currentText() =='所有':
            if czqy=='明州':
                results = self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.czsj.between(t_start, t_end),
                                                                 MT_TJ_CZJLB.jllx.in_(('0010', '0011')),
                                                                 cast(MT_TJ_CZJLB.bz, VARCHAR) == sgys,
                                                                 MT_TJ_CZJLB.jjxm == jjxm,
                                                                 MT_TJ_CZJLB.jjsj == jjsj,
                                                                 MT_TJ_CZJLB.czqy.like('%s%%' % czqy)
                                                                 ).all()
            else:
                results = self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.czsj.between(t_start,t_end),
                                                                 MT_TJ_CZJLB.jllx.in_(('0010', '0011')),
                                                                 MT_TJ_CZJLB.czqy == czqy,
                                                                 cast(MT_TJ_CZJLB.bz, VARCHAR) == sgys,
                                                                 MT_TJ_CZJLB.jjxm == jjxm,
                                                                 MT_TJ_CZJLB.jjsj == jjsj
                                                                 ).all()
        else:
            if czqy=='明州':
                results = self.session.query(MT_TJ_CZJLB).filter(
                                                                 MT_TJ_CZJLB.czsj.between(t_start, t_end),
                                                                 MT_TJ_CZJLB.czgh == self.login_id,
                                                                 MT_TJ_CZJLB.jllx.in_(('0010', '0011')),
                                                                 cast(MT_TJ_CZJLB.bz, VARCHAR) == sgys,
                                                                 MT_TJ_CZJLB.jjxm == jjxm,
                                                                 MT_TJ_CZJLB.jjsj == jjsj,
                                                                 MT_TJ_CZJLB.czqy.like('%s%%' % czqy)
                                                                 ).all()
            else:
                results = self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.czsj.between(t_start,t_end),
                                                                 MT_TJ_CZJLB.czgh == self.login_id,
                                                                 MT_TJ_CZJLB.jllx.in_(('0010', '0011')),
                                                                 MT_TJ_CZJLB.czqy == czqy,
                                                                 cast(MT_TJ_CZJLB.bz,VARCHAR) == sgys,
                                                                 MT_TJ_CZJLB.jjxm == jjxm,
                                                                 MT_TJ_CZJLB.jjsj == jjsj,
                                                                 ).all()

        self.table_handover_detail.load((result.detail for result in results))
        self.gp_middle_right.setTitle('样本采集明细(%s)' %self.table_handover_detail.rowCount(),)

    # 获取 待交接、待签收、完成 详情
    def on_btn_query_detail(self,data1:dict,data2:dict,data3:dict):
        # 销毁 旧的控件
        while self.lt_sample_jj_sum.count():
            item = self.lt_sample_jj_sum.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        while self.lt_sample_qs_sum.count():
            item = self.lt_sample_qs_sum.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        # 刷新新的控件
        for key,value in data1.items():
            btn = QPushButton(Icon(key),key)
            label = CollectLable(str(value))
            self.lt_sample_jj_sum.addWidget(btn)
            self.lt_sample_jj_sum.addWidget(label)
        # self.lt_sample_jj_sum.addStretch()

        for key,value in data2.items():
            btn = QPushButton(Icon(key),key)
            label = CollectLable(str(value))
            self.lt_sample_qs_sum.addWidget(btn)
            self.lt_sample_qs_sum.addWidget(label)
        # self.lt_sample_qs_sum.addStretch()


class CollectLable(QLabel):

    def __init__(self,p1_str):
        super(CollectLable,self).__init__()
        self.setText(p1_str)
        self.setMinimumWidth(30)
        self.setStyleSheet('''font: 75 16pt \"微软雅黑\";color: rgb(0, 85, 255);''')


def merge_by_key(datas):
    tmp = {}
    for data in datas:
        key = data['sgys']
        data.pop('sgys')    # 字符串无法叠加
        if key in tmp:
            # 叠加
            tmp[key] = Counter(tmp[key]) + Counter(data)
        else:
            # 创建
            tmp[key] = data
    # from pprint import pprint
    # pprint(tmp)
    tmp2 = []
    for k,v in tmp.items():
        v['sgys'] = k
        tmp2.append(v)

    tmp2.sort(key=lambda x: x['cjsl'], reverse=True)
    return tmp2

