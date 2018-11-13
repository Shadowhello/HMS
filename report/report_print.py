from .report_print_ui import *
from .model import *
from .report_item_ui import ItemsStateUI
from utils import request_get,print_pdf_gsprint,cur_datetime,request_create_report
from widgets.bweb import WebView
import webbrowser
from .common import *
from widgets import QBrowser

# 报告追踪
class ReportPrint(ReportPrintUI):

    def __init__(self):
        super(ReportPrint, self).__init__()
        self.initParas()
        # 绑定信号槽
        self.btn_query.clicked.connect(self.on_btn_query_click)
        self.btn_down.clicked.connect(self.on_btn_down_click)
        self.btn_print.clicked.connect(self.on_btn_print_click)
        self.btn_receive.clicked.connect(self.on_btn_receive_click)
        self.btn_order.clicked.connect(self.on_btn_order_click)
        self.btn_rebuild.clicked.connect(self.on_btn_rebuild_click)
        # 右键、双击、单击
        self.table_print.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.table_print.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单
        self.table_print.itemClicked.connect(self.on_table_set)
        self.table_print.itemDoubleClicked.connect(self.on_btn_item_click)
        # 快速减速
        self.gp_quick_search.returnPressed.connect(self.on_quick_search)    # 快速检索
        # 特殊变量
        self.cur_tjbh = None
        self.web_pdf_ui = None
        # 网络打印进度
        self.net_print_ui = None
        self.browser = None
        self.pop_ui = None
        # 当次打印数据
        self.print_datas = None
        self.item_ui = None

    # 初始化部分参数
    def initParas(self):
        self.ini_is_remote = gol.get_value('print_network',1)
        self.ini_printer = gol.get_value('print_printer', '79号打印机')
        self.gp_print_setup.setParas(self.ini_is_remote,self.ini_printer)
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
        sql = get_report_print2_sql()
        sql = sql + ''' INNER JOIN TJ_TJDAB ON TJ_TJDJB.DABH=TJ_TJDAB.DABH '''
        sql = sql +''' AND ''' + where_str
        results = self.session.execute(sql).fetchall()
        self.table_print.load(results)
        self.gp_middle.setTitle('打印列表（%s）' %self.table_print.rowCount())
        self.lb_warn.show()
        mes_about(self,'共检索出 %s 条数据！' %self.table_print.rowCount())

    # 打印更新UI
    def on_print_refresh(self,tjbh,state):
        dyfs,dyfs2,printer = self.gp_print_setup.get_print_text()
        # 更新UI
        row = self.print_datas[tjbh]
        if state:
            bgzt = self.table_print.getItemValueOfKey(row, 'bgzt')
            # 获取实际应该更新的状态
            bgzt_name, bgzt_value = get_bgzt(bgzt, '已打印')
            self.table_print.setItemValueOfKey(row, 'dyrq', cur_datetime())
            self.table_print.setItemValueOfKey(row, 'dyr', self.login_name)
            self.table_print.setItemValueOfKey(row, 'dycs', '1')
            self.table_print.setItemValueOfKey(row, 'dyfs', dyfs2)
            self.table_print.setItemValueOfKey(row, 'bgzt', bgzt_name,QColor("#008000"))
            # 更新数据库
            try:
                # 更新TJ_CZJLB TJ_BGGL
                data_obj = {'jllx': '0034', 'jlmc': '报告打印', 'tjbh': tjbh, 'mxbh': '',
                            'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area,
                            'bz': '打印机：%s' % printer}
                self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).update(
                    {
                        MT_TJ_BGGL.dyrq: cur_datetime(),
                        MT_TJ_BGGL.dyfs: dyfs,
                        MT_TJ_BGGL.dygh: self.login_id,
                        MT_TJ_BGGL.dyxm: self.login_name,
                        MT_TJ_BGGL.dycs: MT_TJ_BGGL.dycs + 1,
                        MT_TJ_BGGL.bgzt: bgzt_value,
                        MT_TJ_BGGL.dyzt: None
                    }
                )
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                mes_about(self, '更新数据库失败！错误信息：%s' % e)
                return
        else:
            # 打印失败
            self.table_print.setItemValueOfKey(row, 'bgzt', '打印失败', QColor("#FF0000"))
            try:
                self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).update(
                    {
                        MT_TJ_BGGL.dyzt: '1',
                        MT_TJ_BGGL.bgzt: '3',
                    }
                )
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                mes_about(self, '更新数据库失败！错误信息：%s' % e)
                return

    def on_btn_rebuild_click(self):
        rows = self.table_print.isSelectRows()
        button = mes_warn(self, "温馨提示：\n您确认重新生成当前选择的 %s 份体检报告？" %len(rows))
        if button != QMessageBox.Yes:
            return
        count = 0
        for row in rows:
            tjbh = self.table_print.getItemValueOfKey(row,'tjbh')
            if request_create_report(tjbh, 'pdf'):
                count = count + 1

        mes_about(self, '报告总数：%s，重新生成：%s' % (len(rows), count))

    # 打印
    def on_btn_print_click(self):
        qdrq = self.table_print.getCurItemValueOfKey('qdrq')
        bgzt = self.table_print.getCurItemValueOfKey('bgzt')
        if not date_compare(qdrq,'2018-10-01'):
            if bgzt in ['','已审核']:
                mes_about(self,'当前报告还未被审阅，不允许打印！')
                return
        rows = self.table_print.isSelectRows()
        if not rows:
            return
        is_remote,printer = self.gp_print_setup.get_printer()
        self.printer = printer
        button = mes_warn(self, "您确认用打印机：%s，打印当前选择的 %s 份体检报告？" %(printer,len(rows)))
        if button != QMessageBox.Yes:
            return
        net_print_ui = ReportPrintProgress(self)
        # 并更新UI
        self.print_datas = self.table_print.isSetRowsValue('tjbh','bgzt','打印中',QColor('#FFB90F'))
        # 发送打印信号
        net_print_ui.print_init.emit(list(self.print_datas.keys()),printer,is_remote)
        # 更新数据库：打印中 方便其他客户端进行筛选，避免重复打印
        try:
            self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh.in_(tuple(list(self.print_datas.keys())))).update(
                {
                    MT_TJ_BGGL.dyzt: '0',
                    MT_TJ_BGGL.bgzt: '3',
                },synchronize_session=False
            )
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            mes_about(self, '更新数据库失败！错误信息：%s' % e)
            return
        # 打印接收信号
        net_print_ui.printed.connect(self.on_print_refresh)
        net_print_ui.exec_()

        # 主线程打印 会卡主界面，放弃
        # if rows:
        #     for row in rows:
        #         tjbh = self.table_print.getItemValueOfKey(row, 'tjbh')
        #         dyrq = self.table_print.getItemValueOfKey(row, 'dyrq')
        #         dyr = self.table_print.getItemValueOfKey(row, 'dyr')
        #         dycs = self.table_print.getItemValueOfKey(row, 'dycs')
        #         bgzt = self.table_print.getItemValueOfKey(row, 'bgzt')
        #         bgzt_name,bgzt_value = get_bgzt(bgzt,'已打印')
        #         if is_remote:
        #             pass
        #         else:
        #             # 本地打印 需要下载
        #             url = gol.get_value('api_report_down') %tjbh
        #             filename = os.path.join(gol.get_value('path_tmp'),'%s.pdf' %tjbh)
        #             if request_get(url,filename):
        #                 # 下载成功
        #                 if print_pdf_gsprint(filename) == 0:
        #                     try:
        #                         # 更新数据库 TJ_CZJLB TJ_BGGL
        #                         data_obj = {'jllx': '0034', 'jlmc': '报告打印', 'tjbh': tjbh, 'mxbh': '',
        #                                     'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area,
        #                                     'bz': '本地打印：%s' %printer}
        #                         self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
        #                         self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).update(
        #                             {
        #                                 MT_TJ_BGGL.dyrq: cur_datetime(),
        #                                 MT_TJ_BGGL.dyfs: '2',
        #                                 MT_TJ_BGGL.dygh: self.login_id,
        #                                 MT_TJ_BGGL.dyxm: self.login_name,
        #                                 MT_TJ_BGGL.dycs: MT_TJ_BGGL.dycs + 1,
        #                                 MT_TJ_BGGL.bgzt: bgzt_value
        #                             }
        #                         )
        #                         self.session.commit()
        #                     except Exception as e:
        #                         self.session.rollback()
        #                         mes_about(self, '更新数据库失败！错误信息：%s' % e)
        #                         return
        #                     # 刷新界面
        #                     self.table_print.setItemValueOfKey(row, 'dyrq',cur_datetime())
        #                     self.table_print.setItemValueOfKey(row, 'dyr', self.login_name)
        #                     self.table_print.setItemValueOfKey(row, 'dycs', '1')
        #                     self.table_print.setItemValueOfKey(row, 'dyfs', '本地打印')
        #                     self.table_print.setItemValueOfKey(row, 'bgzt', bgzt_name)
        #                     if len(rows) == 1:
        #                         mes_about(self, "打印成功！")
        #                 else:
        #                     mes_about(self, "打印失败！")
        #             else:
        #                 mes_about(self,'未找到报告，无法打印！')
        #     if len(rows) > 1:
        #         mes_about(self, "打印成功！")
        # else:
        #     mes_about(self,'请选择要打印的报告！')

    # 查询
    def on_btn_query_click(self):
        if self.lt_where_search.where_dwbh=='00000':
            mes_about(self,'不存在该单位，请重新选择！')
            return
        sql = get_report_print_sql()
        t_start,t_end = self.lt_where_search.date_range
        if self.lt_where_search.get_date_text() == '签到日期':
            sql = sql + ''' AND TJ_TJDJB.QDRQ>= '%s' AND TJ_TJDJB.QDRQ< '%s' ''' %(t_start,t_end)
        elif self.lt_where_search.get_date_text() == '总检日期':
            sql = sql + ''' AND TJ_TJDJB.ZJRQ>= '%s' AND TJ_TJDJB.ZJRQ< '%s' ''' %(t_start,t_end)
        elif self.lt_where_search.get_date_text() == '审核日期':
            sql = sql + ''' AND TJ_TJDJB.SHRQ>= '%s' AND TJ_TJDJB.SHRQ< '%s' ''' %(t_start,t_end)
        elif self.lt_where_search.get_date_text() == '审阅日期':
            sql = sql + ''' AND TJ_BGGL.SYRQ>= '%s' AND TJ_BGGL.SYRQ< '%s' ''' %(t_start,t_end)
        elif self.lt_where_search.get_date_text() == '登记日期':
            sql = sql + ''' AND TJ_TJDJB.DJRQ>= '%s' AND TJ_TJDJB.DJRQ< '%s' ''' %(t_start,t_end)
        elif self.lt_where_search.get_date_text() == '预约日期':
            sql = sql + ''' AND TJ_TJDJB.TJRQ>= '%s' AND TJ_TJDJB.TJRQ< '%s' ''' %(t_start,t_end)

        # 是否有手工单
        if self.cb_manual.isChecked():
            sql = sql + ''' AND TJ_BGGL.SGD='1' '''
        # 是否有胶片
        if self.cb_film.isChecked():
            sql = sql + ''' AND TJ_BGGL.JPSL>1 '''
        # 体检金额
        if self.lb_tjje.get_where_text():
            sql = sql + self.lb_tjje.get_where_text()
        # 单位
        if self.lt_where_search.where_dwbh:
            sql = sql + ''' AND TJ_TJDJB.DWBH = '%s' ''' % self.lt_where_search.where_dwbh
        # 体检类型
        if self.cb_report_type.where_tjlx2:
            sql = sql + self.cb_report_type.where_tjlx2
        # 报告状态
        if self.lt_where_search.where_bgzt:
            sql = sql + self.lt_where_search.where_bgzt
        # 体检区域
        if self.lt_where_search.where_tjqy2:
            sql = sql + self.lt_where_search.where_tjqy2

        sql = sql + ''' INNER JOIN TJ_TJDAB ON TJ_TJDJB.DABH=TJ_TJDAB.DABH ;'''
        # print(sql)
        try:
            results = self.session.execute(sql).fetchall()
            self.table_print.load(results)
            self.gp_middle.setTitle('打印列表（%s）' %self.table_print.rowCount())
            if results:
                self.lb_warn.hide()
            else:
                self.lb_warn.show()
            mes_about(self, '检索出数据%s条' % self.table_print.rowCount())
        except Exception as e:
            mes_about(self,'执行查询%s出错，错误信息：%s' %(sql,e))

    # 下载
    def on_btn_down_click(self):
        qdrq = self.table_print.getCurItemValueOfKey('qdrq')
        bgzt = self.table_print.getCurItemValueOfKey('bgzt')
        if not date_compare(qdrq,'2018-10-01'):
            if bgzt in ['','已审核']:
                mes_about(self,'当前报告还未被审阅，不允许下载！')
                return
        rows = self.table_print.isSelectRows()
        button = mes_warn(self, "您确认下载当前选择的 %s 份体检报告？" %len(rows))
        if button != QMessageBox.Yes:
            return
        if rows:
            for row in rows:
                tjbh = self.table_print.getItemValueOfKey(row,'tjbh')
                xm = self.table_print.getItemValueOfKey(row, 'xm')
                url = gol.get_value('api_report_down') %tjbh
                if self.gp_down_setup.get_save_type():
                    filename = os.path.join(self.gp_down_setup.get_save_path(), '%s.pdf' % tjbh)
                else:
                    filename = os.path.join(self.gp_down_setup.get_save_path(),'%s_%s.pdf' %(tjbh,xm))
                if request_get(url,filename):
                    # 下载成功
                    mes_about(self,'下载成功！')
                else:
                    mes_about(self,'未找到报告，无法下载！')
        else:
            mes_about(self,'请选择要下载的报告！')

    # 领取
    def on_btn_receive_click(self):
        if self.gp_receive_setup.get_receive_type():
            try:
                dialog = ReadChinaIdCard_UI(self)
                dialog.exec_()
            except Exception as e:
                print(e)
        else:
            rows = self.table_print.isSelectRows()
            button = mes_warn(self, "您确认领取当前选择的 %s 份体检报告？" % len(rows))
            if button != QMessageBox.Yes:
                return
            if rows:
                for row in rows:
                    tjbh = self.table_print.getItemValueOfKey(row, 'tjbh')
                    bgzt = self.table_print.getItemValueOfKey(row, 'bgzt')
                    if bgzt=='已领取' and self.gp_receive_setup.get_is_repeat()==False:
                        # 不允许被重复领取
                        pass
                    else:
                        # 更新数据库 TJ_CZJLB TJ_BGGL
                        data_obj = {'jllx': '0037', 'jlmc': '报告领取', 'tjbh': tjbh, 'mxbh': '',
                                    'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area,
                                    'bz': self.gp_receive_setup.get_receive_mode()}
                        try:
                            self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                            self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).update(
                                {
                                    MT_TJ_BGGL.lqrq: cur_datetime(),
                                    MT_TJ_BGGL.lqfs: self.gp_receive_setup.get_receive_mode(),
                                    MT_TJ_BGGL.lqgh: self.login_id,
                                    MT_TJ_BGGL.lqxm: self.login_name,
                                    MT_TJ_BGGL.bgzt: '5',
                                }
                            )
                            self.session.commit()
                        except Exception as e:
                            self.session.rollback()
                            mes_about(self, '更新数据库失败！错误信息：%s' % e)
                            return

                        # 刷新界面
                        self.table_print.setItemValueOfKey(row, 'bgzt', '已领取', QColor("#FF0000"))
                        self.table_print.setItemValueOfKey(row, 'lqxm', self.login_name)
                        self.table_print.setItemValueOfKey(row, 'lqrq', cur_datetime())
                        self.table_print.setItemValueOfKey(row, 'lqfs', self.gp_receive_setup.get_receive_mode())
                        mes_about(self,'报告领取成功！')
            else:
                mes_about(self, '请选择要领取的报告！')

    # 整理
    def on_btn_order_click(self):
        rows = self.table_print.isSelectRows()
        button = mes_warn(self, "您确认整理当前选择的 %s 份体检报告？" %len(rows))
        if button != QMessageBox.Yes:
            return
        if rows:
            for row in rows:
                tjbh = self.table_print.getItemValueOfKey(row, 'tjbh')
                zlxm = self.table_print.getItemValueOfKey(row, 'zlxm')
                dwbh = self.table_print.getItemValueOfKey(row, 'dwbh')
                if not zlxm:
                    result = self.session.query(MT_TJ_DWBH).filter(MT_TJ_DWBH.dwbh == dwbh).scalar()
                    if not result:
                        # 不存在该单位货架号，则插入 插入数据库
                        sql = "INSERT INTO TJ_DWBH(DWBH,ZLHM)VALUES('%s',1)" % dwbh
                        try:
                            self.session.execute(sql)
                            self.session.commit()
                        except Exception as e:
                            self.session.rollback()
                            mes_about(self,'执行SQL：%s 出错，错误信息：%s' %(sql,e))
                            return
                    # 重新获取货架号
                    result = self.session.query(MT_TJ_DWBH).filter(MT_TJ_DWBH.dwbh == dwbh).scalar()
                    # 获取货号
                    new_zlhm = "%s-%s-%s" %(dwbh,result.zlhm // self.gp_order_setup.get_size()+1,result.zlhm % self.gp_order_setup.get_size())

                    # 更新数据库 TJ_CZJLB TJ_DWBH
                    data_obj = {'jllx': '0035', 'jlmc': '报告整理', 'tjbh': tjbh, 'mxbh': '',
                                'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area,
                                'bz': new_zlhm}

                    try:
                        # 自增
                        self.session.query(MT_TJ_DWBH).filter(MT_TJ_DWBH.dwbh == dwbh).update(
                            {MT_TJ_DWBH.zlhm : result.zlhm + 1}
                        )
                        # 更新
                        self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).update(
                            {
                                MT_TJ_BGGL.zlrq: cur_datetime(),
                                MT_TJ_BGGL.zlhm: new_zlhm,
                                MT_TJ_BGGL.zlgh: self.login_id,
                                MT_TJ_BGGL.zlxm: self.login_name,
                                MT_TJ_BGGL.bgzt: '4',
                            }
                        )
                        # 插入
                        self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                        self.session.commit()
                    except Exception as e:
                        self.session.rollback()
                        mes_about(self, '更新数据库失败！错误信息：%s' % e)
                        return

                    # 刷新界面
                    self.table_print.setItemValueOfKey(row,'zlxm', self.login_name)
                    self.table_print.setItemValueOfKey(row,'zlrq', cur_datetime())
                    self.table_print.setItemValueOfKey(row,'zlhh', new_zlhm)
                    self.table_print.setItemValueOfKey(row,'bgzt', '已整理')
                    mes_about(self,'整理成功！')

    # 表格右键功能
    def onTableMenu(self,pos):
        row_num = -1
        indexs=self.table_print.selectionModel().selection().indexes()
        if indexs:
            for i in indexs:
                row_num = i.row()
            menu = QMenu()
            item1 = menu.addAction(Icon("报告中心"), "查看PDF报告")
            # item2 = menu.addAction(Icon("报告中心"), "浏览器中打开HTML报告")
            item3 = menu.addAction(Icon("取消"), "取消整理")
            item4 = menu.addAction(Icon("取消"), "取消领取")
            item5 = menu.addAction(Icon("报告中心"), "重新生成PDF报告")
            item6 = menu.addAction(Icon("报告中心"), "生成江东格式报告")
            action = menu.exec_(self.table_print.mapToGlobal(pos))
            tjbh = self.table_print.getCurItemValueOfKey('tjbh')
            zlxm = self.table_print.getCurItemValueOfKey('zlxm')
            lqxm = self.table_print.getCurItemValueOfKey('lqxm')
            bgzt = self.table_print.getCurItemValueOfKey('bgzt')
            tjzt = self.table_print.getCurItemValueOfKey('tjzt')
            if action==item1:
                self.cur_tjbh = tjbh
                self.on_btn_item_click()
            #
            # elif action == item2:
            #     try:
            #         webbrowser.open(gol.get_value('api_report_preview') % ('html', tjbh))
            #     except Exception as e:
            #         mes_about(self, '打开出错，错误信息：%s' % e)
            #         return
            # 取消整理
            if action == item3:
                if not zlxm:
                    mes_about(self,'还未进行报告整理！')
                else:
                    try:
                        # 更新 TJ_BGGL
                        self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).update(
                            {
                                MT_TJ_BGGL.zlrq: None,
                                MT_TJ_BGGL.zlhm: '',
                                MT_TJ_BGGL.zlgh: '',
                                MT_TJ_BGGL.zlxm: '',
                                MT_TJ_BGGL.bgzt: '3',
                            }
                        )
                        # 更新 TJ_CZJLB
                        self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.tjbh == tjbh,
                                                               MT_TJ_CZJLB.jllx == '0035').update(
                            {
                                MT_TJ_CZJLB.jllx: '0000',
                                MT_TJ_CZJLB.jlnr: '取消整理'
                            }
                        )
                        self.session.commit()
                    except Exception as e:
                        self.session.rollback()
                        mes_about(self,'取消整理失败！错误信息：%s' %e)
                        return
                    # 刷新界面
                    self.table_print.setCurItemValueOfKey('zlxm', '')
                    self.table_print.setCurItemValueOfKey('zlrq', '')
                    self.table_print.setCurItemValueOfKey('zlhh', '')
                    self.table_print.setCurItemValueOfKey('bgzt', '已打印')
            # 取消领取
            elif action == item4:
                if not lqxm:
                    mes_about(self, '还未进行被领取！')
                else:
                    try:
                        # 更新 TJ_BGGL
                        self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).update(
                            {
                                MT_TJ_BGGL.lqrq: None,
                                MT_TJ_BGGL.lqgh: '',
                                MT_TJ_BGGL.lqxm: '',
                                MT_TJ_BGGL.bgzt: '3',
                            }
                        )
                        # 更新 TJ_CZJLB
                        self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.tjbh == tjbh,
                                                               MT_TJ_CZJLB.jllx == '0035').update(
                            {
                                MT_TJ_CZJLB.jllx: '0000',
                                MT_TJ_CZJLB.jlnr: '取消整理'
                            }
                        )
                        self.session.commit()
                    except Exception as e:
                        self.session.rollback()
                        mes_about(self, '取消整理失败！错误信息：%s' % e)
                        return
                    # 刷新界面
                    self.table_print.setCurItemValueOfKey('lqxm', '')
                    self.table_print.setCurItemValueOfKey('lqrq', '')
                    self.table_print.setCurItemValueOfKey('lqfs', '')
                    self.table_print.setCurItemValueOfKey('bgzt', '已打印')
            # 取消领取
            elif action == item5:
                if tjzt=='已审阅':
                    if request_create_report(tjbh, 'pdf'):
                        mes_about(self,"重新生成PDF报告成功！")
                    else:
                        mes_about(self,"重新生成PDF报告失败！")
                else:
                    mes_about(self, '当前报告还未审阅，不能生成！')
                    return
                # filename = r'C:\Users\Administrator\Desktop\pdf测试\168160026.pdf'
                # local_open_pdf(filename)
                # title = "%s - Adobe Reader" %os.path.basename(filename)
                # import win32gui
                # hwnd = win32gui.FindWindow("AcrobatSDIWindow", title)
                # if hwnd==0:
                #     return
                # from widgets.embedWindow import EmbedWindow
                # ui = EmbedWindow(self)
                # ui.click_opened.emit(hwnd)
                # ui.show()

            elif action==item6:
                mes_about(self,'当前功能正在开发中，敬请期待！')


    # 设置快速检索文本
    def on_table_set(self,QTableWidgetItem):
        tjbh = self.table_print.getCurItemValueOfKey('tjbh')
        xm = self.table_print.getCurItemValueOfKey('xm')
        sfzh = self.table_print.getCurItemValueOfKey('sfzh')
        sjhm = self.table_print.getCurItemValueOfKey('sjhm')
        self.gp_quick_search.setText(tjbh,xm,sjhm,sfzh)
        self.cur_tjbh = tjbh
        # 弹窗
        if not self.pop_ui:
            self.pop_ui = ReportPrintPopWidget(self)
        # 是否弹窗
        if self.gp_other_setup.is_show_detail:
            self.pop_ui.show()
            # 传递数据
            title = "体检编号：%s  姓名：%s" %(tjbh,xm)
            self.pop_ui.inited.emit(title,self.cur_tjbh)
        else:
            self.pop_ui.hide()

        if QTableWidgetItem.text()=='查看':
            sql = "SELECT PrintDevice,Modality,count(*) FROM t_film_back_print WHERE PatientID='%s' GROUP BY PrintDevice,Modality ; "  %self.cur_tjbh
            film_session = gol.get_value('film_session')
            if film_session:
                mes = ''
                results = film_session.execute(sql).fetchall()
                if results:
                    for result in results:
                        mes = mes + '''打印位置：%s，胶片类型：%s，打印数量：%s ''' %(result[0],result[1],result[2]) + '\n'
                if mes:
                    mes_about(self,mes)
                else:
                    mes_about(self,'未查询到胶片打印信息！')
            else:
                mes_about(self,'胶片数据库连接失败！请检查配置！')

    #体检系统项目查看
    def on_btn_item_click(self):

        # if not self.item_ui:
        #     self.item_ui = ItemsStateUI(self)
        # self.item_ui.show()
        # if not self.cur_tjbh:
        #     self.cur_tjbh = self.table_print.getCurItemValueOfKey('tjbh')
        # self.item_ui.returnPressed.emit(self.cur_tjbh)
        ##########双击查看 体检进度########
        if not self.cur_tjbh:
            mes_about(self,'请先选择一个人！')
            return
        else:
            xm = self.table_print.getCurItemValueOfKey('xm')
            dwmc = self.table_print.getCurItemValueOfKey('dwmc')
            url_title = "体检编号：%s   姓名：%s   单位名称：%s" %(self.cur_tjbh,xm,dwmc)
            # 优先打开 新系统生成的
            result = self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == self.cur_tjbh).scalar()
            if result:
                if result.bglj:
                    filename = os.path.join(result.bglj, '%s.pdf' % self.cur_tjbh).replace('D:/activefile/', '')
                    url = gol.get_value('api_pdf_new_show') % filename
                    self.open_url(url, url_title)
                    # webbrowser.open(url)
                    return
            # else:
            try:
                self.cxk_session = gol.get_value('cxk_session')
                result = self.cxk_session.query(MT_TJ_PDFRUL).filter(MT_TJ_PDFRUL.TJBH == self.cur_tjbh).scalar()
                if result:
                    url = gol.get_value('api_pdf_old_show') % result.PDFURL
                    self.open_url(url, url_title)
                else:
                    #result = self.session.query(MT_TJ_FILE_ACTIVE).filter(MT_TJ_FILE_ACTIVE.tjbh == self.cur_tjbh).order_by(MT_TJ_FILE_ACTIVE.filemtime.desc()).first()
                    mes_about(self,'历史报告请进行下载功能！')
                    # mes_about(self, '未找到该顾客体检报告！')
            except Exception as e:
                mes_about(self, '查询出错，错误信息：%s' % e)
                return

    # 在窗口中打开报告，取消在浏览器中打开，主要用于外部查询中使用，避免地址外泄
    def open_url(self, url, title):
        if not self.browser:
            self.browser = QBrowser(self)
        self.browser.open_url.emit(title, url)
        self.browser.show()

