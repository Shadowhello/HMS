# 系统接口
from app_interface import *
from .report_item_ui import ItemsStateUI,OperateUI
from .report_track_thread import *
from widgets.cwidget import *
from .report_track_ui import ReportTrackUI
from utils import api_file_down,cur_datetime
import webbrowser

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
        #self.btn_task.clicked.connect(self.on_btn_task_click)               # 任务领取
        self.btn_receive.clicked.connect(self.on_btn_receive_click)         # 结果接收
        #self.btn_myself.clicked.connect(self.on_btn_myself_click)           # 查看我自己的领取任务
        self.btn_djd.clicked.connect(self.on_btn_djd_click)
        self.btn_myself.menu_clicked.connect(self.on_btn_myself_click)
        self.btn_send.menu_clicked.connect(self.on_btn_send_click)          # 发送任务：发到审核、发到审阅
        self.btn_task.menu_clicked.connect(self.on_btn_task_click)          # 任务领取
        # 功能栏
        self.btn_item.clicked.connect(self.on_btn_item_click)
        self.btn_czjl.clicked.connect(self.on_btn_czjl_click)
        self.btn_pis.clicked.connect(self.on_btn_pis_click)
        self.btn_pacs.clicked.connect(self.on_btn_pacs_click)
        self.btn_lis.clicked.connect(self.on_btn_lis_click)
        self.btn_equip.clicked.connect(self.on_btn_equip_click)
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
        self.operatr_ui = None    # 操作记录界面
        self.pis_ui = None        # 病理对话框
        self.lis_ui = None        # 检验对话框
        self.pacs_ui = None       # 检查对话框
        self.equip_ui = None      # 设备对话框
        self.phone_ui = None      # 电话记录对话框
        self.sms_ui = None        # 短信记录对话框
        self.pic_ui = None        # 采血照片对话框
        self.pd_ui = None         # 进度条
        self.pd_ui_num = 0        # 进度条计数，用于处理线程->UI静态变量 弹窗造成的BUG
        self.zyd_ui = None        # 指引单对话框
        self.pop_ui =None          # 特殊信息提示 胶片、手工单、未结束项目

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
        self.gp_middle.setTitle('追踪列表（%s）' %self.table_track.rowCount() )
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
            item6 = menu.addAction(Icon("取消"), "取消到达")
            item7 = menu.addAction(Icon("编辑"), "修改备注")
            item8 = menu.addAction(Icon("报告中心"), "浏览HTML报告")
            item9 = menu.addAction(Icon("报告中心"), "浏览PDF报告")
            item10 = menu.addAction(Icon("发送"), "发送医生总检")
            item11 = menu.addAction(Icon("发送"), "发送护理审阅")
            action = menu.exec_(self.table_track.mapToGlobal(pos))
            # 获取变量
            tjbh = self.table_track.getCurItemValueOfKey('tjbh')
            sjhm = self.table_track.getCurItemValueOfKey('sjhm')
            tjzt = self.table_track.getCurItemValueOfKey('tjzt')
            zzzt = self.table_track.getCurItemValueOfKey('zzzt')
            if action == item1:
                if self.table_track.getCurItemValueOfKey('lqry'):
                    button = mes_warn(self,'您确认自己追踪本报告吗？')
                    if button == QMessageBox.Yes:
                        try:
                            # 更新
                            self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh ==tjbh).update({
                                MT_TJ_BGGL.zzgh: self.login_id,
                                MT_TJ_BGGL.zzxm: self.login_name
                            })
                            # 更新
                            self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.tjbh ==tjbh,MT_TJ_CZJLB.jllx =='0030').update({
                                MT_TJ_CZJLB.jllx: '0000',
                                MT_TJ_CZJLB.jlnr: '更换追踪人，原追踪人：%s,现追踪人：%s' %(MT_TJ_CZJLB.czxm,self.login_name)
                            })
                            # 插入记录
                            data_obj = {'jllx': '0030', 'jlmc': '报告追踪', 'tjbh': tjbh, 'mxbh': '',
                                        'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area,
                                        'jlnr': '','bz': None}
                            self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                            self.session.commit()
                            mes_about(self,'更新成功！')
                        except Exception as e:
                            self.session.rollback()
                            mes_about(self,'执行发生错误：%s' %e)
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
            elif action == item6:
                button = mes_warn(self, '您确认取消到达吗？')
                if button == QMessageBox.Yes:
                    tjbh = self.table_track.getCurItemValueOfKey('tjbh')
                    sql = " UPDATE TJ_TJDJB SET QD=NULL,QDRQ=NULL,TJZT='1' WHERE TJBH='%s';"%tjbh
                    # 插入记录
                    data_obj = {'jllx': '0007', 'jlmc': '取消签到', 'tjbh': tjbh, 'mxbh': '',
                                'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area,
                                'jlnr': '', 'bz': None}
                    try:
                        self.session.execute(sql)
                        self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                        self.session.commit()
                        mes_about(self, '取消到达成功！')
                    except Exception as e:
                        self.session.rollback()
                        mes_about(self, '执行发生错误：%s' % e)
            elif action == item7:
                tjbh = self.table_track.getCurItemValueOfKey('tjbh')
                bz= self.table_track.getCurItemValueOfKey('bz')
                text, ok = QInputDialog.getText(self, '明州体检', '当前备注信息：',QLineEdit.Normal, bz)
                if ok:
                    sql = "UPDATE TJ_TJDJB SET bz=cast('%s' as text) WHERE TJBH='%s';" %(str(text),tjbh)
                    # 插入记录
                    data_obj = {'jllx': '0000', 'jlmc': '修改备注', 'tjbh': tjbh, 'mxbh': '',
                                'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area,
                                'jlnr': '原备注内容：%s，新备注内容：%s' %(bz,str(text)), 'bz': None}
                    try:
                        self.session.execute(sql)
                        self.session.commit()
                        self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                        self.session.commit()
                        self.table_track.setCurItemValueOfKey('bz', str(text))
                        mes_about(self, '备注修改成功！')
                    except Exception as e:
                        self.session.rollback()
                        mes_about(self, '执行发生错误：%s' % e)
            elif action == item8:
                if tjzt in ['已审核','已审阅'] or zzzt in ['审阅退回','审核退回']:
                    try:
                        webbrowser.open(gol.get_value('api_report_preview') % ('html', tjbh))
                    except Exception as e:
                        mes_about(self, '打开出错，错误信息：%s' % e)
                        return
                else:
                    mes_about(self,'该顾客报告还未被审核！')
                    return

            elif action == item9:
                if tjzt=='已审阅' or zzzt in ['审阅退回','审核退回']:
                    # 优先打开 新系统生成的
                    result = self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).scalar()
                    if result:
                        filename = os.path.join(result.bglj, '%s.pdf' % tjbh).replace('D:/activefile/', '')
                        url = gol.get_value('api_pdf_new_show') % filename
                        webbrowser.open(url)
                    else:
                        try:
                            self.cxk_session = gol.get_value('cxk_session')
                            result = self.cxk_session.query(MT_TJ_PDFRUL).filter(
                                MT_TJ_PDFRUL.TJBH == tjbh).scalar()
                            if result:
                                url = gol.get_value('api_pdf_old_show') % result.PDFURL
                                webbrowser.open(url)
                            else:
                                mes_about(self, '未找到该顾客体检报告！')
                        except Exception as e:
                            mes_about(self, '查询出错，错误信息：%s' % e)
                            return
                else:
                    mes_about(self,'该顾客报告还未被审阅过，不能查看！')
                    return

            elif action == item10:
                if zzzt in ['审核退回','审阅退回']:
                    # 取消审核退回
                    sql1 = "UPDATE TJ_TJDJB SET TJZT='4',SUMOVER='0' WHERE TJBH='%s';" % tjbh
                    sql2 = "UPDATE TJ_BGGL SET BGZT='0',BGTH=NULL,SYGH=NULL,SYXM=NULL,SHRQ=NULL,SYBZ=NULL WHERE TJBH='%s';" % tjbh
                    try:
                        self.session.execute(sql1)
                        self.session.execute(sql2)
                        self.session.commit()
                    except Exception as e:
                        self.session.rollback()
                        mes_about(self,'处理失败，错误信息：%s' %e)

                else:
                    mes_about(self, "只有审阅退回/审核退回的报告才能使用此功能！")

            elif action == item11:
                if zzzt in ['审核退回', '审阅退回']:
                    # 取消审阅
                    sql1 = "UPDATE TJ_TJDJB SET TJZT='7' WHERE TJBH='%s';" % tjbh
                    sql2 = "UPDATE TJ_BGGL SET BGZT='0',BGTH=NULL,SYGH=NULL,SYXM=NULL,SHRQ=NULL,SYBZ=NULL WHERE TJBH='%s';" % tjbh
                    try:
                        self.session.execute(sql1)
                        self.session.execute(sql2)
                        self.session.commit()
                    except Exception as e:
                        self.session.rollback()
                        mes_about(self, '处理失败，错误信息：%s' % e)

                else:
                    mes_about(self, "只有审阅退回/审核退回的报告才能使用此功能！")

    # 手动接收结果
    def on_btn_receive_click(self):
        if not self.table_track.rowCount():
            mes_about(self,'请先查询后再进行手工结果接收！')
            return
        receive_ui = ResultReceiveDialog(self)
        receive_ui.started.emit(self.table_track.isSelectRowsValue('tjbh'))
        receive_ui.exec_()

    # 查询我自己追踪的任务
    def on_btn_myself_click(self,is_finish=False):
        if is_finish:
            tstart, tend = self.lt_where_search.date_range  # 日期
            results = self.session.execute(get_report_track_myself_sql(tstart, tend,self.login_id)).fetchall()
            self.table_track.load(results)
        else:
            pass

    # 发送任务
    def on_btn_send_click(self,is_doctor=True):
        zzzt = self.table_track.getCurItemValueOfKey('zzzt')
        tjbh = self.table_track.getCurItemValueOfKey('tjbh')
        if zzzt in ['审核退回','审阅退回']:
            if is_doctor:
                sql1 = "UPDATE TJ_TJDJB SET TJZT='4',SUMOVER='0' WHERE TJBH='%s';" % tjbh
                data_obj = {'jllx': '0123', 'jlmc': '报告退回处理', 'tjbh': tjbh, 'mxbh': '',
                            'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area,
                            'jlnr': '%s -> %s，%s：已处理 -> 医生审核' %(zzzt,cur_datetime(),self.login_name)
                            }
            else:
                sql1 = "UPDATE TJ_TJDJB SET TJZT='7' WHERE TJBH='%s';" % tjbh
                data_obj = {'jllx': '0123', 'jlmc': '报告退回处理', 'tjbh': tjbh, 'mxbh': '',
                            'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area,
                            'jlnr': '%s -> %s，%s：已处理 -> 护理审阅' %(zzzt,cur_datetime(),self.login_name)
                            }
            sql2 = "UPDATE TJ_BGGL SET BGZT='1',BGTH=NULL,SYGH=NULL,SYXM=NULL,SHRQ=NULL,SYBZ=NULL WHERE TJBH='%s';" % tjbh
            try:
                self.session.execute(sql1)
                self.session.execute(sql2)
                self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                self.session.commit()
                mes_about(self,'处理成功！')
            except Exception as e:
                self.session.rollback()
                mes_about(self, '处理失败，错误信息：%s' % e)
        else:
            mes_about(self,"只有审阅退回/审核退回的报告才能使用此功能！")

    # 查看导检单
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
        if self.lt_where_search.where_bgzt_text =='待追踪':
            sql = get_report_track_sql(tstart, tend)
        elif self.lt_where_search.where_bgzt_text =='追踪中':
            sql = get_report_tracking_sql(tstart, tend)
        elif self.lt_where_search.where_bgzt_text == '待总检':
            sql = get_report_tracked_sql(tstart, tend)
        elif self.lt_where_search.where_bgzt_text == '待审核':
            sql = get_report_tracked_zj_sql(tstart, tend)
        elif self.lt_where_search.where_bgzt_text == '待审阅':
            sql = get_report_tracked_sh_sql(tstart, tend)
        elif self.lt_where_search.where_bgzt_text == '待打印':
            sql = get_report_tracked_sy_sql(tstart, tend)
        else:
            sql = None

        where_tjqy = self.lt_where_search.where_tjqy             # 体检区域
        if where_tjqy:
            sql = sql + where_tjqy

        where_tjlx = self.cb_report_type.where_tjlx               # 体检类型
        if where_tjlx:
            sql = sql +where_tjlx

        where_dwmc = self.lt_where_search.where_dwmc              # 体检单位
        if where_dwmc:
            sql = sql + where_dwmc

        # # 待总检的特殊处理下
        if self.lt_where_search.where_bgzt_text == '待总检':
             sql = sql + ''' LEFT JOIN TJ_BGGL ON T1.TJBH =TJ_BGGL.TJBH '''
        else:
        # # 追踪类型 待总检不做此筛选
            if not self.cb_track_type.text():
                if self.lt_where_search.where_bgzt_text == '待追踪':
                    # 所有
                    sql = sql + ''' UNION ALL ''' + get_report_shth_sql()+ ''' UNION ALL ''' + get_report_syth_sql()
                    sql = sql + ''' ORDER BY zzzt desc,XMZQ,QDRQ,DWMC  '''
                else:
                    sql = sql
            elif self.cb_track_type.text() == '未结束':
                sql = sql + ''' ORDER BY d.XMZQ,T1.QDRQ,T1.DWMC  '''
            elif self.cb_track_type.text() == '审核退回':
                sql = get_report_shth_sql()
            else:
                sql = get_report_syth_sql()


        # print(sql)
        # 执行查询
        self.execQuery(sql)
        # 进度条
        self.pd_ui = ProgressDialog(self)
        self.pd_ui.show()

    # 设置快速检索文本
    def on_table_set(self,tableWidgetItem):
        row = tableWidgetItem.row()
        zzzt = self.table_track.getItemValueOfKey(row, 'zzzt')
        tjbh = self.table_track.getItemValueOfKey(row,'tjbh')
        xm = self.table_track.getItemValueOfKey(row,'xm')
        sfzh = self.table_track.getItemValueOfKey(row,'sfzh')
        sjhm = self.table_track.getItemValueOfKey(row,'sjhm')
        self.gp_quick_search.setText(tjbh,xm,sjhm,sfzh)
        self.cur_tjbh = tjbh
        if not self.pop_ui:
            self.pop_ui = ReportPopWidget(self)
        self.pop_ui.show()
        if zzzt in ['审阅退回','审核退回']:
            reason = self.table_track.getItemValueOfKey(row, 'wjxm')
        else:
            reason = ''
        # 传递数据
        self.pop_ui.inited.emit("体检编号：%s  姓名：%s" %(tjbh,xm),self.cur_tjbh,reason)


    #体检系统项目查看
    def on_btn_item_click(self):
        if not self.item_ui:
            self.item_ui = ItemsStateUI(self)
        self.item_ui.show()
        if self.cur_tjbh:
            self.item_ui.returnPressed.emit(self.cur_tjbh)


    #体检系统项目查看
    def on_btn_czjl_click(self):
        if not self.operatr_ui:
            self.operatr_ui = OperateUI(self)
        self.operatr_ui.show()
        if self.cur_tjbh:
            self.operatr_ui.returnPressed.emit(self.cur_tjbh)


    #体检系统项目查看
    def on_btn_equip_click(self):
        if not self.equip_ui:
            self.equip_ui = EquipUI(self)
        self.equip_ui.show()
        if self.cur_tjbh:
            self.equip_ui.returnPressed.emit(self.cur_tjbh)

    # 电话记录
    def on_btn_phone_click(self):
        sjhm = self.table_track.getCurItemValueOfKey('sjhm')
        if not self.cur_tjbh:
            mes_about(self, '请先选择一个人！')
            return
        else:
            if not self.phone_ui:
                self.phone_ui = PhoneUI(self)
            self.phone_ui.show()
            self.phone_ui.returnPressed.emit(self.cur_tjbh, sjhm)

    # 短信记录
    def on_btn_sms_click(self):
        if not self.cur_tjbh:
            mes_about(self, '请先选择一个人！')
            return
        else:
            sjhm = self.table_track.getCurItemValueOfKey('sjhm')
            if not self.sms_ui:
                self.sms_ui = SmsUI(self)
            self.sms_ui.show()
            self.sms_ui.returnPressed.emit(self.cur_tjbh,sjhm)


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
            self.pis_ui.show()
            self.pis_ui.setData(results)

        elif sys_name =='LIS':
            if not self.lis_ui:
                self.lis_ui = LisResult(self)
            self.lis_ui.show()
            self.lis_ui.setData(results)

        elif sys_name =='PACS':
            if not self.pacs_ui:
                self.pacs_ui = PacsResult(self)
            self.pacs_ui.show()
            self.pacs_ui.setData(results)

        else:
            pass

    # 追踪任务领取
    def on_btn_task_click(self,is_two=True):
        tmp = []
        rows = self.table_track.isSelectRows()
        button = mes_warn(self, "您确认领取当前选择的 %s 份体检报告？" %len(rows))
        if button != QMessageBox.Yes:
            return
        if is_two:
            pass
        else:
            for row in rows:
                if not self.table_track.getItemValueOfKey(row,'lqry'):
                    data_obj = {'jllx': '0030', 'jlmc': '报告追踪', 'tjbh': '', 'mxbh': '',
                                'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area, 'jlnr': None,
                                'bz': None}
                    tjbh = self.table_track.getItemValueOfKey(row,'tjbh')
                    jlnr = self.table_track.getItemValueOfKey(row,'wjxm')
                    data_obj['tjbh'] = tjbh
                    data_obj['jlnr'] = jlnr
                    tmp.append(data_obj)
                    self.table_track.item(row, 2).setText('追踪中')
                    self.table_track.item(row, 3).setText(self.login_name)

                    result = self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).scalar()
                    if result:
                        self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).update(
                            {
                                MT_TJ_BGGL.zzxm: self.login_name,
                                MT_TJ_BGGL.zzgh: self.login_id,
                                MT_TJ_BGGL.zzrq: cur_datetime(),
                                MT_TJ_BGGL.bgzt: '0',
                            }
                        )
                    else:self.session.bulk_insert_mappings(MT_TJ_BGGL, [{'tjbh':tjbh,'bgzt':'0','zzxm':self.login_name,'zzgh':self.login_id,'zzrq':cur_datetime()}])
                    self.session.commit()

                    if len(rows)==1:
                        mes_about(self, '领取成功！')
            if tmp:
                try:
                    self.session.bulk_insert_mappings(MT_TJ_CZJLB, tmp)
                    self.session.commit()
                    if len(rows)>1:
                        mes_about(self, '领取成功！')
                except Exception as e:
                    self.session.rollback()
                    mes_about(self, '插入 TJ_CZJLB 记录失败！错误代码：%s' % e)

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

