from widgets.cwidget import *
from utils import get_wx_session
from .model import *

# 客户满意度
class CustomSatisfaction(Widget):

    def __init__(self,parent=None):
        super(CustomSatisfaction,self).__init__(parent)
        self.initUI()
        # 绑定信号
        self.btn_query.clicked.connect(self.on_btn_query_click)
        self.btn_export.clicked.connect(self.on_btn_export_click)
        self.btn_rate_sd.clicked.connect(partial(self.on_btn_click,'扫单率'))
        self.btn_rate_ts.clicked.connect(partial(self.on_btn_click,'推送率'))
        self.btn_rate_gz.clicked.connect(partial(self.on_btn_click,'关注率'))
        self.btn_rate_tx.clicked.connect(partial(self.on_btn_click,'填写率'))
        self.btn_rate_hp.clicked.connect(partial(self.on_btn_click,'好评率'))
        # 特殊变量 用于快速获取、重复利用
        self.query_thread = None    # 查询线程，用于耗时查询
        self.cur_start_time = None  # 入口保持一致
        self.cur_end_time = None    # 入口保持一致
        self.pd_ui = None           # 进度条
        self.pd_ui_num = 0  # 进度条计数，用于处理线程->UI静态变量 弹窗造成的BUG
        try:
            self.myd_session = get_wx_session()
        except Exception as e:
            self.myd_session = None
            mes_about(self,'微信公众号数据库连接失败，请检查Ora配置！错误信息：%s' %e)

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
        self.gp_left_middle = QGroupBox('满意度指标')
        self.btn_rate_sd = QPushButton(Icon('扫单率'),'扫单率')
        self.btn_rate_ts = QPushButton(Icon('推送率'),'推送率')
        self.btn_rate_gz = QPushButton(Icon('关注率'),'关注率')
        self.btn_rate_tx = QPushButton(Icon('填写率'),'填写率')
        self.btn_rate_hp = QPushButton(Icon('好评率'),'好评率')
        self.lb_rate_sd = BtnLable()  # 扫单率
        self.lb_rate_ts = BtnLable()  # 推送率
        self.lb_rate_gz = BtnLable()  # 关注率
        self.lb_rate_tx = BtnLable()  # 填写率
        self.lb_rate_hp = BtnLable()  # 好评率
        # 添加布局
        lt_left_middle.addWidget(self.btn_rate_sd)
        lt_left_middle.addWidget(self.lb_rate_sd)
        lt_left_middle.addSpacing(10)
        lt_left_middle.addWidget(self.btn_rate_ts)
        lt_left_middle.addWidget(self.lb_rate_ts)
        lt_left_middle.addSpacing(10)
        lt_left_middle.addWidget(self.btn_rate_gz)
        lt_left_middle.addWidget(self.lb_rate_gz)
        lt_left_middle.addSpacing(10)
        lt_left_middle.addWidget(self.btn_rate_tx)
        lt_left_middle.addWidget(self.lb_rate_tx)
        lt_left_middle.addSpacing(10)
        lt_left_middle.addWidget(self.btn_rate_hp)
        lt_left_middle.addWidget(self.lb_rate_hp)
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
        self.table_cs_detail_cols = OrderedDict([
            ('state', '状态'),
            ('tjbh', '体检编号'),
            ('name', '姓名'),
            ('zdsj', '作答时间'),
            ('sjhm', '联系方式'),
            ('mydpf', '满意度评分'),
            ('mydbz', '意见箱'),
        ])
        # 好评列表
        self.table_cs_hp_cols = OrderedDict([
            ('state', '状态'),
            ('tjbh', '体检编号'),
            ('name', '姓名'),
            ('zdsj', '作答时间'),
            ('sjhm', '联系方式'),
            ('mydpf', '满意度评分')
        ])
        # 填写列表
        self.table_cs_tx_cols = OrderedDict([
            ('state', '状态'),
            ('tjbh', '体检编号'),
            ('name', '姓名'),
            ('zdsj', '作答时间'),
            ('sjhm', '联系方式'),
            ('yypc', '预约排程'),
            ('tjlc', '体检流程'),
            ('zysp', '专业水平'),
            ('yhfw', '医护服务'),
            ('zcfw', '早餐服务'),
            ('suggestion', '意见箱')
        ])
        self.table_cs_detail = CustomSatisfactionTable(self.table_cs_detail_cols)
        lt_right_top.addWidget(self.table_cs_detail)
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

    def on_btn_query_click(self):
        self.cur_start_time = self.de_start.text()
        self.cur_end_time = self.de_end.text()
        if self.myd_session:
            sql_maps = {}
            sql_maps['rate_qd'] = get_qd_sql(self.cur_start_time,self.cur_end_time)
            sql_maps['rate_sd'] = get_sd_sql(self.cur_start_time,self.cur_end_time)
            sql_maps['rate_ts'] = get_ts_sql(self.cur_start_time, self.cur_end_time)
            sql_maps['rate_gz'] = get_gz_sql(self.cur_start_time, self.cur_end_time)
            sql_maps['rate_tx'] = get_tx_sql(self.cur_start_time, self.cur_end_time)
            sql_maps['rate_fs'] = get_myd_score_sql(self.cur_start_time, self.cur_end_time)
            self.execQuery(sql_maps)
            # 进度条
            self.pd_ui = ProgressDialog(self)
            self.pd_ui.show()
        else:
            mes_about(self, '微信公众号数据库连接失败，请检查Ora配置！')

    # 绑定 指标按钮
    def on_btn_click(self,btn_name:str):
        if not all([self.cur_start_time,self.cur_end_time]):
            mes_about(self,'查询后再点击各指标按钮查看明细数据！')
            return
        if btn_name == '好评率':
            results = self.myd_session.execute(get_myd_hp_sql(self.cur_start_time,self.cur_end_time)).fetchall()
            self.table_cs_detail.load(results,self.table_cs_hp_cols)
        elif btn_name =='填写率':
            results = self.myd_session.execute(get_myd_tx_sql(self.cur_start_time,self.cur_end_time)).fetchall()
            self.table_cs_detail.load(results,self.table_cs_tx_cols)
        elif btn_name == '关注率':
            results = self.myd_session.execute(get_myd_sum_sql(self.cur_start_time,self.cur_end_time)).fetchall()
            self.table_cs_detail.load(results,self.table_cs_detail_cols)

        elif btn_name == '推送率':
            pass
        else:
            pass

        self.gp_right_top.setTitle('%s：详细列表（%s）' %(btn_name,self.table_cs_detail.rowCount()))
        mes_about(self,'检索出 %s 条数据！'%self.table_cs_detail.rowCount())

    # 导出功能
    def on_btn_export_click(self):
        self.table_cs_detail.export()

    # 启动线程 执行查询
    def execQuery(self,sql_maps:dict):
        if not self.query_thread:
            self.query_thread = mydQueryThread(self.myd_session,self.session)
        self.query_thread.setTask(sql_maps)
        self.query_thread.signalMes.connect(self.on_mes_show, type=Qt.QueuedConnection)
        self.query_thread.start()

    def on_mes_show(self,mes:bool,result:dict,num:int):
        if self.pd_ui_num == num:
            return
        else:
            self.pd_ui_num = num
        if self.pd_ui:
            if not self.pd_ui.isHidden():
                self.pd_ui.hide()
        if mes:
            if all([result['qdrs'],result['tsrs'],result['gzrs']]):
                self.lb_rate_sd.setText('{:.1f}%'.format(result['sdrs'] / result['qdrs'] * 100))
                self.lb_rate_ts.setText('{:.1f}%'.format(result['tsrs'] / result['qdrs'] * 100))
                self.lb_rate_gz.setText('{:.1f}%'.format(result['gzrs'] / result['tsrs'] * 100))
                self.lb_rate_tx.setText('{:.1f}%'.format(result['txrs'] / result['gzrs'] * 100))
                self.lb_rate_hp.setText('{:.1f}%'.format(result['score']))
                self.gp_left_middle.setTitle('满意度指标（体检：%s  扫单：%s  关注：%s  作答：%s）' %(
                    str(result['qdrs']),str(result['sdrs']),str(result['gzrs']),str(result['txrs'])
                ))
            else:
                mes_about(self,'未检索到数据或者该段时间关注人数为零！')

        else:
            mes_about(self,"查询出错，错误信息：%s" %result['error'] )

class CustomSatisfactionTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(CustomSatisfactionTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(row_index)
            for col_index, col_value in enumerate(row_data):
                item = QTableWidgetItem(col_value)
                if col_index == 0 :
                    if col_value =='收到未作答':
                        item.setBackground(QColor("#FF0000"))
                    else:
                        item.setBackground(QColor("#008000"))
                    item.setTextAlignment(Qt.AlignCenter)
                elif col_index == len(self.heads) -1:
                    pass
                else:
                    item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

            self.setColumnWidth(0, 80)
            self.setColumnWidth(1, 70)
            self.setColumnWidth(2, 55)
            self.setColumnWidth(3, 80)
            self.setColumnWidth(4, 80)
            self.setColumnWidth(5, 80)
            self.horizontalHeader().setStretchLastSection(True)


# 定制的查询线程，需要同时处理多个数据库的多条SQL语句
class mydQueryThread(QThread):

    # 定义信号,定义参数为str类型
    signalMes = pyqtSignal(bool,dict,int)        #成功/失败，任务结果 最后一个参数，用于防止静态方法mes_about 重复弹出的问题
    signalExit = pyqtSignal()                # 退出线程

    def __init__(self,session_myd,session_tj):
        super(mydQueryThread,self).__init__()
        self.runing = False
        self.session_myd = session_myd               # 满意度数据库会话
        self.session_tj = session_tj                 # 体检数据库会话
        self.num = 1

    def stop(self):
        self.runing = False

    # 启动任务
    def setTask(self,sql_maps:dict):
        self.sql_maps =sql_maps
        self.runing = True

    def run(self):
        while self.runing:
            result = {'qdrs': 0, 'sdrs': 0, 'gzrs': 0, 'txrs': 0,'score':0,'error':None}
            try:
                result['qdrs'] = self.session_tj.execute(self.sql_maps['rate_qd']).scalar()
                result['sdrs'] = self.session_tj.execute(self.sql_maps['rate_sd']).scalar()
                result['tsrs'] = self.session_tj.execute(self.sql_maps['rate_ts']).scalar()
                result['gzrs'] = self.session_myd.execute(self.sql_maps['rate_gz']).scalar()
                result['txrs'] = self.session_myd.execute(self.sql_maps['rate_tx']).scalar()
                result['score'] = self.session_myd.execute(self.sql_maps['rate_fs']).scalar()
                self.signalMes.emit(True, result,self.num)
            except Exception as e:
                result['error'] = e
                self.signalMes.emit(False, result,self.num)
            self.num = self.num + 1
            self.stop()

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