class PdfDialog(QDialog):

    urlChange = pyqtSignal(str)

    def __init__(self,parent=None):
        super(PdfDialog,self).__init__(parent)
        self.setWindowTitle('明州体检')
        self.initUI()
        # 绑定信号槽
        self.urlChange.connect(self.on_web_url_change)

    def initUI(self):
        lt_main = QHBoxLayout()
        self.wv_pdf = WebView()
        lt_main.addWidget(self.wv_pdf)
        self.setLayout(lt_main)

    def on_web_url_change(self,url:str):
        self.wv_pdf.load(url)
        self.wv_pdf.show()

# 没有窗口外围
class PdfWebView(WebView):

    urlChange = pyqtSignal(str)

    def __init__(self,parent=None):
        super(WebView,self).__init__(parent)
        self.setWindowTitle('明州体检')
        # 绑定信号槽
        self.urlChange.connect(self.on_web_url_change)
        # 移动位置
        desktop = QDesktopWidget()
        self.setFixedHeight(900)
        self.setFixedWidth(500)
        self.move((desktop.availableGeometry().width()-self.width()-20),0)
                  #desktop.availableGeometry().height()-60)  # 初始化位置到右下角
        self.show()

    # URL 刷新
    def on_web_url_change(self,url:str):
        self.load(url)