class ResultReceiveDialog(Dialog):

    started = pyqtSignal(list)

    def __init__(self,parent=None):
        super(ResultReceiveDialog,self).__init__(parent)
        self.setWindowTitle('明州体检')
        self.initUI()
        # 绑定信号
        self.started.connect(self.initDatas)
        self.btn_start.clicked.connect(self.on_btn_start_click)
        self.btn_stop.clicked.connect(self.on_btn_stop_click)
        # 特殊变量
        self.datas = None
        self.result_receive_thread = None

    def initUI(self):
        lt_main = QVBoxLayout()
        ###########################################################
        lt_top = QHBoxLayout()
        gp_top = QGroupBox('进度总览')
        # 待接收的总数
        self.sb_all = ProcessLable()
        # 已完成接收数
        self.sb_is_done = ProcessLable()
        # 未完成总数
        self.sb_no_done = ProcessLable()
        # 错误数
        self.sb_error = ProcessLable()
        # 添加布局
        lt_top.addWidget(QLabel('总数：'))
        lt_top.addWidget(self.sb_all)
        lt_top.addWidget(QLabel('完成数：'))
        lt_top.addWidget(self.sb_is_done)
        lt_top.addWidget(QLabel('未完成数：'))
        lt_top.addWidget(self.sb_no_done)
        lt_top.addWidget(QLabel('错误数：'))
        lt_top.addWidget(self.sb_error)
        gp_top.setLayout(lt_top)
        ###########################################################
        lt_middle = QHBoxLayout()
        gp_middle = QGroupBox('处理详情')
        ###########################################################
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox('接收进度')
        self.pb_progress=QProgressBar()
        self.pb_progress.setMinimum(0)
        self.pb_progress.setValue(0)
        lt_bottom.addWidget(self.pb_progress)
        gp_bottom.setLayout(lt_bottom)
        #########增加按钮组########################################
        lt_1 = QHBoxLayout()
        self.lb_timer = TimerLabel2()
        self.btn_start = QPushButton(Icon("启动"),"启动")
        self.btn_stop = QPushButton(Icon("停止"),"停止")
        lt_1.addWidget(self.lb_timer)
        lt_1.addStretch()
        lt_1.addWidget(self.btn_start)
        lt_1.addWidget(self.btn_stop)
        # 布局
        lt_main.addWidget(gp_top)
        lt_main.addWidget(gp_middle)
        lt_main.addWidget(gp_bottom)
        lt_main.addLayout(lt_1)
        self.setLayout(lt_main)

    def on_progress_change(self,is_done,no_done,error):
        self.sb_is_done.setText(str(is_done))
        self.sb_no_done.setText(str(no_done))
        self.sb_error.setText(str(error))
        self.pb_progress.setValue(is_done)
        dProgress = (self.pb_progress.value() - self.pb_progress.minimum()) * 100.0 / (self.pb_progress.maximum() - self.pb_progress.minimum())
        #self.progress.setFormat("当前进度为：%s%" %dProgress)
        self.pb_progress.setAlignment(Qt.AlignRight | Qt.AlignVCenter) #对齐方式

    # 启动
    def on_btn_start_click(self):
        # 刷新界面控件
        self.btn_start.setDisabled(True)
        self.btn_stop.setDisabled(False)
        self.lb_timer.start()
        self.sb_all.setText(str(len(self.datas)))
        self.pb_progress.setMaximum(len(self.datas))
        if not self.result_receive_thread:
            self.result_receive_thread = ResultReceiveThread()

        self.result_receive_thread.setTask(self.datas)
        self.result_receive_thread.signalCur.connect(self.on_mes_show, type=Qt.QueuedConnection)
        self.result_receive_thread.signalDone.connect(self.on_progress_change, type=Qt.QueuedConnection)
        self.result_receive_thread.signalExit.connect(self.on_thread_exit, type=Qt.QueuedConnection)
        self.result_receive_thread.start()

    # 停止接收数据
    def on_btn_stop_click(self):
        # 刷新界面控件
        self.btn_start.setDisabled(False)
        self.btn_stop.setDisabled(True)
        self.lb_timer.stop()
        # 停止线程
        try:
            if self.result_receive_thread:
                self.result_receive_thread.stop()
        except Exception as e:
            print(e)

    # 初始化数据
    def initDatas(self,datas:list):
        self.datas = datas
        self.on_btn_start_click()

    # 消息展示
    def on_mes_show(self,tjbh:str,mes:str):
        pass

    def on_thread_exit(self,status:bool,error:str):
        self.on_btn_stop_click()
        self.result_receive_thread = None

        mes_about(self,error)

    def closeEvent(self, QCloseEvent):
        try:
            if self.result_receive_thread:
                # button = mes_warn(self,"项目结果接收正在运行中，您是否确定立刻退出？")
                # if button == QMessageBox.Yes:
                self.result_receive_thread.stop()
                self.result_receive_thread = None
        except Exception as e:
            print(e)
        super(ResultReceiveDialog, self).closeEvent(QCloseEvent)

