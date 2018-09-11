from widgets.cwidget import *
from .model import *

# 客户满意度
class ItemResultReturn(Widget):

    def __init__(self,parent=None):
        super(ItemResultReturn,self).__init__(parent)
        self.initUI()
        # 绑定信号槽
        self.btn_query.clicked.connect(self.on_btn_query_click)
        self.btn_export.clicked.connect(self.on_btn_export_click)
        self.btn_item_lis.clicked.connect(partial(self.on_btn_click,'检验'))
        self.btn_item_pacs.clicked.connect(partial(self.on_btn_click,'检查'))
        self.btn_item_pis.clicked.connect(partial(self.on_btn_click,'功能'))

        # 特殊变量 用于快速获取/复用
        self.query_thread = None
        self.pd_ui = None
        self.pd_ui_num = 0
        self.cur_start_time = None  # 入口保持一致
        self.cur_end_time = None    # 入口保持一致

    def on_btn_click(self,btn_name):
        if btn_name == '检验':
            sql = get_report_item_cq_sql(2,self.cur_start_time,self.cur_end_time)
        elif btn_name == '检查':
            sql = get_report_item_cq_sql(3, self.cur_start_time, self.cur_end_time)
        else:
            sql = get_report_item_cq_sql(1, self.cur_start_time, self.cur_end_time)
        # 线程执行
        self.execQuery(sql)
        # 进度条
        self.pd_ui = ProgressDialog(self)
        self.pd_ui.show()


    def on_btn_query_click(self):
        self.cur_start_time = self.de_start.text()
        self.cur_end_time = self.de_end.text()
        self.execQuery(get_report_item_sql(self.cur_start_time,self.cur_end_time),False)
        # 进度条
        self.pd_ui = ProgressDialog(self)
        self.pd_ui.show()

    # 导出功能
    def on_btn_export_click(self):
        self.table_item_cq.export()

    # 启动线程 执行查询
    def execQuery(self,sql,flag=True):
        if not self.query_thread:
            self.query_thread = ReportItemQueryThread(self.session)
        self.query_thread.execSql(sql,flag)
        self.query_thread.signalMes.connect(self.on_mes_show2, type=Qt.QueuedConnection)
        self.query_thread.signalMesSql.connect(self.on_mes_show, type=Qt.QueuedConnection)
        self.query_thread.start()

    def on_mes_show(self,mes:bool,result:list,num:int,error:str):
        if self.pd_ui_num == num:
            return
        else:
            self.pd_ui_num = num
        if self.pd_ui:
            if not self.pd_ui.isHidden():
                self.pd_ui.hide()
        if mes:
            self.table_item_cq.load(result)
            self.gp_right_top.setTitle('详细列表（%s）' %self.table_item_cq.rowCount())
        else:
            mes_about(self,"查询出错，错误信息：%s" %error)

    def on_mes_show2(self,mes:bool,result:list,num:int,error:str):
        if self.pd_ui_num == num:
            return
        else:
            self.pd_ui_num = num
        if self.pd_ui:
            if not self.pd_ui.isHidden():
                self.pd_ui.hide()
        if mes:
            count = 0
            lis_count = 0
            pacs_count = 0
            pis_count = 0
            lis_cq_count = 0
            pacs_cq_count = 0
            pis_cq_count = 0
            for i in result:
                count = count + i[1]
                if i[0] == '1':
                    if i[2] == 1:
                        pis_cq_count = i[1]
                    else:
                        pis_count = i[1]
                elif i[0] == '2':
                    if i[2] == 1:
                        lis_cq_count = i[1]
                    else:
                        lis_count = i[1]
                elif i[0] == '3':
                    if i[2] == 1:
                        pacs_cq_count = i[1]
                    else:
                        pacs_count = i[1]

            self.lb_item_lis.setText('{:.1f}%'.format(lis_cq_count / (lis_count+lis_cq_count) * 100))
            self.lb_item_pacs.setText('{:.1f}%'.format(pacs_cq_count / (pacs_count + pacs_cq_count) * 100))
            self.lb_item_pis.setText('{:.1f}%'.format(pis_cq_count / (pis_count + pis_cq_count) * 100))
            self.gp_left_middle.setTitle('项目结果超期率 总数：%s  检验：%s  检查：%s  功能：%s' %(
                count,lis_count+lis_cq_count,pacs_count + pacs_cq_count,pis_count + pis_cq_count
            ))
        else:
            mes_about(self,"查询出错，错误信息：%s" %error)

    def initUI(self):
        lt_main = QHBoxLayout()
        # 总体分左右布局
        lt_left = QVBoxLayout()
        lt_right = QHBoxLayout()
        ################# 条件检索 ##############################
        lt_left_top = QHBoxLayout()
        gp_left_top = QGroupBox('条件检索')
        self.de_start = QDateEdit(QDate.currentDate())
        self.de_end = QDateEdit(QDate.currentDate().addDays(1))
        self.de_start.setCalendarPopup(True)
        self.de_start.setDisplayFormat("yyyy-MM-dd")
        self.de_end.setCalendarPopup(True)
        self.de_end.setDisplayFormat("yyyy-MM-dd")
        self.btn_query = QPushButton(Icon('query'),'查询')
        self.btn_export = QPushButton(Icon('导出'), '导出')
        lt_left_top.addWidget(QLabel("操作时间："))
        lt_left_top.addWidget(self.de_start)
        lt_left_top.addWidget(QLabel('-'))
        lt_left_top.addWidget(self.de_end)
        lt_left_top.addWidget(self.btn_query)
        lt_left_top.addWidget(self.btn_export)
        lt_left_top.addStretch()
        gp_left_top.setLayout(lt_left_top)
        ################## 指标栏 ######################
        lt_left_middle = QHBoxLayout()
        self.gp_left_middle = QGroupBox('项目结果超期率')
        self.btn_item_lis = QPushButton(Icon('LIS'),'检验项目')
        self.btn_item_pacs = QPushButton(Icon('pacs'),'检查项目')
        self.btn_item_pis = QPushButton(Icon('pis'),'功能项目')
        self.lb_item_lis= BtnLable()  # 扫单率
        self.lb_item_pacs = BtnLable()  # 推送率
        self.lb_item_pis = BtnLable()  # 关注率
        # 添加布局
        lt_left_middle.addWidget(self.btn_item_lis)
        lt_left_middle.addWidget(self.lb_item_lis)
        lt_left_middle.addSpacing(10)
        lt_left_middle.addWidget(self.btn_item_pacs)
        lt_left_middle.addWidget(self.lb_item_pacs)
        lt_left_middle.addSpacing(10)
        lt_left_middle.addWidget(self.btn_item_pis)
        lt_left_middle.addWidget(self.lb_item_pis)
        lt_left_middle.addSpacing(10)
        self.gp_left_middle.setLayout(lt_left_middle)
        ################# 图表栏 ##########################
        lt_left_bottom = QHBoxLayout()
        gp_left_bottom = QGroupBox()
        gp_left_bottom.setLayout(lt_left_bottom)
        ################# 右侧详细列表 ##########################
        lt_right_top = QHBoxLayout()
        self.gp_right_top = QGroupBox('详细列表（0）')
        # 关注
        self.table_item_cq_cols = OrderedDict([
            ('tjbh', '体检编号'),
            ('xmbh', '项目编号'),
            ('xmmc', '项目名称'),
            ('xmlx', '项目类型'),
            ('qdrq', '体检日期'),
            ('jcrq', '结果日期'),
            ('xmzq', '默认周期'),
            ('sjzq', '实际周期'),
            ('xmcq', '超期')
        ])
        self.table_item_cq = ReportItemTable(self.table_item_cq_cols)
        lt_right_top.addWidget(self.table_item_cq)
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


class ReportItemTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(ReportItemTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(row_index)
            for col_index, col_value in enumerate(row_data):
                if col_index in [2,3]:
                    item = QTableWidgetItem(str2(col_value))
                elif col_index in[6,7]:
                    item = QTableWidgetItem(str(col_value))
                elif col_index==8:
                    item = QTableWidgetItem(str(col_value))
                    item.setBackground(QColor("#FF0000"))
                else:
                    item = QTableWidgetItem(col_value)
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

            self.setColumnWidth(0, 80)
            self.setColumnWidth(1, 70)
            self.setColumnWidth(2, 120)
            self.setColumnWidth(3, 80)
            self.setColumnWidth(4, 80)
            self.setColumnWidth(5, 80)
            self.horizontalHeader().setStretchLastSection(True)

class BtnLable(QLabel):

    def __init__(self):
        super(BtnLable,self).__init__()
        # self.setFixedHeight(30)
        self.setStyleSheet('''font: 75 16pt \"微软雅黑\";color: rgb(0, 85, 255);''')

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

# 定制的查询线程，需要同时处理多个数据库的多条SQL语句
class ReportItemQueryThread(QThread):

    # 定义信号,定义参数为str类型
    signalMes = pyqtSignal(bool,list,int,str)        #成功/失败，任务结果 最后一个参数，用于防止静态方法mes_about 重复弹出的问题
    signalMesSql = pyqtSignal(bool, list, int,str)  # 成功/失败，任务结果 最后一个参数，用于防止静态方法mes_about 重复弹出的问题
    signalExit = pyqtSignal()                # 退出线程

    def __init__(self,session):
        super(ReportItemQueryThread,self).__init__()
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

    def execSql(self,sql,flag=True):
        self.flag = flag
        self.sql = sql
        self.runing = True

    def run(self):
        while self.runing:
            try:
                results = self.session.execute(self.sql).fetchall()
                if self.flag:
                    self.signalMesSql.emit(True, results,self.num,'')
                else:
                    self.signalMes.emit(True, results, self.num, '')
            except Exception as e:
                if self.flag:
                    self.signalMesSql.emit(False, [],self.num,e)
                else:
                    self.signalMes.emit(False, [], self.num, e)

            self.num = self.num + 1
            self.stop()