def local_open_pdf(filename):
    import subprocess
    cmd = os.getenv("comspec")
    acrobat = "acrord32.exe"
    cmds = [cmd, "/c", "start", acrobat, "/s", filename]
    subprocess.Popen(cmds)

def get_bgzt(s_bgzt,t_bgzt):
    bgzt = {
        '已追踪': 0,
        '已审核': 1,
        '已审阅': 2,
        '已打印': 3,
        '已整理': 4,
        '已领取': 5
    }
    if bgzt.get(s_bgzt,0)>=bgzt.get(t_bgzt,0):
        return s_bgzt,str(bgzt.get(s_bgzt,0))
    else:
        return t_bgzt,str(bgzt.get(t_bgzt,0))

# 运行打印线程
class PrintThread(QThread):

    # 定义信号,定义参数为str类型
    signalMes = pyqtSignal(bool,list,int)        #成功/失败，任务结果 最后一个参数，用于防止静态方法mes_about 重复弹出的问题
    signalExit = pyqtSignal()                # 退出线程

    def __init__(self,session):
        super(PrintThread,self).__init__()
        self.runing = False
        self.session = session               # 数据库会话
        self.num = 1

    def stop(self):
        self.runing = False

    # 启动任务
    def setTask(self,sql:str):
        self.sql =sql
        self.runing = True

    def run(self):
        while self.runing:
            try:
                results = self.session.execute(self.sql).fetchall()
                self.signalMes.emit(True, results,self.num)
            except Exception as e:
                self.signalMes.emit(False, [e],self.num)
            self.num = self.num + 1
            self.stop()