# 运行线程
class ResultReceiveThread(QThread):

    # 定义信号,定义参数为str类型
    signalCur = pyqtSignal(str,str)     # 处理过程：成功/失败，错误消息，
    signalDone = pyqtSignal(int, int, int)   # 处理完成：成功/失败，错误消息，
    signalExit = pyqtSignal(bool,str)   # 处理结束：成功/失败，是否异常退出

    def __init__(self):
        super(ResultReceiveThread,self).__init__()
        self.runing = False
        self.initParas()
        # 特殊变量
        self.num_all = 0
        self.num_done = 0
        self.num_undone = 0
        self.num_error = 0

    def initParas(self):
        # 获取数据库连接会话
        self.session_tj = gol.get_value("tjxt_session_thread")
        self.session_pacs = gol.get_value("pacs_session")
        self.session_pis = gol.get_value("pis_session")
        self.session_lis = gol.get_value("lis_session")
        self.num = 1

    def stop(self):
        self.runing = False

    # 启动任务
    def setTask(self,tjbhs:list):
        self.tjbhs =tjbhs
        self.num_all = len(tjbhs)
        self.runing = True

    def run(self):
        while self.runing:
            for tjbh in self.tjbhs:
                # 连接PACS数据库，读取并接收更新
                try:
                    pacs_results = self.session_pacs.execute(get_pacs_result_sql(tjbh)).fetchall()
                    self.signalCur.emit(tjbh, "接收检查项目结果")
                except Exception as e:
                    self.stop()
                    self.signalExit.emit(False, "接收结果中断，错误信息：%s" %e)
                    return
                if pacs_results:
                    for result in pacs_results:
                        tjbh = result[0][0:9]       # 体检编号
                        xmbh = result[0][9:]        # 项目编号
                        shys = result[1]            # 审核医生
                        shsj = result[2]            # 审核时间
                        xmjg = result[3]            # 项目结果
                        xmzd = result[4]            # 项目诊断
                        # print(tjbh,xmbh,shys,shsj)
                        # 更新数据库
                        update_items_inspect(self.session_tj,tjbh,xmbh,shys,shsj,xmjg,xmzd)
                # 连接PIS数据库，读取并接收更新
                try:
                    pis_results = self.session_pis.execute(get_pis_result_sql(tjbh)).fetchall()
                    self.signalCur.emit(tjbh, "接收病理项目结果")
                except Exception as e:
                    self.stop()
                    self.signalExit.emit(False, "连接病理数据库发生错误，错误信息：%s" %e)
                    return
                if pis_results:
                    for result in pis_results:
                        tjbh = result[0][0:9]       # 体检编号
                        xmbh = result[0][9:]        # 项目编号
                        shys = result[1]            # 审核医生
                        shsj = result[2]            # 审核时间
                        if result[3]:
                            xmjg = result[3]            # 项目结果
                        else:
                            xmjg = result[4]            # 项目诊断 当做结果
                        xmzd = result[4]            # 项目诊断
                        filename = result[5]        # 病理图片路径
                        update_items_inspect(self.session_tj, tjbh, xmbh, shys, shsj, xmjg, xmzd,filename)
                self.num_done = self.num_done + 1
                self.num_undone = self.num_all - self.num_done
                self.signalDone.emit(self.num_done,self.num_undone,self.num_error)
            self.stop()
            self.signalExit.emit(True, "数据接收完成")


