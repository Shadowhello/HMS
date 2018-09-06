from .report_print_ui import *
from .model import *
from utils import request_get,print_pdf,cur_datetime
from widgets.bweb import WebView
import webbrowser

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
        self.table_print.itemDoubleClicked.connect(self.on_btn_item_click)
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

    # 打印
    def on_btn_print_click(self):
        rows = self.table_print.isSelectRows()
        if rows:
            for row in rows:
                tjbh = self.table_print.getItemValueOfKey(row,'tjbh')
                url = gol.get_value('api_report_down') %tjbh
                filename = os.path.join(gol.get_value('path_tmp'),'%s.pdf' %tjbh)
                if request_get(url,filename):
                    # 下载成功
                    print_pdf(filename)
                else:
                    mes_about(self,'未找到报告，无法打印！')
        else:
            mes_about(self,'请选择要打印的报告！')

    # 查询
    def on_btn_query_click(self):
        sql = get_report_print2_sql()
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
            mes_about(self, '检索出数据%s条' % self.table_print.rowCount())
        except Exception as e:
            mes_about(self,'执行查询%s出错，错误信息：%s' %(sql,e))

    # 下载
    def on_btn_down_click(self):
        rows = self.table_print.isSelectRows()
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
        if rows:
            for row in rows:
                tjbh = self.table_print.getItemValueOfKey(row, 'tjbh')
                zlxm = self.table_print.getItemValueOfKey(row, 'zlxm')
                dwbh = self.table_print.getItemValueOfKey(row, 'dwbh')
                if not zlxm:
                    result = self.session.query(MT_TJ_DWBH).filter(MT_TJ_DWBH.dwbh == dwbh).scalar()
                    if result:
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
                    else:
                        # 插入数据库
                        sql = "INSERT INTO TJ_DWBH(DWBH,ZLHM)VALUES('%s',0)" % dwbh
                        try:
                            self.session.execute(sql)
                            self.session.commit()
                        except Exception as e:
                            self.session.rollback()
                            mes_about(self,'执行SQL：%s 出错，错误信息：%s' %(sql,e))
                            return

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
            action = menu.exec_(self.table_print.mapToGlobal(pos))
            tjbh = self.table_print.getCurItemValueOfKey('tjbh')
            zlxm = self.table_print.getCurItemValueOfKey('zlxm')
            lqxm = self.table_print.getCurItemValueOfKey('lqxm')
            if action==item1:
                try:
                    self.cxk_session = gol.get_value('cxk_session')
                    result = self.cxk_session.query(MT_TJ_PDFRUL).filter(MT_TJ_PDFRUL.TJBH == tjbh).scalar()
                    if result:
                        url = gol.get_value('api_pdf_old_show') % result.PDFURL
                        webbrowser.open(url)
                    else:
                        mes_about(self, '未找到该顾客体检报告！')
                except Exception as e:
                    mes_about(self, '查询出错，错误信息：%s' % e)
                    return
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