# # 通用进度对话框，需要实现启动和停止，及数据初始化
# class ProcessDialog(Dialog):
#
#     started = pyqtSignal(list)
#
#     def __init__(self,parent=None):
#         super(ProcessDialog,self).__init__(parent)
#         self.setWindowTitle('明州体检')
#         self.initUI()
#         # 绑定信号
#         self.started.connect(self.initDatas)
#         self.btn_start.clicked.connect(self.on_btn_start_click)
#         self.btn_stop.clicked.connect(self.on_btn_stop_click)
#         # 特殊变量
#         self.datas = None
#         self.task_type = None
#         self.thread = CustomThread()
#
#     def initUI(self):
#         lt_main = QVBoxLayout()
#         ###########################################################
#         lt_top = QHBoxLayout()
#         gp_top = QGroupBox('进度总览')
#         # 待接收的总数
#         self.lb_all = ProcessLable()
#         # 已完成接收数
#         self.lb_is_done = ProcessLable()
#         # 未完成总数
#         self.lb_no_done = ProcessLable()
#         # 错误数
#         self.lb_error = ProcessLable()
#         # 添加布局
#         lt_top.addWidget(QLabel('总数：'))
#         lt_top.addWidget(self.lb_all)
#         lt_top.addWidget(QLabel('完成数：'))
#         lt_top.addWidget(self.lb_is_done)
#         lt_top.addWidget(QLabel('未完成数：'))
#         lt_top.addWidget(self.lb_no_done)
#         lt_top.addWidget(QLabel('错误数：'))
#         lt_top.addWidget(self.lb_error)
#         gp_top.setLayout(lt_top)
#         ###########################################################
#         lt_middle = QHBoxLayout()
#         gp_middle = QGroupBox('处理详情')
#         ###########################################################
#         lt_bottom = QHBoxLayout()
#         gp_bottom = QGroupBox('进度')
#         self.pb_progress=QProgressBar()
#         self.pb_progress.setMinimum(0)
#         self.pb_progress.setValue(0)
#         lt_bottom.addWidget(self.pb_progress)
#         gp_bottom.setLayout(lt_bottom)
#         #########增加按钮组########################################
#         lt_1 = QHBoxLayout()
#         self.lb_timer = TimerLabel2()
#         self.btn_start = QPushButton(Icon("启动"),"启动")
#         self.btn_stop = QPushButton(Icon("停止"),"停止")
#         lt_1.addWidget(self.lb_timer)
#         lt_1.addStretch()
#         lt_1.addWidget(self.btn_start)
#         lt_1.addWidget(self.btn_stop)
#         # 布局
#         lt_main.addWidget(gp_top)
#         lt_main.addWidget(gp_middle)
#         lt_main.addWidget(gp_bottom)
#         lt_main.addLayout(lt_1)
#         self.setLayout(lt_main)
#
#     def on_progress_change(self,is_done,no_done,error):
#         self.sb_is_done.setText(str(is_done))
#         self.sb_no_done.setText(str(no_done))
#         self.sb_error.setText(str(error))
#         self.pb_progress.setValue(is_done)
#         dProgress = (self.pb_progress.value() - self.pb_progress.minimum()) * 100.0 / (self.pb_progress.maximum() - self.pb_progress.minimum())
#         #self.progress.setFormat("当前进度为：%s%" %dProgress)
#         self.pb_progress.setAlignment(Qt.AlignRight | Qt.AlignVCenter) #对齐方式
#
#     # 启动
#     def on_btn_start_click(self):
#         # 刷新界面控件
#         self.btn_start.setDisabled(True)
#         self.btn_stop.setDisabled(False)
#         self.lb_timer.start()
#         self.sb_all.setText(str(len(self.datas)))
#         self.pb_progress.setMaximum(len(self.datas))
#         self.thread.setTakType(self.task_type)
#         self.thread.setTask(self.datas)
#         self.thread.signalCur.connect(self.on_mes_show, type=Qt.QueuedConnection)
#         self.thread.signalDone.connect(self.on_progress_change, type=Qt.QueuedConnection)
#         self.thread.signalExit.connect(self.on_thread_exit, type=Qt.QueuedConnection)
#         self.thread.start()
#
#     # 停止接收数据
#     def on_btn_stop_click(self):
#         # 刷新界面控件
#         self.btn_start.setDisabled(False)
#         self.btn_stop.setDisabled(True)
#         self.lb_timer.stop()
#
#     # 初始化数据
#     def initDatas(self,datas:list,task_type=1):
#         self.datas = datas
#         self.task_type = task_type
#         self.on_btn_start_click()
#
#     # 消息展示
#     def on_mes_show(self,tjbh:str,mes:str):
#         pass
#
#     def on_thread_exit(self,status:bool,error:str):
#         self.on_btn_stop_click()
#         mes_about(self,error)
#
#     def closeEvent(self, QCloseEvent):
#         try:
#             if self.thread:
#                 # button = mes_warn(self,"项目结果接收正在运行中，您是否确定立刻退出？")
#                 # if button == QMessageBox.Yes:
#                 self.thread.stop()
#                 self.thread = None
#         except Exception as e:
#             print(e)
#         super(ProcessDialog, self).closeEvent(QCloseEvent)