def get_pacs_result_sql(tjbh):
    return '''
        SELECT 
            HISORDER_IID,
            RIS_BG_CSHYS AS SHYS,
            RIS_BG_DSHSJ AS SHSJ,
            RIS_BG_CBGSJ_HL7 AS XMJG,
            RIS_BG_CBGZD AS XMZD 
        FROM V_RIS2HIS_ALL 
            WHERE CBLKH = '%s' AND CBGZT='已审核'
    ''' %tjbh

def get_pis_result_sql(tjbh):
    return '''
        SELECT  
            HIS_keyCode,
            AuditDoc,
            AuditDate,
            TJSJ,
            TJZD,
            filename
        FROM V_PS_Report_TJ WHERE LEFT(HIS_keyCode,9)='%s' AND OrderState=3030;
    ''' %tjbh

# 更新结果记录表 检查和病理
def update_items_inspect(session,tjbh,xmbh,shys,shsj,xmjg,xmzd,filename=None):
    result = session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,
                                                 MT_TJ_TJJLMXB.zhbh == xmbh,
                                                 MT_TJ_TJJLMXB.sfzh == '1'
                                                 ).scalar()
    # 是否存在项目
    if result:
        if result.qzjs == '1':
            pass
        elif result.zxpb == '1' and result.jsbz == '1':
            pass
        else:
            try:
                session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh, MT_TJ_TJJLMXB.zhbh == xmbh).update({
                    MT_TJ_TJJLMXB.shys: shys,
                    MT_TJ_TJJLMXB.shsj: shsj,
                    MT_TJ_TJJLMXB.zxpb: '1',
                    MT_TJ_TJJLMXB.jsbz: '1',
                    MT_TJ_TJJLMXB.qzjs: None,
                    MT_TJ_TJJLMXB.ycbz: '1',
                    MT_TJ_TJJLMXB.ycts: ''
                })
                session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh, MT_TJ_TJJLMXB.zhbh == xmbh,
                                                            MT_TJ_TJJLMXB.sfzh == '0').update({
                    MT_TJ_TJJLMXB.jg: xmjg,
                    MT_TJ_TJJLMXB.zd: xmzd
                })
                session.commit()
            except Exception as e:
                session.rollback()
    if filename:
        result = session.query(MT_TJ_PACS_PIC).filter(MT_TJ_PACS_PIC.tjbh == tjbh,MT_TJ_PACS_PIC.zhbh == xmbh).scalar()
        if not result:
            data_obj = {
                'tjbh':tjbh,
                'ksbm':'0026',
                'picpath':filename,
                'picname': filename,
                'path': filename,
                'zhbh':xmbh,
                'ftp_bz':'0'
            }
            try:
                session.bulk_insert_mappings(MT_TJ_PACS_PIC, [data_obj])
                session.commit()
            except Exception as e:
                session.rollback()

