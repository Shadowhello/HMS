# 系统接口
from app_interface.i_pacs_result_ui import PacsResultUI
from app_interface.i_pis_result_ui import PisResultUI
from app_interface.i_sms_ui import SmsUI
from app_interface.i_phone_ui import PhoneUI
from lis.lis_result_ui import LisResultUI
from report.report_item_ui import ItemsStateUI
from report.report_track_thread import *
from widgets.cwidget import *
from .report_track_ui import ReportTrackUI


# 报告追踪
class ReportTrack(ReportTrackUI):

    def __init__(self):
        super(ReportTrack, self).__init__()
        self.initParas()
        #################### 信号槽  ############################
        # 右键菜单
        self.table_track.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.table_track.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单
        self.table_track.itemClicked.connect(self.on_table_set)
        self.table_track.itemDoubleClicked.connect(self.on_btn_item_click)
        # 快速检索
        self.gp_quick_search.returnPressed.connect(self.on_quick_search)
        self.btn_export.clicked.connect(self.on_btn_export_click)       # 导出
        self.btn_query.clicked.connect(self.on_btn_query_click)          # 查询
        # 功能栏
        self.btn_item.clicked.connect(self.on_btn_item_click)
        self.btn_pis.clicked.connect(self.on_btn_pis_click)
        self.btn_pacs.clicked.connect(self.on_btn_pacs_click)
        self.btn_lis.clicked.connect(self.on_btn_lis_click)
        self.btn_phone.clicked.connect(self.on_btn_phone_click)
        self.btn_sms.clicked.connect(self.on_btn_sms_click)
        ##############线程########################################################
        self.cur_tjbh = None         #最后一次选择的体检编号
        self.pis_thread = None
        self.lis_thread = None
        self.pacs_thread = None
        ############### 系统对话框 #######################################
        self.item_ui = None       # 项目查看
        self.pis_ui = None        # 病理对话框
        self.lis_ui = None        # 检验对话框
        self.pacs_ui = None       # 检查对话框
        self.phone_ui = None      # 电话记录对话框
        self.sms_ui = None        # 短信记录对话框

    def initParas(self):
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()
        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)

        self.lt_where_search.s_dwbh.setValues(self.dwmc_bh,self.dwmc_py)

    def on_quick_search(self,p1_str,p2_str):
        if p1_str == 'tjbh':
            where_str = " TJ_TJDJB.TJBH = '%s' " %p2_str
        elif p1_str == 'sjhm':
            where_str = " TJ_TJDAB.SJHM = '%s' " % p2_str
        elif p1_str == 'sfzh':
            where_str = " TJ_TJDAB.SFZH = '%s' " % p2_str
        else:
            where_str = " TJ_TJDAB.XM ='%s' " % p2_str

        results = self.session.execute(get_quick_search_sql(where_str)).fetchall()
        self.table_track.load(results)
        mes_about(self,'共检索出 %s 条数据！' %self.table_track.rowCount())

    # 右键功能
    def onTableMenu(self,pos):
        row_num = -1
        indexs=self.table_track.selectionModel().selection().indexes()
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

            action = menu.exec_(self.table_track.mapToGlobal(pos))

    # 导出功能
    def on_btn_export_click(self):
        self.table_track.export()

    # 查询功能
    def on_btn_query_click(self):
        tstart,tend = self.lt_where_search.date_range             # 日期
        sql = get_report_track_sql(tstart, tend)

        where_tjqy = self.lt_where_search.where_tjqy              #体检区域
        if where_tjqy:
            sql = sql + where_tjqy

        where_tjlx = self.cb_report_type.where_tjlx               # 体检类型
        if where_tjlx:
            sql = sql +where_tjlx

        where_dwmc = self.lt_where_search.where_dwmc              # 体检单位
        if where_dwmc:
            sql = sql + where_dwmc

        results = self.session.execute(sql).fetchall()
        self.table_track.load(results)

    # 设置快速检索文本
    def on_table_set(self,tableWidgetItem):
        row = tableWidgetItem.row()
        tjbh = self.table_track.item(row, 3).text()
        xm = self.table_track.item(row, 4).text()
        sfzh = self.table_track.item(row, 7).text()
        sjhm = self.table_track.item(row, 8).text()
        self.gp_quick_search.setText(tjbh,xm,sjhm,sfzh)
        self.cur_tjbh = tjbh

    #体检系统项目查看
    def on_btn_item_click(self):
        if not self.cur_tjbh:
            mes_about(self,'请先选择一个人！')
            return
        else:
            if not self.item_ui:
                self.item_ui = ItemsStateUI(self)
            self.item_ui.returnPressed.emit(self.cur_tjbh)
            self.item_ui.show()

    # 电话记录
    def on_btn_phone_click(self):
        if not self.cur_tjbh:
            mes_about(self, '请先选择一个人！')
            return
        else:
            if not self.item_ui:
                self.phone_ui = PhoneUI(self)
            self.phone_ui.returnPressed.emit(self.cur_tjbh)
            self.phone_ui.show()

    # 短信记录
    def on_btn_sms_click(self):
        if not self.cur_tjbh:
            mes_about(self, '请先选择一个人！')
            return
        else:
            if not self.sms_ui:
                self.sms_ui = SmsUI(self)
            self.sms_ui.returnPressed.emit(self.cur_tjbh)
            self.sms_ui.show()

    # 进入PIS
    def on_btn_pis_click(self):
        if not self.cur_tjbh:
            mes_about(self,'请先选择一个人！')
            return
        is_has = self.session.execute(has_pis_sql(self.cur_tjbh)).scalar()
        if not is_has:
            mes_about(self,'该体检顾客：%s，无病理项目！' %self.cur_tjbh)
            return
        if self.pis_thread:
            self.pis_thread.setStart(self.cur_tjbh)
            self.pis_thread.signalConnFail.connect(self.on_sys_conn_fail, type=Qt.QueuedConnection)
            self.pis_thread.signalPost.connect(self.on_sys_refresh, type=Qt.QueuedConnection)
            self.pis_thread.start()
        else:
            self.pis_thread = PisResultThread()
            self.pis_thread.setStart(self.cur_tjbh)
            self.pis_thread.signalConnFail.connect(self.on_sys_conn_fail, type=Qt.QueuedConnection)
            self.pis_thread.signalPost.connect(self.on_sys_refresh, type=Qt.QueuedConnection)
            self.pis_thread.start()

    # 进入PACS系统
    def on_btn_pacs_click(self):
        if not self.cur_tjbh:
            mes_about(self,'请先选择一个人！')
            return
        is_has = self.session.execute(has_pacs_sql(self.cur_tjbh)).scalar()
        if not is_has:
            mes_about(self, '该体检顾客：%s，无放射检查项目！' % self.cur_tjbh)
            return
        if self.pacs_thread:
            self.pacs_thread.setStart(self.cur_tjbh)
            self.pacs_thread.signalConnFail.connect(self.on_sys_conn_fail, type=Qt.QueuedConnection)
            self.pacs_thread.signalPost.connect(self.on_sys_refresh, type=Qt.QueuedConnection)
            self.pacs_thread.start()
        else:
            self.pacs_thread = PacsResultThread()
            self.pacs_thread.setStart(self.cur_tjbh)
            self.pacs_thread.signalConnFail.connect(self.on_sys_conn_fail, type=Qt.QueuedConnection)
            self.pacs_thread.signalPost.connect(self.on_sys_refresh, type=Qt.QueuedConnection)
            self.pacs_thread.start()

    # 进入LIS系统
    def on_btn_lis_click(self):
        if not self.cur_tjbh:
            mes_about(self,'请先选择一个人！')
            return
        # is_has = self.session.execute(has_pis_sql(self.cur_tjbh)).scalar()
        # if not is_has:
        #     mes_about(self, '该体检顾客：%s，无检验项目！' % self.cur_tjbh)
        #     return
        if self.lis_thread:
            self.lis_thread.setStart(self.cur_tjbh)
            self.lis_thread.signalConnFail.connect(self.on_sys_conn_fail, type=Qt.QueuedConnection)
            self.lis_thread.signalPost.connect(self.on_sys_refresh, type=Qt.QueuedConnection)
            self.lis_thread.start()
        else:
            self.lis_thread = LisResultThread()
            self.lis_thread.setStart(self.cur_tjbh)
            self.lis_thread.signalConnFail.connect(self.on_sys_conn_fail, type=Qt.QueuedConnection)
            self.lis_thread.signalPost.connect(self.on_sys_refresh, type=Qt.QueuedConnection)
            self.lis_thread.start()

    # LIS、PACS、PIS 系统连接失败，提示
    def on_sys_conn_fail(self,message):
        mes_about(self,message)

    def on_sys_refresh(self,sys_name,results):
        '''
        :param sys_name: 系统名称 PIS，PACS，LIS
        :param results: 数据
        :return:
        '''
        if sys_name =='PIS':
            if not self.pis_ui:
                self.pis_ui = PisResultUI('病理系统',self)
            self.pis_ui.setData(results)
            self.pis_ui.show()
        elif sys_name =='LIS':
            if not self.lis_ui:
                self.lis_ui = LisResultUI('检验系统',self)
            self.lis_ui.setData(results)
            self.lis_ui.show()
        elif sys_name =='PACS':
            if not self.pacs_ui:
                self.pacs_ui = PacsResultUI('检查系统',self)
            self.pacs_ui.setData(results)
            self.pacs_ui.show()
        else:
            pass

    def closeEvent(self, *args, **kwargs):
        super(ReportTrack, self).closeEvent(*args, **kwargs)
        try:
            if self.lis_thread:
                self.lis_thread.stop()
            if self.pacs_thread:
                self.pacs_thread.stop()
            if self.pis_thread:
                self.pis_thread.stop()
        except Exception as e:
            self.log.info("ReportTrack 线程关闭时发生错误：%s " %e)
        try:
            if self.lis_ui:
                self.lis_ui.close()
            if self.pacs_ui:
                self.pacs_ui.close()
            if self.pis_ui:
                self.pis_ui.close()
            if self.phone_ui:
                self.phone_ui.close()
            if self.sms_ui:
                self.sms_ui.close()
        except Exception as e:
            self.log.info("ReportTrack 子UI关闭时发生错误：%s " %e)