# 运行线程处理耗时任务：打印、下载、领取、整理
# class CustomThread(QThread):
#
#     # 定义信号,定义参数为str类型
#     signalCur = pyqtSignal(str,str)     # 处理过程：成功/失败，错误消息，
#     signalDone = pyqtSignal(int, int, int)   # 处理完成：成功/失败，错误消息，
#     signalExit = pyqtSignal(bool,str)   # 处理结束：成功/失败，是否异常退出
#
#     def __init__(self):
#         super(CustomThread,self).__init__()
#         self.runing = False
#         self.initParas()
#         # 特殊变量
#         self.num_all = 0            # 总数
#         self.num_is_done = 0        # 已完成
#         self.num_no_done = 0        # 未完成
#         self.num_error = 0          # 错误
#
#     # 完成参数初始化
#     def setParas(self,session):
#         self.session = session
#         self.num = 1
#
#     def stop(self):
#         self.runing = False
#
#     # 启动任务
#     def setTask(self,tjbhs:list):
#         self.tjbhs =tjbhs
#         self.num_all = len(tjbhs)
#         self.runing = True
#
#     def setTakType(self,taktype = 1):
#         self.taktype = taktype
#
#     def print_obj(self,tjbh):
#         pass
#
#     def run(self):
#         while self.runing:
#             for tjbh in self.tjbhs:
#                 if self.runing:
#                     if api_print(tjbh,printers[printer]):
#                         if len(rows) == 1:
#                             mes_about(self, "打印成功！")
#                     else:
#                         mes_about(self, "打印失败！")
#                 self.num_done = self.num_done + 1
#                 self.num_undone = self.num_all - self.num_done
#                 self.signalDone.emit(self.num_done,self.num_undone,self.num_error)
#             self.signalExit.emit(True, "处理完成！")
#             self.stop()




