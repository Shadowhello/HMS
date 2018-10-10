from .report_print_ui import *
from .model import *
from utils import request_get,print_pdf_gsprint,cur_datetime,api_print,request_create_report
from widgets.bweb import WebView
import webbrowser
from .common import get_pdf_url

printers = {
    '77号打印机':'77',
    '78号打印机':'78',
    '79号打印机':'79',
    '江东打印机':'jd'
}

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
        # 右键、双击、单击
        self.table_print.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.table_print.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单
        self.table_print.itemClicked.connect(self.on_table_set)
        # self.table_print.itemDoubleClicked.connect(self.on_btn_item_click)
        # 快速减速
        self.gp_quick_search.returnPressed.connect(self.on_quick_search)    # 快速检索
        # 特殊变量
        self.cur_tjbh = None
        self.web_pdf_ui = None

    # 初始化部分参数
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
        sql = get_report_print2_sql()
        sql = sql + ''' INNER JOIN TJ_TJDAB ON TJ_TJDJB.DABH=TJ_TJDAB.DABH '''
        sql = sql +''' AND ''' + where_str
        results = self.session.execute(sql).fetchall()
        self.table_print.load(results)
        self.gp_middle.setTitle('打印列表（%s）' %self.table_print.rowCount())
        mes_about(self,'共检索出 %s 条数据！' %self.table_print.rowCount())

    # 打印
    def on_btn_print_click(self):
        rows = self.table_print.isSelectRows()
        is_remote,printer = self.gp_print_setup.get_printer()
        button = mes_warn(self, "您确认用打印机：%s，打印当前选择的 %s 份体检报告？" %(printer,len(rows)))
        if button != QMessageBox.Yes:
            return
        if rows:
            for row in rows:
                tjbh = self.table_print.getItemValueOfKey(row, 'tjbh')
                dyrq = self.table_print.getItemValueOfKey(row, 'dyrq')
                dyr = self.table_print.getItemValueOfKey(row, 'dyr')
                dycs = self.table_print.getItemValueOfKey(row, 'dycs')
                bgzt = self.table_print.getItemValueOfKey(row, 'bgzt')
                bgzt_name,bgzt_value = get_bgzt(bgzt,'已打印')
                if is_remote:
                    # 发送网络打印请求
                    try:
                        # 更新数据库 TJ_CZJLB TJ_BGGL
                        data_obj = {'jllx': '0034', 'jlmc': '报告打印', 'tjbh': tjbh, 'mxbh': '',
                                    'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area,
                                    'bz': '网络打印：%s' %printer}
                        self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                        self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).update(
                            {
                                MT_TJ_BGGL.dyrq: cur_datetime(),
                                MT_TJ_BGGL.dyfs: '1',
                                MT_TJ_BGGL.dygh: self.login_id,
                                MT_TJ_BGGL.dyxm: self.login_name,
                                MT_TJ_BGGL.dycs: MT_TJ_BGGL.dycs + 1,
                                MT_TJ_BGGL.bgzt: bgzt_value
                            }
                        )
                        self.session.commit()
                    except Exception as e:
                        self.session.rollback()
                        mes_about(self, '更新数据库失败！错误信息：%s' % e)
                        return
                    # 刷新界面
                    self.table_print.setItemValueOfKey(row, 'dyrq', cur_datetime())
                    self.table_print.setItemValueOfKey(row, 'dyr', self.login_name)
                    self.table_print.setItemValueOfKey(row, 'dycs', '1')
                    self.table_print.setItemValueOfKey(row, 'dyfs', '租赁打印')
                    self.table_print.setItemValueOfKey(row, 'bgzt', bgzt_name)
                    if api_print(tjbh,printers[printer]):
                        if len(rows) == 1:
                            mes_about(self, "打印成功！")
                    else:
                        mes_about(self, "打印失败！")
                else:
                    # 本地打印 需要下载
                    url = gol.get_value('api_report_down') %tjbh
                    filename = os.path.join(gol.get_value('path_tmp'),'%s.pdf' %tjbh)
                    if request_get(url,filename):
                        # 下载成功
                        if print_pdf_gsprint(filename) == 0:
                            try:
                                # 更新数据库 TJ_CZJLB TJ_BGGL
                                data_obj = {'jllx': '0034', 'jlmc': '报告打印', 'tjbh': tjbh, 'mxbh': '',
                                            'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area,
                                            'bz': '本地打印：%s' %printer}
                                self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                                self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).update(
                                    {
                                        MT_TJ_BGGL.dyrq: cur_datetime(),
                                        MT_TJ_BGGL.dyfs: '1',
                                        MT_TJ_BGGL.dygh: self.login_id,
                                        MT_TJ_BGGL.dyxm: self.login_name,
                                        MT_TJ_BGGL.dycs: MT_TJ_BGGL.dycs + 1,
                                        MT_TJ_BGGL.bgzt: bgzt_value
                                    }
                                )
                                self.session.commit()
                            except Exception as e:
                                self.session.rollback()
                                mes_about(self, '更新数据库失败！错误信息：%s' % e)
                                return
                            # 刷新界面
                            self.table_print.setItemValueOfKey(row, 'dyrq',cur_datetime())
                            self.table_print.setItemValueOfKey(row, 'dyr', self.login_name)
                            self.table_print.setItemValueOfKey(row, 'dycs', '1')
                            self.table_print.setItemValueOfKey(row, 'dyfs', '本地打印')
                            self.table_print.setItemValueOfKey(row, 'bgzt', bgzt_name)
                            if len(rows) == 1:
                                mes_about(self, "打印成功！")
                        else:
                            mes_about(self, "打印失败！")
                    else:
                        mes_about(self,'未找到报告，无法打印！')
            if len(rows) > 1:
                mes_about(self, "打印成功！")
        else:
            mes_about(self,'请选择要打印的报告！')

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
        print(sql)
        try:
            results = self.session.execute(sql).fetchall()
            self.table_print.load(results)
            self.gp_middle.setTitle('打印列表（%s）' %self.table_print.rowCount())
            mes_about(self, '检索出数据%s条' % self.table_print.rowCount())
        except Exception as e:
            mes_about(self,'执行查询%s出错，错误信息：%s' %(sql,e))

    # 下载
    def on_btn_down_click(self):
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
            item1 = menu.addAction(Icon("报告中心"), "浏览器中打开PDF报告")
            item2 = menu.addAction(Icon("报告中心"), "浏览器中打开HTML报告")
            item3 = menu.addAction(Icon("取消"), "取消整理")
            item4 = menu.addAction(Icon("取消"), "取消领取")
            item5 = menu.addAction(Icon("报告中心"), "重新生成PDF报告")
            action = menu.exec_(self.table_print.mapToGlobal(pos))
            tjbh = self.table_print.getCurItemValueOfKey('tjbh')
            zlxm = self.table_print.getCurItemValueOfKey('zlxm')
            lqxm = self.table_print.getCurItemValueOfKey('lqxm')
            bgzt = self.table_print.getCurItemValueOfKey('bgzt')
            tjzt = self.table_print.getCurItemValueOfKey('tjzt')
            if action==item1:
                url = get_pdf_url(self.session,tjbh)
                if url:
                    webbrowser.open(url)
                else:
                    mes_about(self, '未查询到该报告！')

            elif action == item2:
                try:
                    webbrowser.open(gol.get_value('api_report_preview') % ('html', tjbh))
                except Exception as e:
                    mes_about(self, '打开出错，错误信息：%s' % e)
                    return
            # 取消整理
            elif action == item3:
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


    # 设置快速检索文本
    def on_table_set(self,QTableWidgetItem):
        tjbh = self.table_print.getCurItemValueOfKey('tjbh')
        xm = self.table_print.getCurItemValueOfKey('xm')
        sfzh = self.table_print.getCurItemValueOfKey('sfzh')
        sjhm = self.table_print.getCurItemValueOfKey('sjhm')
        self.gp_quick_search.setText(tjbh,xm,sjhm,sfzh)
        self.cur_tjbh = tjbh
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
        if not self.cur_tjbh:
            mes_about(self,'请先选择一个人！')
            return
        else:
            try:
                self.cxk_session = gol.get_value('cxk_session')
                result = self.cxk_session.query(MT_TJ_PDFRUL).filter(MT_TJ_PDFRUL.TJBH == self.cur_tjbh).scalar()
                if result:
                    url = gol.get_value('api_pdf_old_show') %result.PDFURL
                else:
                    url = None
            except Exception as e:
                mes_about(self,'查询出错，错误信息：%s' %e)
                return
            if not url:
                mes_about(self,'未找到该顾客体检报告！')
                return
            if not self.web_pdf_ui:
                self.web_pdf_ui = PdfDialog(self)
            self.web_pdf_ui.urlChange.emit(url)
            self.web_pdf_ui.show()

    # def setSaveFileName(self):
    #     filepath = QFileDialog.getExistingDirectory(self, "保存路径",
    #                                               desktop(),
    #                                                QFileDialog.ShowDirsOnly|QFileDialog.DontResolveSymlinks)
    #     return filepath

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

