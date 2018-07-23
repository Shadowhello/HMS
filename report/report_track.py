from .report_track_ui import ReportTrackUI
from report.report_track_thread import *
from report.model import *
from widgets.cwidget import *
from pis.pis_result_ui import PisResultUI

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

        self.btn_export.clicked.connect(self.on_btn_export_click)       # 导出
        self.btn_query.clicked.connect(self.on_btn_query_click)          # 查询

        self.btn_pis.clicked.connect(self.on_btn_pis_click)
        ##############线程########################################################
        self.cur_tjbh = None         #最后一次选择的体检编号
        self.pis_thread = None
        self.lis_thread = None
        self.pacs_thread = None
        ############### 对话框 #######################################
        self.pis_ui = None

    def initParas(self):
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()
        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)

        self.lt_where_search.s_dwbh.setValues(self.dwmc_bh,self.dwmc_py)

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
        self.lt_quick_search.setText(tjbh,xm,sjhm,sfzh)
        self.cur_tjbh = tjbh

    # 进入PIS
    def on_btn_pis_click(self):
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
            self.pis_thread = PacsResultThread()
            self.pis_thread.setStart(self.cur_tjbh)
            self.pis_thread.signalConnFail.connect(self.on_sys_conn_fail, type=Qt.QueuedConnection)
            self.pis_thread.signalPost.connect(self.on_sys_refresh, type=Qt.QueuedConnection)
            self.pis_thread.start()

    # LIS、PACS、PIS 系统连接失败，提示
    def on_sys_conn_fail(self,message):
        mes_about(self,message)

    def on_sys_refresh(self,results):
        if not self.pis_ui:
            self.pis_ui = PisResultUI(self, results)
        else:
            self.pis_ui.setData(results)
        self.pis_ui.show()




