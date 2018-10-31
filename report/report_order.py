from .report_order_ui import ReportOrderUI
from widgets.cwidget import *
from utils.readparas import GolParasMixin
from .model import *
from collections import OrderedDict
from widgets import QBrowser
from .common import *

# 报告整理
class ReportOrder(GolParasMixin,ReportOrderUI):

    def __init__(self):
        super(ReportOrder, self).__init__()
        self.init()
        self.initParas()
        # 绑定信号槽
        self.le_tjbh.returnPressed.connect(self.on_le_tjbh_search)
        self.btn_query.clicked.connect(self.on_btn_query_click)
        self.btn_export.clicked.connect(self.on_btn_export_click)
        self.table_report_progress.itemClicked.connect(self.on_table_detail)
        # 功能区按钮绑定
        self.btn_order.clicked.connect(self.on_btn_order_click)
        self.btn_view.clicked.connect(self.on_btn_view_click)
        self.btn_print.clicked.connect(self.on_btn_print_click)
        self.btn_review.clicked.connect(self.on_btn_review_click)
        # 特殊变量
        self.cur_bgzt = None    # 当前报告状态，快速识别是否可以使用功能区按钮
        self.browser = None

    # 初始化部分参数
    def initParas(self):
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()
        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)
        self.report_dwmc.setBhs(self.dwmc_bh)
        self.report_dwmc.setPys(self.dwmc_py)

    def on_le_tjbh_search(self):
        tjbh = self.le_tjbh.text()
        if not tjbh:
            mes_about(self,'请输入体检编号！')
            return
        # 更新人员信息
        result = self.session.query(MV_RYXX).filter(MV_RYXX.tjbh == tjbh).scalar()
        if result:
            self.set_user_data(result.to_dict)
        else:
            self.clear_user_data()
            mes_about(self,'不存在，请确认后重新输入！')
            return
        # 报告状态
        result = self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).scalar()
        if result:
            self.lb_bgsy.setText('%s；%s' % (str2(result.syxm), result.syrq if result.syrq else ''))
            self.lb_bgdy.setText('%s；%s' % (str2(result.dyxm), result.dyrq if result.dyrq else ''))

        # 更新胶片信息
        film = {}
        results = self.session.execute(get_film_num(tjbh))
        for result in results:
            if result[0] in list(film.keys()):
                film[result[0]] = film[result[0]] + result[1]
            else:
                film[result[0]] = result[1]
        # 更新
        self.init_film(film)
        # 手工报告单 # xmbh in ['1122', '1931', '0903', '501732', '501933', '501934']:
        results = self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,
                                                           MT_TJ_TJJLMXB.sfzh == '1',
                                                           MT_TJ_TJJLMXB.zhbh.in_(['1122', '1931', '0903', '501732', '501933', '501934'])).all()
        self.lb_manual.setText("  ".join([str2(result.xmmc) for result in results]))
        self.gp_middle_bottom2.setTitle('手工单报告(%s)' %str(len(results)))
        # 清空
        self.le_tjbh.setText('')

    def set_user_data(self,user_data:dict):
        self.clear_user_data()
        self.lb_user_id.setText(user_data.get('tjbh',''))
        self.lb_user_name.setText(user_data.get('xm',''))
        self.lb_user_sex.setText(user_data.get('xb',''))
        self.lb_user_age.setText(user_data.get('nl',''))
        self.lb_user_sjhm.setText(user_data.get('sjhm',''))
        self.lb_user_sfzh.setText(user_data.get('sfzh',''))
        if user_data.get('depart',''):
            self.lb_user_dwmc.setText("%s(%s)" %(user_data.get('dwmc',''),user_data.get('depart','')))
        else:
            self.lb_user_dwmc.setText(user_data.get('dwmc', ''))
        #
        self.report_dwmc.setText(user_data.get('dwmc', ''))

    def clear_user_data(self):
        self.lb_user_id.setText('')
        self.lb_user_name.setText('')
        self.lb_user_sex.setText('')
        self.lb_user_age.setText('')
        self.lb_user_sjhm.setText('')
        self.lb_user_sfzh.setText('')
        self.lb_user_dwmc.setText('')

    # 初始化胶片信息
    def init_film(self,film:dict):
        self.lb_count_dr.setText(str(film.get('DR','')))
        self.lb_count_ct.setText(str(film.get('CT', '')))
        self.lb_count_mri.setText(str(film.get('MRI', '')))
        self.lb_count_rx.setText(str(film.get('RX', '')))
        self.gp_middle_bottom.setTitle('胶片数量(%s)' %str(film.get('DR',0)+film.get('CT',0)+film.get('MRI',0)+film.get('RX',0)))

    def on_table_detail(self,QTableWidgetItem):
        col = QTableWidgetItem.column()
        tjzt = list(self.table_report_progress_cols.keys())[col]
        if tjzt=='sum':
            sql = get_report_progress_sql2(self.report_dwmc.where_dwbh)
        else:
            sql = get_report_progress_sql(self.report_dwmc.where_dwbh, tjzt)
        results = self.session.execute(sql).fetchall()
        self.table_report_detail.load(results)
        col_name = list(self.table_report_progress_cols.values())[col]
        self.gp_right_bottom.setTitle('%s（%s）' %(col_name,self.table_report_detail.rowCount()))
        mes_about(self, '检索出 %s 条数据！' %self.table_report_detail.rowCount())


    def on_btn_query_click(self):
        if self.report_dwmc.where_dwbh:

            if self.report_dwmc.where_dwbh=='00000':
                mes_about(self,'不存在该单位，请重新选择！')
                return
            count = 0
            tmp = {
                'tjqx': 0,
                'tjdj': 0,
                'tjqd': 0,
                'tjzz': 0,
                'tjzj': 0,
                'tjsh': 0,
                'tjsy': 0,
                'tjdy': 0,
                'tjzl': 0,
                'tjlq': 0,
                'sum':0
            }
            results = self.session.execute(get_report_progress_sum_sql(self.report_dwmc.where_dwbh)).fetchall()
            for result in results:
                tmp[result[0]] = result[1]
                count = count + result[1]
            tmp['sum'] = count
            self.table_report_progress.load([tmp])

        else:
            mes_about(self,'请先选择单位！')


    def on_btn_order_click(self):
        pass

    # 导出功能
    def on_btn_export_click(self):
        self.table_report_detail.export()

    #预览报告
    def on_btn_view_click(self):
        tjbh = self.table_report_detail.getCurItemValueOfKey('tjbh')
        xm = self.table_report_detail.getCurItemValueOfKey('xm')
        dwmc = self.table_report_detail.getCurItemValueOfKey('dwmc')
        if not tjbh:
            mes_about(self,'请先选择一个人！')
            return
        else:
            url_title = "体检编号：%s   姓名：%s   单位名称：%s" %(tjbh,xm,dwmc)
            # 优先打开 新系统生成的
            result = self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).scalar()
            if result:
                filename = os.path.join(result.bglj, '%s.pdf' % tjbh).replace('D:/activefile/', '')
                url = gol.get_value('api_pdf_new_show') % filename
                self.open_url(url, url_title)
                # webbrowser.open(url)
            else:
                try:
                    self.cxk_session = gol.get_value('cxk_session')
                    result = self.cxk_session.query(MT_TJ_PDFRUL).filter(MT_TJ_PDFRUL.TJBH == tjbh).scalar()
                    if result:
                        url = gol.get_value('api_pdf_old_show') % result.PDFURL
                        self.open_url(url, url_title)
                    else:
                        mes_about(self, '未找到该顾客体检报告！')
                except Exception as e:
                    mes_about(self, '查询出错，错误信息：%s' % e)
                    return

    # 在窗口中打开报告，取消在浏览器中打开，主要用于外部查询中使用，避免地址外泄
    def open_url(self, url, title):
        if not self.browser:
            self.browser = QBrowser(self)
        self.browser.open_url.emit(title, url)
        self.browser.show()

    # 打印
    def on_btn_print_click(self):
        rows = self.table_report_detail.isSelectRows()
        if not rows:
            return
        is_remote,printer = self.gp_print_setup.get_printer()
        self.printer = printer
        button = mes_warn(self, "您确认用打印机：%s，打印当前选择的 %s 份体检报告？" %(printer,len(rows)))
        if button != QMessageBox.Yes:
            return
        net_print_ui = ReportPrintProgress(self)
        # 获取要打印的数据，并更新UI
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

    def on_btn_review_click(self):
        # 判断状态
        if '已审核' not in self.gp_right_bottom.title():
            mes_about(self,'医生审核完成的报告，才可进行护理三审，请重新选择！')
            return
        # 是否选择了报告
        rows = self.table_report_detail.isSelectRows()
        if not rows:
            mes_about(self,'请选择要审阅的报告！')
            return
        #
        ui = ReportReviewFullScreen(self)
        ui.opened.emit(self.table_report_review.cur_data_set, self.table_report_review.currentIndex().row())
        ui.showMaximized()