# 进度对话框，需要实现启动和停止，及数据初始化
class ProcessDialog(Dialog):

    started = pyqtSignal(list)

    def __init__(self,parent=None):
        super(ProcessDialog,self).__init__(parent)
        self.setWindowTitle('明州体检')
        self.initUI()
        # 绑定信号
        self.started.connect(self.initDatas)
        self.btn_start.clicked.connect(self.on_btn_start_click)
        self.btn_stop.clicked.connect(self.on_btn_stop_click)
        # 特殊变量
        self.datas = None
        self.task_type = None
        self.thread = CustomThread()

    def initUI(self):
        lt_main = QVBoxLayout()
        ###########################################################
        lt_top = QHBoxLayout()
        gp_top = QGroupBox('进度总览')
        # 待接收的总数
        self.lb_all = ProcessLable()
        # 已完成接收数
        self.lb_is_done = ProcessLable()
        # 未完成总数
        self.lb_no_done = ProcessLable()
        # 错误数
        self.lb_error = ProcessLable()
        # 添加布局
        lt_top.addWidget(QLabel('总数：'))
        lt_top.addWidget(self.lb_all)
        lt_top.addWidget(QLabel('完成数：'))
        lt_top.addWidget(self.lb_is_done)
        lt_top.addWidget(QLabel('未完成数：'))
        lt_top.addWidget(self.lb_no_done)
        lt_top.addWidget(QLabel('错误数：'))
        lt_top.addWidget(self.lb_error)
        gp_top.setLayout(lt_top)
        ###########################################################
        lt_middle = QHBoxLayout()
        gp_middle = QGroupBox('处理详情')
        ###########################################################
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox('进度')
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
        self.thread.setTakType(self.task_type)
        self.thread.setTask(self.datas)
        self.thread.signalCur.connect(self.on_mes_show, type=Qt.QueuedConnection)
        self.thread.signalDone.connect(self.on_progress_change, type=Qt.QueuedConnection)
        self.thread.signalExit.connect(self.on_thread_exit, type=Qt.QueuedConnection)
        self.thread.start()

    # 停止接收数据
    def on_btn_stop_click(self):
        # 刷新界面控件
        self.btn_start.setDisabled(False)
        self.btn_stop.setDisabled(True)
        self.lb_timer.stop()

    # 初始化数据
    def initDatas(self,datas:list,task_type=1):
        self.datas = datas
        self.task_type = task_type
        self.on_btn_start_click()

    # 消息展示
    def on_mes_show(self,tjbh:str,mes:str):
        pass

    def on_thread_exit(self,status:bool,error:str):
        self.on_btn_stop_click()
        mes_about(self,error)

    def closeEvent(self, QCloseEvent):
        try:
            if self.thread:
                # button = mes_warn(self,"项目结果接收正在运行中，您是否确定立刻退出？")
                # if button == QMessageBox.Yes:
                self.thread.stop()
                self.thread = None
        except Exception as e:
            print(e)
        super(ProcessDialog, self).closeEvent(QCloseEvent)

