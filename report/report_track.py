# 系统接口
from app_interface import PacsResult, PisResult,LisResult,SmsPostUI
from app_interface.i_phone_ui import PhoneUI
from app_interface.i_sms_ui import SmsUI
from report.report_item_ui import ItemsStateUI
from report.report_track_thread import *
from widgets.cwidget import *
from .report_track_ui import ReportTrackUI
from utils import api_file_down,cur_datetime

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
        # 按钮栏
        self.gp_quick_search.returnPressed.connect(self.on_quick_search)    # 快速检索
        self.btn_export.clicked.connect(self.on_btn_export_click)           # 导出
        self.btn_query.clicked.connect(self.on_btn_query_click)             # 查询
        self.btn_task.clicked.connect(self.on_btn_task_click)               # 任务领取
        self.btn_receive.clicked.connect(self.on_btn_receive_click)         # 结果接收
        self.btn_myself.clicked.connect(self.on_btn_myself_click)           # 查看我自己的领取任务
        self.btn_djd.clicked.connect(self.on_btn_djd_click)
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
        self.query_thread = None     # SQL 查询线程
        ############### 系统对话框 #######################################
        self.item_ui = None       # 项目查看
        self.pis_ui = None        # 病理对话框
        self.lis_ui = None        # 检验对话框
        self.pacs_ui = None       # 检查对话框
        self.phone_ui = None      # 电话记录对话框
        self.sms_ui = None        # 短信记录对话框
        self.pic_ui = None        # 采血照片对话框
        self.pd_ui = None         # 进度条
        self.pd_ui_num = 0        # 进度条计数，用于处理线程->UI静态变量 弹窗造成的BUG
        self.zyd_ui = None        # 指引单对话框

    def initParas(self):
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()
        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)

        self.lt_where_search.s_dwbh.setValues(self.dwmc_bh,self.dwmc_py)

    #快速检索
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
            item1 = menu.addAction(Icon("切换"), "更换追踪人员")
            item2 = menu.addAction(Icon("电话"), "增加电话记录")
            item3 = menu.addAction(Icon("短信"), "发送短信")
            item4 = menu.addAction(Icon("采血台"), "查看采血照片")
            item5 = menu.addAction(Icon("体检收单"), "纸质导检单")
            action = menu.exec_(self.table_track.mapToGlobal(pos))
            # 获取变量
            tjbh = self.table_track.getCurItemValueOfKey('tjbh')
            sjhm = self.table_track.getCurItemValueOfKey('sjhm')
            if action == item1:
                if self.table_track.getCurItemValueOfKey('lqry'):
                    button = mes_warn(self,'您确认自己追踪本报告吗？')
                    if button == QMessageBox.Yes:
                        pass
                        mes_about(self,'更新成功！')
                else:
                    mes_about(self,'该体检报告当前无追踪护士，无须更换！')
            elif action == item2:
                if not self.phone_ui:
                    self.phone_ui = PhoneUI(self)
                self.phone_ui.returnPressed.emit(tjbh, sjhm)
                self.phone_ui.show()
            elif action == item3:
                if sjhm:
                    ui = SmsPostUI(self)
                    ui.initData.emit(tjbh,sjhm)
                    ui.show()
                else:
                    mes_about(self,'该顾客不存在手机，请先补充完整！')

            elif action == item4:
                if self.get_gol_para('api_file_down'):
                    self.show_url = self.get_gol_para('api_file_down')
                else:
                    self.show_url = 'http://10.8.200.201:4000/app_api/file/down/%s/%s'
                url = self.show_url % (tjbh, '000001')
                data = api_file_down(url)
                if data:
                    if not self.pic_ui:
                        self.pic_ui = PicDialog()
                    self.pic_ui.setData(data)
                    self.pic_ui.show()
                else:
                    mes_about(self, '该人未拍照！')

            elif action == item5:
                result = self.session.query(MT_TJ_PHOTO_ZYD).filter(MT_TJ_PHOTO_ZYD.tjbh == tjbh).scalar()
                if result:
                    if result.picture_zyd:
                        if not self.zyd_ui:
                            self.zyd_ui = ZYDDialog()
                        self.zyd_ui.setData(result.picture_zyd)
                        self.zyd_ui.show()
                else:
                    mes_about(self, '该人导检单未拍照！')

    # 查询我自己追踪的任务
    def on_btn_myself_click(self):
        pass

    def on_btn_djd_click(self):
        result = self.session.query(MT_TJ_PHOTO_ZYD).filter(MT_TJ_PHOTO_ZYD.tjbh == self.cur_tjbh).scalar()
        if result:
            if result.picture_zyd:
                if not self.zyd_ui:
                    self.zyd_ui = ZYDDialog()
                self.zyd_ui.setData(result.picture_zyd)
                self.zyd_ui.show()
        else:
            mes_about(self, '该人导检单未拍照！')

    # 导出功能
    def on_btn_export_click(self):
        self.table_track.export()

    # 启动线程 执行查询
    def execQuery(self,sql):
        if not self.query_thread:
            self.query_thread = QueryThread(self.session)
        self.query_thread.setTask(sql)
        self.query_thread.signalMes.connect(self.on_mes_show, type=Qt.QueuedConnection)
        self.query_thread.start()

    def on_mes_show(self,mes:bool,result:list,num:int):
        if self.pd_ui_num == num:
            return
        else:
            self.pd_ui_num = num
        if self.pd_ui:
            if not self.pd_ui.isHidden():
                self.pd_ui.hide()
        if mes:
            self.table_track.load(result)
            self.gp_middle.setTitle('追踪列表（%s）' %self.table_track.rowCount())
            mes_about(self,'共检索出 %s 条数据！' %self.table_track.rowCount())
        else:
            mes_about(self,"查询出错，错误信息：%s" %result[0])

    # 查询功能
    def on_btn_query_click(self):
        if self.lt_where_search.where_dwbh=='00000':
            mes_about(self,'不存在该单位，请重新选择！')
            return
        tstart,tend = self.lt_where_search.date_range             # 日期

        # 报告状态优先选择
        print(self.lt_where_search.where_bgzt_text)
        if self.lt_where_search.where_bgzt_text =='待追踪':
            sql = get_report_track_sql(tstart, tend)
        elif self.lt_where_search.where_bgzt_text =='追踪中':
            sql = get_report_tracking_sql(tstart, tend)
        else:
            sql = get_report_tracked_sql(tstart, tend)

        print(sql)

        where_tjqy = self.lt_where_search.where_tjqy             # 体检区域
        if where_tjqy:
            sql = sql + where_tjqy

        where_tjlx = self.cb_report_type.where_tjlx               # 体检类型
        if where_tjlx:
            sql = sql +where_tjlx

        where_dwmc = self.lt_where_search.where_dwmc              # 体检单位
        if where_dwmc:
            sql = sql + where_dwmc

        # sql = sql + ''' ORDER BY d.XMZQ,T1.QDRQ,T1.DWMC  '''
        # 追踪类型
        if not self.cb_track_type.text():
            if self.lt_where_search.where_bgzt_text == '待追踪':
                # 所有
                sql = sql + ''' UNION ALL ''' +get_report_bgth_sql()
            else:
                sql = sql
        elif self.cb_track_type.text() == '未结束':
            sql = sql + ''' ORDER BY d.XMZQ,T1.QDRQ,T1.DWMC  '''
        elif self.cb_track_type.text() == '审核退回':
            sql = get_report_bgth_sql() + ''' AND TJ_BGGL.bgth = '0' '''
        else:
            sql = get_report_bgth_sql() + ''' AND TJ_BGGL.bgth = '1' '''


        # print(sql)
        # 执行查询
        self.execQuery(sql)
        # 进度条
        self.pd_ui = ProgressDialog(self)
        self.pd_ui.show()

    # 设置快速检索文本
    def on_table_set(self,tableWidgetItem):
        row = tableWidgetItem.row()
        tjbh = self.table_track.item(row, 7).text()
        xm = self.table_track.item(row, 8).text()
        sfzh = self.table_track.item(row, 11).text()
        sjhm = self.table_track.item(row, 12).text()
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
        sjhm = self.table_track.getCurItemValueOfKey('sjhm')
        if not self.cur_tjbh:
            mes_about(self, '请先选择一个人！')
            return
        else:
            if not self.phone_ui:
                self.phone_ui = PhoneUI(self)
            self.phone_ui.returnPressed.emit(self.cur_tjbh,sjhm)
            self.phone_ui.show()

    # 短信记录
    def on_btn_sms_click(self):
        if not self.cur_tjbh:
            mes_about(self, '请先选择一个人！')
            return
        else:
            sjhm = self.table_track.getCurItemValueOfKey('sjhm')
            if not self.sms_ui:
                self.sms_ui = SmsUI(self)
            self.sms_ui.returnPressed.emit(self.cur_tjbh,sjhm)
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
                self.pis_ui = PisResult(self)
            self.pis_ui.setData(results)
            self.pis_ui.show()
        elif sys_name =='LIS':
            if not self.lis_ui:
                self.lis_ui = LisResult(self)
            self.lis_ui.setData(results)
            self.lis_ui.show()
        elif sys_name =='PACS':
            if not self.pacs_ui:
                self.pacs_ui = PacsResult(self)
            self.pacs_ui.setData(results)
            self.pacs_ui.show()
        else:
            pass

    def on_btn_task_click(self):
        tmp = []

        rows = self.table_track.isSelectRows()
        for row in rows:
            data_obj = {'jllx': '0030', 'jlmc': '报告追踪', 'tjbh': '', 'mxbh': '',
                        'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area, 'jlnr': None,
                        'bz': None}
            data_obj['tjbh'] = self.table_track.item(row, 7).text()
            data_obj['jlnr'] = self.table_track.item(row, 15).text()
            tmp.append(data_obj)
            self.table_track.item(row, 2).setText('追踪中')
            self.table_track.item(row, 3).setText(self.login_name)

            result = self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == self.cur_tjbh).scalar()
            if result:
                self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == self.cur_tjbh).update(
                    {
                        MT_TJ_BGGL.zzxm: self.login_name,
                        MT_TJ_BGGL.zzgh: self.login_id,
                        MT_TJ_BGGL.zzrq: cur_datetime(),
                        MT_TJ_BGGL.bgzt: '0',
                    }
                )
            else:
                self.session.bulk_insert_mappings(MT_TJ_BGGL, [{'tjbh':self.cur_tjbh,'bgzt':'0','zzxm':self.login_name,'zzgh':self.login_id,'zzrq':cur_datetime()}])
            self.session.commit()
        try:
            self.session.bulk_insert_mappings(MT_TJ_CZJLB, tmp)
            self.session.commit()
            mes_about(self,'领取成功！')
        except Exception as e:
            self.session.rollback()
            mes_about(self, '插入 TJ_CZJLB 记录失败！错误代码：%s' % e)

    def on_btn_receive_click(self):
        rows =self.table_track.isSelectRows()
        for row in rows:
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

# 等待过程中的进度动态图
class ProgressDialog(QDialog):

    def __init__(self,parent):
        super(ProgressDialog,self).__init__(parent)
        self.initUI()

    def initUI(self):
        # 窗口模式，去掉标题栏
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(500,500)
        lt_main = QVBoxLayout()
        lb_pic = QLabel()
        lb_mes = QLabel('正在查询，请您稍等')
        lb_mes.setStyleSheet('''font: 75 28pt \"微软雅黑\";color: rgb(255, 0, 0);''')
        movie = QMovie(file_ico('35.gif'))
        lb_pic.setMovie(movie)
        movie.start()
        # 加入布局
        lt_main.addWidget(lb_pic)
        lt_main.addWidget(lb_mes)
        self.setLayout(lt_main)