# 更新结果记录表
def update_items_lis(session,tjbh,xmbh,shys,shsj,xmjg,xmzd):
    result = session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,
                                                 MT_TJ_TJJLMXB.zhbh == xmbh,
                                                 MT_TJ_TJJLMXB.sfzh == '1'
                                                 ).scalar()
    # 是否存在项目
    if result:
        if result.qzjs == '1':
            pass
        elif result.zxpb == '1' and result.jsbz == '1':
            pass
        else:
            try:
                session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh, MT_TJ_TJJLMXB.zhbh == xmbh).update({
                    MT_TJ_TJJLMXB.shys: shys,
                    MT_TJ_TJJLMXB.shsj: shsj,
                    MT_TJ_TJJLMXB.zxpb: '1',
                    MT_TJ_TJJLMXB.jsbz: '1',
                    MT_TJ_TJJLMXB.qzjs: None,
                    MT_TJ_TJJLMXB.ycbz: '1',
                    MT_TJ_TJJLMXB.ycts: ''
                })
                session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh, MT_TJ_TJJLMXB.zhbh == xmbh,
                                                            MT_TJ_TJJLMXB.sfzh == '0').update({
                    MT_TJ_TJJLMXB.jg: xmjg,
                    MT_TJ_TJJLMXB.zd: xmzd
                })
                session.commit()
            except Exception as e:
                session.rollback()