# 运行线程处理耗时任务：打印、下载、领取、整理
class CustomThread(QThread):

    # 定义信号,定义参数为str类型
    signalCur = pyqtSignal(str,str)     # 处理过程：成功/失败，错误消息，
    signalDone = pyqtSignal(int, int, int)   # 处理完成：成功/失败，错误消息，
    signalExit = pyqtSignal(bool,str)   # 处理结束：成功/失败，是否异常退出

    def __init__(self):
        super(CustomThread,self).__init__()
        self.runing = False
        self.initParas()
        # 特殊变量
        self.num_all = 0            # 总数
        self.num_is_done = 0        # 已完成
        self.num_no_done = 0        # 未完成
        self.num_error = 0          # 错误

    # 完成参数初始化
    def setParas(self,session):
        self.session = session
        self.num = 1

    def stop(self):
        self.runing = False

    # 启动任务
    def setTask(self,tjbhs:list):
        self.tjbhs =tjbhs
        self.num_all = len(tjbhs)
        self.runing = True

    def setTakType(self,taktype = 1):
        self.taktype = taktype

    def print_obj(self,tjbh):
        pass

    def run(self):
        while self.runing:
            for tjbh in self.tjbhs:
                if self.runing:
                    pass
                self.num_done = self.num_done + 1
                self.num_undone = self.num_all - self.num_done
                self.signalDone.emit(self.num_done,self.num_undone,self.num_error)
            self.signalExit.emit(True, "处理完成！")
            self.stop()

class ProcessLable(QLabel):

    def __init__(self):
        super(ProcessLable,self).__init__()
        self.setMinimumWidth(50)
        self.setStyleSheet('''font: 75 14pt \"微软雅黑\";color: rgb(0, 85, 255);''')