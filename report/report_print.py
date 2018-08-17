from .report_print_ui import *
from .model import *
from widgets.bweb import WebView
import webbrowser

# 报告追踪
class ReportPrint(ReportPrintUI):

    def __init__(self):
        super(ReportPrint, self).__init__()
        self.initParas()
        # 绑定信号槽
        self.btn_query.clicked.connect(self.ob_btn_query_click)
        # 右键、双击、单击
        self.table_print.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.table_print.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单
        self.table_print.itemClicked.connect(self.on_table_set)
        self.table_print.itemDoubleClicked.connect(self.on_btn_item_click)
        # 特殊变量
        self.cur_tjbh = None
        self.web_pdf_ui = None

    def initParas(self):
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()
        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)

        self.lt_where_search.s_dwbh.setValues(self.dwmc_bh,self.dwmc_py)

    def ob_btn_query_click(self):
        if self.lt_where_search.get_date_text()=='签到日期':
            t_start,t_end = self.lt_where_search.date_range
            results = self.session.execute(get_report_print_sql(t_start,t_end)).fetchall()
            self.table_print.load(results)
            mes_about(self, '检索出数据%s条' % self.table_print.rowCount())
        else:
            t_start,t_end = self.lt_where_search.date_range
            results = self.session.execute(get_report_print2_sql(t_start,t_end)).fetchall()
            self.table_print.load(results)
            mes_about(self,'检索出数据%s条' %self.table_print.rowCount())

    # 右键功能
    def onTableMenu(self,pos):
        row_num = -1
        indexs=self.table_print.selectionModel().selection().indexes()
        if indexs:
            for i in indexs:
                row_num = i.row()

            menu = QMenu()
            item1 = menu.addAction(Icon("报告中心"), "浏览器中打开PDF报告")
            action = menu.exec_(self.table_print.mapToGlobal(pos))
            if action==item1:
                try:
                    self.cxk_session = gol.get_value('cxk_session')
                    result = self.cxk_session.query(MT_TJ_PDFRUL).filter(MT_TJ_PDFRUL.TJBH == self.table_print.getCurItemValueOfKey('tjbh')).scalar()
                    if result:
                        url = gol.get_value('api_pdf_old_show') % result.PDFURL
                        webbrowser.open(url)
                    else:
                        mes_about(self, '未找到该顾客体检报告！')
                except Exception as e:
                    mes_about(self, '查询出错，错误信息：%s' % e)
                    return

    # 设置快速检索文本
    def on_table_set(self,tableWidgetItem):
        tjbh = self.table_print.getCurItemValueOfKey('tjbh')
        xm = self.table_print.getCurItemValueOfKey('xm')
        sfzh = self.table_print.getCurItemValueOfKey('sfzh')
        sjhm = self.table_print.getCurItemValueOfKey('sjhm')
        self.gp_quick_search.setText(tjbh,xm,sjhm,sfzh)
        self.cur_tjbh = tjbh

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