class ProcessLable(QLabel):

    def __init__(self):
        super(ProcessLable,self).__init__()
        self.setMinimumWidth(50)
        self.setStyleSheet('''font: 75 14pt \"微软雅黑\";color: rgb(0, 85, 255);''')


# 弹出框
class ReportPopWidget(Dialog):

    inited = pyqtSignal(str,str,str)    # 人员信息、体检编号、退回原因

    def __init__(self,parent=None):
        super(ReportPopWidget, self).__init__(parent)
        self.initUI()
        self.inited.connect(self.on_search)

    # 传递体检编号
    def on_search(self,ryxx,tjbh,reason):
        # 刷新标题
        self.setWindowTitle(ryxx)
        # 手工报告单 # xmbh in ['1122', '1931', '0903', '501732', '501933', '501934']:
        results = self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,
                                                           MT_TJ_TJJLMXB.sfzh == '1',
                                                           MT_TJ_TJJLMXB.zhbh.in_(['1122', '1931', '0903', '501732', '501933', '501934'])).all()
        self.lb_manual.setText("  ".join([str2(result.xmmc) for result in results]))
        self.gp_top.setTitle('手工单报告(%s)' %str(len(results)))

        # 胶片数据
        film = {}
        results = self.session.execute(get_film_num(tjbh))
        for result in results:
            film[result[0]] = result[1]
        # 更新
        self.init_film(film)
        # 获取未结束项目
        results = self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh==tjbh,MT_TJ_TJJLMXB.sfzh=='1',MT_TJ_TJJLMXB.jsbz!='1').all()
        self.table_no_finish.load([result.item_result2 for result in results])
        self.gp_bottom.setTitle('未结束项目（%s）' %self.table_no_finish.rowCount())
        # 报告退回 处理信息
        if reason:
            # 剔除未完成项目布局
            self.lb_reason.setText(reason)
            # try:
            #     self.layout().removeWidget(self.gp_bottom)
            #     self.layout().addWidget(self.gp_bottom2)
            # except Exception as e:
            #     print(e,111111)
        else:
            self.lb_reason.setText('')
            # try:
            #     self.layout().removeWidget(self.gp_bottom2)
            #     self.layout().addWidget(self.gp_bottom)
            # except Exception as e:
            #     print(e,22222222)

    def initUI(self):
        lt_main = QVBoxLayout()
        self.gp_top = QGroupBox('手工单报告(0)')
        self.lt_top = QHBoxLayout()
        self.lb_manual = QLabel()
        self.lb_manual.setWordWrap(True)
        self.lb_manual.setStyleSheet('''color: rgb(0, 85, 255);''')
        self.lt_top.addWidget(self.lb_manual)
        self.gp_top.setLayout(self.lt_top)
        ######################胶片数量###################################
        self.gp_middle = QGroupBox('胶片数量(0)')
        lt_middle = QHBoxLayout()
        self.lb_count_dr = FilmLable()
        self.lb_count_ct = FilmLable()
        self.lb_count_mri = FilmLable()
        lt_middle.addWidget(QLabel('DR：'))
        lt_middle.addWidget(self.lb_count_dr)
        lt_middle.addSpacing(10)
        lt_middle.addWidget(QLabel('CT：'))
        lt_middle.addWidget(self.lb_count_ct)
        lt_middle.addSpacing(10)
        lt_middle.addWidget(QLabel('MRI：'))
        lt_middle.addWidget(self.lb_count_mri)
        lt_middle.addSpacing(10)
        lt_middle.addStretch()
        self.gp_middle.setLayout(lt_middle)
        ######################未结束项目###################################
        self.gp_bottom = QGroupBox('未结束项目')
        lt_bottom  = QHBoxLayout()
        self.gp_bottom.setLayout(lt_bottom)
        self.table_no_finish_cols = OrderedDict(
            [
                ("state", "状态"),
                ("xmbh", "编号"),
                ("xmmc", "项目名称"),
                ("btn", "")
             ])
        self.table_no_finish = ItemTable(self.table_no_finish_cols)
        lt_bottom.addWidget(self.table_no_finish)
        self.gp_bottom.setLayout(lt_bottom)
        ######################退回原因###################################
        self.gp_bottom2 = QGroupBox('退回原因')
        lt_bottom2 = QHBoxLayout()
        self.lb_reason = QLabel()
        self.lb_reason.setStyleSheet('''color:#FF0000;''')
        self.lb_reason.setWordWrap(True)
        lt_bottom2.addWidget(self.lb_reason)
        self.gp_bottom2.setLayout(lt_bottom2)
        # 添加布局
        lt_main.addWidget(self.gp_top)
        lt_main.addWidget(self.gp_middle)
        lt_main.addWidget(self.gp_bottom)
        lt_main.addWidget(self.gp_bottom2)
        # lt_main.addStretch()
        self.setLayout(lt_main)

        self.setWindowIcon(Icon('mztj'))
        # 移动整体位置
        desktop = QDesktopWidget()
        self.setFixedHeight(500)
        self.setFixedWidth(400)
        self.move((desktop.availableGeometry().width()-self.width()-20),
                  desktop.availableGeometry().height()-self.height()-120)  # 初始化位置到右下角

    # 初始化胶片信息
    def init_film(self,film:dict):
        self.lb_count_dr.setText(str(film.get('DR','')))
        self.lb_count_ct.setText(str(film.get('CT', '')))
        self.lb_count_mri.setText(str(film.get('MRI', '')))
        self.gp_middle.setTitle('胶片数量(%s)' %str(film.get('DR',0)+film.get('CT',0)+film.get('MRI',0)))