# 报告打印弹出框
class ReportPrintPopWidget(Dialog):

    inited = pyqtSignal(str,str)    # 人员信息、体检编号

    def __init__(self,parent=None):
        super(ReportPrintPopWidget, self).__init__(parent)
        self.initUI()
        self.inited.connect(self.on_search)
        self.states = {'0':'追踪中','1':'已审核','2':'已审阅','3':'已打印','4':'已整理','5':'已领取'}

    def initUI(self):
        lt_main = QVBoxLayout()
        ###################### 手工单 ###################################
        self.gp_top = QGroupBox('手工单(0)')
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
        self.lb_count_rx = FilmLable()
        lt_middle.addWidget(QLabel('DR：'))
        lt_middle.addWidget(self.lb_count_dr)
        lt_middle.addSpacing(10)
        lt_middle.addWidget(QLabel('CT：'))
        lt_middle.addWidget(self.lb_count_ct)
        lt_middle.addSpacing(10)
        lt_middle.addWidget(QLabel('MRI：'))
        lt_middle.addWidget(self.lb_count_mri)
        lt_middle.addSpacing(10)
        lt_middle.addWidget(QLabel('钼靶：'))
        lt_middle.addWidget(self.lb_count_rx)

        lt_middle.addStretch()
        self.gp_middle.setLayout(lt_middle)
        ######################报告信息###################################
        gp_bottom = QGroupBox('报告信息')
        lt_bottom = QFormLayout()
        lt_bottom.setLabelAlignment(Qt.AlignRight)
        lt_bottom.setFormAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        self.lb_bgzz = FilmLable()
        self.lb_bgzj = FilmLable()
        self.lb_bgsh = FilmLable()
        self.lb_bgsy = FilmLable()
        self.lb_bgdy = FilmLable()
        self.lb_bgzl = FilmLable()
        self.lb_bglq = FilmLable()
        lt_bottom.addRow(QLabel("追踪："), self.lb_bgzz)
        lt_bottom.addRow(QLabel("总检："), self.lb_bgzj)
        lt_bottom.addRow(QLabel("审核："), self.lb_bgsh)
        lt_bottom.addRow(QLabel("审阅："), self.lb_bgsy)
        lt_bottom.addRow(QLabel("打印："), self.lb_bgdy)
        lt_bottom.addRow(QLabel("整理："), self.lb_bgzl)
        lt_bottom.addRow(QLabel("领取："), self.lb_bglq)
        lt_bottom.setHorizontalSpacing(10)
        gp_bottom.setLayout(lt_bottom)
        #################报告状态###########################
        lt_state = QHBoxLayout()
        self.lb_state = ReportStateLable()
        self.lb_state.show()
        lt_state.addWidget(self.lb_state)
        lt_1= QVBoxLayout()
        # 添加布局
        lt_1.addWidget(self.gp_top)
        lt_1.addWidget(self.gp_middle)
        lt_2 = QHBoxLayout()
        lt_2.addLayout(lt_1)
        lt_2.addLayout(lt_state)
        # lt_2.addStretch()
        lt_main.addLayout(lt_2)
        lt_main.addWidget(gp_bottom)
        # lt_main.addWidget(self.gp_bottom2)
        lt_main.addStretch()
        self.setLayout(lt_main)

        self.setWindowIcon(Icon('mztj'))
        # 移动整体位置
        desktop = QDesktopWidget()
        self.setFixedHeight(400)
        self.setFixedWidth(400)
        self.move((desktop.availableGeometry().width()-self.width()-20),
                  desktop.availableGeometry().height()-self.height()-50)  # 初始化位置到右下角

    # 传递体检编号
    def on_search(self,ryxx,tjbh):
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
            if result[0] in list(film.keys()):
                film[result[0]] = film[result[0]] + result[1]
            else:
                film[result[0]] = result[1]
        # 更新
        self.init_film(film)
        # 获取报告状态
        result = self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh==tjbh).scalar()
        if result:
            self.lb_bgzz.setText("%s，%s" % (str2(result.zzxm), str2(result.zzrq)))
            self.lb_bgzj.setText("%s，%s" % (str2(result.zjxm), str2(result.zjrq)))
            self.lb_bgsh.setText("%s，%s" % (str2(result.shxm), str2(result.shrq)))
            self.lb_bgsy.setText("%s，%s" % (str2(result.syxm), str2(result.syrq)))
            self.lb_bgdy.setText("%s，%s" % (str2(result.dyxm), str2(result.dyrq)))
            self.lb_bgzl.setText("%s，%s" % (str2(result.zlxm), str2(result.zlrq)))
            self.lb_bglq.setText("%s，%s" % (str2(result.lqxm), str2(result.lqrq)))
            self.lb_state.show2(self.states.get(result.bgzt,''),True)


    # 初始化胶片信息
    def init_film(self,film:dict):
        self.lb_count_dr.setText(str(film.get('DR','')))
        self.lb_count_ct.setText(str(film.get('CT', '')))
        self.lb_count_mri.setText(str(film.get('MRI', '')))
        self.lb_count_rx.setText(str(film.get('RX', '')))
        self.gp_middle.setTitle('胶片数量(%s)' %str(film.get('DR',0)+film.get('CT',0)+film.get('MRI',0)+film.get('RX',0)))


class FilmLable(QLabel):

    def __init__(self):
        super(FilmLable,self).__init__()
        # self.setMinimumWidth(50)
        self.setStyleSheet('''font: 75 14pt \"微软雅黑\";color: rgb(0, 85, 255);''')

def date_compare(date1:str,date2:str):
    s_time = time.mktime(time.strptime(date1,'%Y-%m-%d'))
    t_time = time.mktime(time.strptime(date2,'%Y-%m-%d'))
    return int(s_time) - int(t_time)