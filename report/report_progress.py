from widgets.cwidget import *
from .model import *

# 报告进度
class ReportProgress(Widget):

    def __init__(self,parent=None):
        super(ReportProgress,self).__init__(parent)
        self.initParas()
        self.initUI()
        # 绑定信号槽
        self.btn_query.clicked.connect(self.on_btn_query_click)
        self.btn_export.clicked.connect(self.on_btn_export_click)
        self.table_report_progress.itemClicked.connect(self.on_table_detail)

        # 特殊变量 用于快速获取/复用
        self.query_thread = None
        self.pd_ui_num = 0
        self.cur_start_time = None  # 入口保持一致
        self.cur_end_time = None    # 入口保持一致

    def initParas(self):
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()

        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)

        ###################################################

    def on_table_detail(self,QTableWidgetItem):
        col = QTableWidgetItem.column()
        if col==0:
            sql = get_report_progress_sql(self.report_dwmc.where_dwbh,'0')
        elif col==1:
            sql = get_report_progress_sql(self.report_dwmc.where_dwbh,'1')
        elif col==2:
            sql = get_report_progress_sql(self.report_dwmc.where_dwbh,'3')
        elif col==3:
            sql = get_report_progress_sql(self.report_dwmc.where_dwbh,'4')
        elif col==4:
            sql = get_report_progress_sql(self.report_dwmc.where_dwbh,'6')
        elif col==5:
            sql = get_report_progress_sql(self.report_dwmc.where_dwbh,'7')
        else:
            sql = get_report_progress_sql(self.report_dwmc.where_dwbh, '8')
        if QTableWidgetItem.text()==0:
            mes_about(self,'检索出 0 条数据！')
        else:
            results = self.session.execute(sql).fetchall()
            self.table_report_detail.load(results)
            self.gp_right_top.setTitle('详细列表（%s）' %self.table_report_detail.rowCount())
            mes_about(self, '检索出 %s 条数据！' %self.table_report_detail.rowCount())


    def on_btn_query_click(self):
        if self.report_dwmc.where_dwbh:
            tmp = {'tjqx':0,'tjdj':0,'tjqd':0,'tjzz':0,'tjzj':0,'tjsh':0,'tjsy':0,'tjdy':0}
            if self.report_dwmc.where_dwbh=='00000':
                mes_about(self,'不存在该单位，请重新选择！')
                return
            sql = "SELECT TJZT,COUNT(*) FROM TJ_TJDJB WHERE DWBH ='%s' GROUP BY TJZT" %self.report_dwmc.where_dwbh
            results = self.session.execute(sql).fetchall()
            for result in results:
                if result[0] == '0':
                    tmp['tjqx'] = result[1]
                elif result[0] == '1':
                    tmp['tjdj'] = result[1]
                elif result[0] == '3':
                    tmp['tjqd'] = result[1]
                elif result[0] == '4':
                    tmp['tjzz'] = result[1]
                elif result[0] == '6':
                    tmp['tjzj'] = result[1]
                elif result[0] == '7':
                    tmp['tjsh'] = result[1]
                elif result[0] == '8':
                    tmp['tjsy'] = result[1]

            self.table_report_progress.load([tmp])

        else:
            mes_about(self,'请先选择单位！')


    # 导出功能
    def on_btn_export_click(self):
        self.table_report_detail.export()

    # 启动线程 执行查询
    def execQuery(self,date_range:tuple):
        if not self.query_thread:
            self.query_thread = ReportQueryThread(self.session)
        self.query_thread.setTask(date_range)
        self.query_thread.signalMes.connect(self.on_mes_show, type=Qt.QueuedConnection)
        self.query_thread.start()

    def on_mes_show(self,mes:bool,result:dict,num:int):
        pass

    def initUI(self):
        lt_main = QHBoxLayout()
        # 总体分左右布局
        lt_left = QVBoxLayout()
        lt_right = QHBoxLayout()
        ################# 条件检索 ##############################
        lt_left_top = QHBoxLayout()
        gp_left_top = QGroupBox()
        self.report_dwmc = TUint(self.dwmc_bh, self.dwmc_py)  # 体检单位
        self.btn_query = QPushButton(Icon('query'),'查询')
        self.btn_export = QPushButton(Icon('导出'), '导出')
        lt_left_top.addWidget(QLabel('单位名称：'))
        lt_left_top.addWidget(self.report_dwmc)
        lt_left_top.addWidget(self.btn_query)
        lt_left_top.addWidget(self.btn_export)
        # lt_left_top.addStretch()
        gp_left_top.setLayout(lt_left_top)
        ################## 指标栏 ######################
        lt_left_middle = QHBoxLayout()
        self.gp_left_middle = QGroupBox('单位报告进度')
        self.table_report_progress_cols = OrderedDict([
            ('tjqx', '取消'),
            ('tjdj', '登记'),
            ('tjqd', '签到'),
            ('tjzz', '追踪'),
            ('tjzj', '总检'),
            ('tjsh', '审核'),
            ('tjsy', '审阅'),
            ('tjdy', '打印'),
        ])
        self.table_report_progress = ReportProgressTable(self.table_report_progress_cols)
        # 添加布局
        lt_left_middle.addWidget(self.table_report_progress)
        self.gp_left_middle.setLayout(lt_left_middle)
        ################# 图表栏 ##########################
        lt_left_bottom = QHBoxLayout()
        gp_left_bottom = QGroupBox()
        gp_left_bottom.setLayout(lt_left_bottom)

        ################# 右侧详细列表 ##########################
        lt_right_top = QHBoxLayout()
        self.gp_right_top = QGroupBox('详细列表（0）')
        # 关注
        self.table_report_detail_cols = OrderedDict([
            ('tjzt', '状态'),
            ('tjbh', '体检编号'),
            ('qdrq', '登记日期'),
            ('qdrq', '签到日期'),
            ('sdrq', '收单日期'),
            ('zzrq', '追踪日期'),
            ('zjrq', '总检日期'),
            ('shrq', '审核日期'),
            ('syrq', '三审日期'),
            ('dyrq', '打印日期'),
        ])
        self.table_report_detail = ReportDetailTable(self.table_report_detail_cols)
        lt_right_top.addWidget(self.table_report_detail)
        self.gp_right_top.setLayout(lt_right_top)

        # 添加主布局
        lt_left.addWidget(gp_left_top)
        lt_left.addWidget(self.gp_left_middle)
        lt_left.addWidget(gp_left_bottom)
        lt_left.addStretch()
        lt_right.addWidget(self.gp_right_top)
        lt_main.addLayout(lt_left)
        lt_main.addLayout(lt_right)
        self.setLayout(lt_main)

class ReportProgressTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(ReportProgressTable, self).__init__(heads, parent)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)  # 选中一行

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(row_index)
            for col_index, col_name in enumerate(heads.keys()):
                item = QTableWidgetItem(str(row_data[col_name]))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

        # self.setColumnWidth(0, 40)
        # self.setColumnWidth(1, 40)
        # self.setColumnWidth(2, 40)
        # self.setColumnWidth(3, 40)
        # self.setColumnWidth(4, 40)
        # self.setColumnWidth(5, 40)
        # self.setColumnWidth(6, 40)
        # self.setColumnWidth(7, 40)

class ReportDetailTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(ReportDetailTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(row_index)
            for col_index, col_value in enumerate(row_data):
                if col_index==0:
                    item = QTableWidgetItem(str2(col_value))
                else:
                    item = QTableWidgetItem(col_value)
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

            self.setColumnWidth(0, 60)
            self.setColumnWidth(1, 70)
            self.setColumnWidth(2, 80)
            self.setColumnWidth(3, 80)
            self.setColumnWidth(4, 80)
            self.setColumnWidth(5, 80)
            self.horizontalHeader().setStretchLastSection(True)

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

class BtnLable(QLabel):

    def __init__(self):
        super(BtnLable,self).__init__()
        # self.setFixedHeight(30)
        self.setStyleSheet('''font: 75 16pt \"微软雅黑\";color: rgb(0, 85, 255);''')

# 定制的查询线程，需要同时处理多个数据库的多条SQL语句
class ReportQueryThread(QThread):

    # 定义信号,定义参数为str类型
    signalMes = pyqtSignal(bool,dict,int)        #成功/失败，任务结果 最后一个参数，用于防止静态方法mes_about 重复弹出的问题
    signalExit = pyqtSignal()                # 退出线程

    def __init__(self,session):
        super(ReportQueryThread,self).__init__()
        self.runing = False
        self.session = session
        self.num = 1

    def stop(self):
        self.runing = False

    # 启动任务
    def setTask(self,date_range):
        self.time_start =date_range[0]
        self.time_end = date_range[1]
        self.runing = True

    def run(self):
        while self.runing:
            tmp = {'SUM': 0, 'SDSC': 0, 'ZZSC': 0, 'ZJSC': 0, 'SHSC': 0,
                   'SYSC': 0, 'DYSC': 0, 'error':None}
            sum_count = 0
            sd_count = 0
            zz_count = 0
            zj_count = 0
            sh_count = 0
            sy_count = 0
            dy_count = 0
            try:
                results = self.session.execute(get_report_efficiency_sql(self.time_start,self.time_end)).fetchall()
                if results:
                    for result in results:
                        sum_count = sum_count +1
                        if compare(result[1],8):
                            sd_count = sd_count + 1
                        if compare(result[2],72):
                            zz_count = zz_count + 1
                        if compare(result[3],24):
                            zj_count = zj_count + 1
                        if compare(result[4],24):
                            sh_count = sh_count + 1
                        if compare(result[5],24):
                            sy_count = sy_count + 1
                        if compare(result[6],24):
                            dy_count = dy_count + 1

                tmp = {'SUM': sum_count, 'SDSC': sd_count, 'ZZSC': zz_count, 'ZJSC': zj_count, 'SHSC': sh_count, 'SYSC': sy_count, 'DYSC': dy_count}
                self.signalMes.emit(True, tmp,self.num)
            except Exception as e:
                tmp['error'] = e
                self.signalMes.emit(False, tmp,self.num)
            self.num = self.num + 1
            self.stop()
# X是否比Y大
def compare(x,y):
    if x == 0:
        return False
    else:
        if x:
            if isinstance(x,str):
                if x.isdigit():
                    if int(x) > y:
                        return True
                    else:
                        return False
                else:
                    return True
            elif isinstance(x,int):
                if x>y:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True