class FilmLable(QLabel):

    def __init__(self):
        super(FilmLable,self).__init__()
        self.setMinimumWidth(50)
        self.setStyleSheet('''font: 75 14pt \"微软雅黑\";color: rgb(0, 85, 255);''')


# 报告审阅列表
class ItemTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(ItemTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # 字典载入
        tmp = None  #获取第一列的值
        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)  # 插入一行
            for col_index, col_name in enumerate(self.heads):
                col_value = row_data[col_name]
                if col_index==0:
                    item = QTableWidgetItem(col_value)
                    tmp = col_value
                    if col_value in ['已检查','已抽血','已留样']:
                        item.setBackground(QColor("#f0e68c"))
                    elif col_value in ['核实','未定义']:
                        item.setBackground(QColor("#FF0000"))
                    elif col_value == '已拒检':
                        item.setBackground(QColor("#008000"))
                    elif col_value == '已接收':
                        item.setBackground(QColor("#b0c4de"))
                    elif col_value == '已回写':
                        item.setBackground(QColor("#1e90ff"))
                    elif col_value == '已登记':
                        item.setBackground(QColor("#b0c4de"))
                    else:
                        pass
                    item.setTextAlignment(Qt.AlignCenter)
                elif col_index == len(self.heads)-1:
                    if tmp=='已小结':
                        item = QTableWidgetItem('')
                    elif tmp=='核实':
                        item = QTableWidgetItem('拒检')
                        item.setFont(get_font())
                        item.setBackground(QColor(218, 218, 218))
                        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    else:
                        item = QTableWidgetItem('核实')
                        item.setFont(get_font())
                        item.setBackground(QColor(218, 218, 218))
                        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                else:
                    item = QTableWidgetItem(row_data[col_name])
                    # item.setTextAlignment(Qt.AlignCenter)

                self.setItem(row_index, col_index, item)
        # 布局
        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 180)
        self.horizontalHeader().setStretchLastSection(True)