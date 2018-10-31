from .model import *
from widgets.cwidget import *
from widgets.utils import CefWidget
from .report_item_ui import ItemsStateUI
from utils import gol,api_print,request_get,print_pdf_gsprint
from utils import cur_datetime,request_create_report,report_sms_content,sms_api


class ReportReviewFullScreen(Dialog):

    # 自定义 信号，封装对外使用
    opened = pyqtSignal(list,int)   #待审阅的数据，和当前开始审阅的索引

    def __init__(self,parent=None):
        super(ReportReviewFullScreen,self).__init__(parent)
        self.setWindowTitle('报告审阅')
        self.initUI()
        self.datas = None   # 结果集
        self.cur_index = 0  # 当前索引
        self.opened.connect(self.initData)
        self.btn_previous.clicked.connect(self.on_btn_previous_click)
        self.btn_next.clicked.connect(self.on_btn_next_click)
        self.btn_fullscreen.clicked.connect(self.on_btn_fullscreen_click)
        self.btn_item.clicked.connect(self.on_btn_item_click)
        self.btn_pic.clicked.connect(self.on_btn_pic_click)
        self.btn_reload.clicked.connect(self.on_btn_reload_click)
        self.btn_rebuild.clicked.connect(self.on_btn_rebuild_click)
        # 审阅
        self.gp_review_user.btnClick.connect(self.on_btn_review_click)
        self.gp_review_user.btnCancle.connect(self.on_btn_cancle_click)

        # 特殊变量 用于快速获取 复用
        self.cur_tjbh = None
        self.cur_data = None
        self.item_ui = None

    # 退回
    def on_btn_cancle_click(self,p_str):
        # 更新数据库 TJ_CZJLB TJ_BGGL
        data_obj = {
            'jllx': '0033', 'jlmc': '审阅退回', 'tjbh': self.cur_tjbh, 'mxbh': '','czgh': self.login_id,
            'czxm': self.login_name, 'czqy': self.login_area,'bz': p_str
            }
        try:
            sql = "UPDATE TJ_TJDJB SET TJZT='4' WHERE TJBH ='%s' " %self.cur_tjbh
            self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
            self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == self.cur_tjbh).update({
                MT_TJ_BGGL.bgzt:'0', MT_TJ_BGGL.bgth:'1',MT_TJ_BGGL.gcbz: p_str,MT_TJ_BGGL.sybz: p_str
            })
            self.session.execute(sql)
            self.session.commit()
            mes_about(self,'退回成功！')
        except Exception as e:
            self.session.rollback()
            mes_about(self, '更新数据库失败！错误信息：%s' % e)
            return

    # 全屏
    def on_btn_fullscreen_click(self):
        button = mes_warn(self,"您确定退出全屏审阅模式？")
        if button == QMessageBox.Yes:
            self.close()
        else:
            pass

    # 上一个
    def on_btn_previous_click(self):
        try:
            self.cur_index = self.cur_index - 1
            self.open_page(self.datas[self.cur_index])
        except Exception as e:
            mes_about(self,'当前是最后一份报告')
        # if abs(self.cur_index) <= len(self.datas)-1:
        #     mes_about(self,'当前是最后一份报告')
        #     return

    # 下一个
    def on_btn_next_click(self):
        # if self.cur_index <= len(self.datas)-1:
        #     mes_about(self,'当前是最后一份报告')
        #     return
        try:
            self.cur_index = self.cur_index + 1
            self.open_page(self.datas[self.cur_index])
        except Exception as e:
            print(e)
            mes_about(self, '当前是最后一份报告')

    def initData(self,datas,index):
        print(len(datas),index)
        self.datas=datas
        self.cur_index=index
        self.open_page(datas[self.cur_index])
        # self.cur_index = self.cur_index + 1

    # 放射检查项目接收
    def on_btn_pic_click(self):
        pass

    def on_btn_reload_click(self):
        self.wv_report_equip.reload()

    def on_btn_rebuild_click(self):
        if request_create_report(self.cur_tjbh, 'html'):
            mes_about(self, "重新生成HTML报告成功！")
        else:
            mes_about(self, "重新生成HTML报告失败！")

    # 打开页面
    def open_page(self,data):
        self.cur_data = data
        bgzt = data[0]
        tjbh = data[3]
        xm = data[4]
        xb = data[5]
        nl = data[6]
        syrq = data[7]
        syxm = data[8]
        dwmc = data[9]
        sybz = data[10]
        self.cur_tjbh = tjbh
        # 更新title
        self.gp_bottom.setTitle('体检编号：%s  姓名：%s 性别：%s  年龄：%s  单位名称：%s' %(tjbh,xm,xb,nl,dwmc))
        self.gp_bottom.setStyleSheet('''font: 75 14pt '微软雅黑';color: rgb(0,128,0);''')
        # 未审阅则打开HTML 页面
        url = gol.get_value('api_report_preview') %('html',tjbh)
        self.wv_report_equip.load(url)
        # 刷新界面
        self.gp_review_user.setData({'sybz':sybz,'syrq':syrq,'syxm':syxm,'syzt':bgzt})
        results = self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == self.cur_tjbh,MT_TJ_TJJLMXB.xmbh.in_(('1122','1931','0903','501732','501933','501934'))).all()
        if results:
            self.gp_review_user.setData2(",".join([str2(result.xmmc) for result in results]))

    def initUI(self):
        lt_main = QVBoxLayout()
        # 审阅栏信息
        self.gp_review_user = ReportReviewUser()
        lt_middle = QHBoxLayout()
        self.btn_previous = QPushButton(Icon('向左'), '上一个')
        self.btn_fullscreen = QPushButton(Icon('全屏'),'退出全屏')
        self.btn_next = QPushButton(Icon('向右'),'下一个')
        self.btn_item = QPushButton(Icon('项目'), '项目查看')
        self.btn_pic = QPushButton(Icon('图片'), '图像接收')
        self.btn_reload = QPushButton(Icon('刷新'), '刷新报告')
        self.btn_rebuild = QPushButton(Icon('刷新'), '重新生成')
        lable = QLabel('审阅完成：')
        lable.setStyleSheet('''font: 75 14pt '微软雅黑';color: rgb(255,0,0);height:16px;''')
        self.btn_auto_next = QCheckBox('自动下一份')
        self.btn_auto_next.setChecked(False)
        self.btn_auto_print = QCheckBox('自动打印报告')
        self.btn_auto_print.setChecked(False)
        self.btn_auto_sms = QCheckBox('自动发送短信')
        self.btn_auto_sms.setChecked(False)
        lt_middle.addStretch()
        lt_middle.addWidget(self.btn_previous)
        lt_middle.addSpacing(20)
        lt_middle.addWidget(self.btn_fullscreen)
        lt_middle.addSpacing(20)
        lt_middle.addWidget(self.btn_next)
        lt_middle.addSpacing(20)
        lt_middle.addWidget(self.btn_item)
        lt_middle.addSpacing(20)
        lt_middle.addWidget(self.btn_reload)
        lt_middle.addSpacing(20)
        lt_middle.addWidget(self.btn_rebuild)
        # lt_middle.addSpacing(20)
        # lt_middle.addWidget(self.btn_pic)
        lt_middle.addStretch()
        lt_middle.addWidget(lable)
        lt_middle.addWidget(self.btn_auto_next)
        lt_middle.addWidget(self.btn_auto_print)
        lt_middle.addWidget(self.btn_auto_sms)
        # 报告预览
        # self.wv_report_equip = WebView(self)
        self.wv_report_equip = CefWidget(self)
        lt_bottom = QHBoxLayout()
        lt_bottom.addWidget(self.wv_report_equip)
        self.gp_bottom = QGroupBox('报告预览')
        self.gp_bottom.setLayout(lt_bottom)

        lt_main.addWidget(self.gp_review_user,2)
        lt_main.addWidget(self.gp_bottom,37)
        lt_main.addLayout(lt_middle,1)

        self.setLayout(lt_main)

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

    # 审阅/取消审阅
    def on_btn_review_click(self,syzt:bool,num:int):
        # 未双击过查看过报告 不允许审核
        if not self.cur_tjbh:
            mes_about(self,'您还未打开报告，不允许审阅')
            return
        # 完成审阅
        if syzt:
            # 更新数据库 TJ_CZJLB TJ_BGGL
            data_obj = {'jllx':'0031','jlmc':'报告审阅','tjbh':self.cur_tjbh,'mxbh':'',
                         'czgh':self.login_id,'czxm':self.login_name,'czqy':self.login_area,'jlnr':str(num),'bz':self.gp_review_user.get_sybz()}
            try:
                self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == self.cur_tjbh).update(
                    {
                        MT_TJ_BGGL.syxm: self.login_name,
                        MT_TJ_BGGL.sygh: self.login_id,
                        MT_TJ_BGGL.syrq: cur_datetime(),
                        MT_TJ_BGGL.sybz: self.gp_review_user.get_sybz(),
                        MT_TJ_BGGL.sysc: num,
                        MT_TJ_BGGL.bgzt: 2,
                    }
                )
                sql = "UPDATE TJ_TJDJB SET TJZT='8' WHERE TJBH='%s';" %self.cur_tjbh
                self.session.execute(sql)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                mes_about(self,'更新数据库失败！错误信息：%s' %e)
                return
            # 刷新控件
            self.gp_review_user.statechange()
            # 刷新内存中的数据
            self.cur_data[0] = '已审阅'
            self.cur_data[7] = cur_datetime()
            self.cur_data[8] = self.login_name
            self.cur_data[10] = self.gp_review_user.get_sybz()
            self.datas[self.cur_index] = self.cur_data
            self.gp_review_user.setData({'sybz': self.gp_review_user.get_sybz(), 'syrq': cur_datetime(), 'syxm': self.login_name, 'syzt': 2})
            # HTML 报告需要重新生成
            request_create_report(self.cur_tjbh, 'html')
            # 生成PDF 报告请求
            request_create_report(self.cur_tjbh, 'pdf')
            # 是否发送短信
            if self.btn_auto_sms.isChecked():
                try:
                    result = self.session.query(MV_RYXX).filter(MV_RYXX.tjbh == self.cur_tjbh).scalar()
                    if result.sjhm:
                        sms_api(result.sjhm,report_sms_content)
                except Exception as e:
                    mes_about(self,"短信发送失败！错误信息：%s" %e)
            # 是否下一个
            if self.btn_auto_next.isChecked():
                self.on_btn_next_click()
        # 取消审阅
        else:
            if not self.gp_review_user.get_sybz():
                mes_about(self,'请您输入取消审阅原因！')
                return
            # 更新数据库 TJ_CZJLB TJ_BGGL
            data_obj = {'jllx':'0032','jlmc':'取消审阅','tjbh':self.cur_tjbh,'mxbh':'',
                         'czgh':self.login_id,'czxm':self.login_name,'czqy':self.login_area,'bz':self.gp_review_user.get_sybz()}
            try:
                self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == self.cur_tjbh).update(
                    {
                        MT_TJ_BGGL.syxm: None,
                        MT_TJ_BGGL.sygh: None,
                        MT_TJ_BGGL.syrq: None,
                        MT_TJ_BGGL.sybz: None,
                        MT_TJ_BGGL.gcbz: self.gp_review_user.get_sybz(),
                        MT_TJ_BGGL.sysc: 0,
                        MT_TJ_BGGL.bgzt: 1,
                    }
                )
                sql = "UPDATE TJ_TJDJB SET TJZT='7' WHERE TJBH='%s';" %self.cur_tjbh
                self.session.execute(sql)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                mes_about(self,'更新数据库失败！错误信息：%s' %e)
                return
            # 刷新控件
            self.gp_review_user.clearData()                                                     # 清空数据
            # 刷新内存中的数据
            self.cur_data[0] = '已审核'
            self.cur_data[7] = ''
            self.cur_data[8] = ''
            self.cur_data[10] = self.gp_review_user.get_sybz()
            self.datas[self.cur_index] = self.cur_data

    def closeEvent(self, QCloseEvent):
        if self.item_ui:
            self.item_ui.close()
        super(ReportReviewFullScreen, self).closeEvent(QCloseEvent)

class ReportReviewUser(QGroupBox):

    # 自定义 信号，封装对外使用
    btnClick = pyqtSignal(bool,int)
    # 取消事件
    btnCancle = pyqtSignal(str)

    def __init__(self):
        super(ReportReviewUser,self).__init__()
        self.initUI()
        self.btn_review.clicked.connect(self.on_btn_review_click)
        self.btn_cancle.clicked.connect(self.on_btn_cancle_click)

    def initUI(self):
        self.setTitle('审阅信息')
        lt_main = QGridLayout()
        self.review_user = ReviewLabel()
        self.review_time = ReviewLabel()
        self.review_comment = QPlainTextEdit()
        self.review_comment.setStyleSheet('''font: 75 12pt '微软雅黑';color: rgb(255,0,0);height:20px;''')
        self.review_comment.setPlaceholderText("审阅备注")
        # 外出项目
        self.review_item = QPlainTextEdit()
        self.review_item.setStyleSheet('''font: 75 10pt '微软雅黑';color: rgb(255,0,0);height:20px;''')
        self.review_item.setDisabled(True)
        self.review_item.setPlaceholderText("手工单备注")
        # 外出项目
        self.review_film = QPlainTextEdit()
        self.review_film.setStyleSheet('''font: 75 10pt '微软雅黑';color: rgb(255,0,0);height:20px;''')
        self.review_film.setDisabled(True)
        self.review_film.setPlaceholderText("胶片备注")
        self.btn_cancle = ToolButton(Icon('取消'),'退回追踪')
        self.btn_review = Timer2Button(Icon('样本签收'),'完成审阅')
        ###################基本信息  第一行##################################
        lt_main.addWidget(QLabel('审阅者：'), 0, 0, 1, 1)
        lt_main.addWidget(self.review_user, 0, 1, 1, 1)
        lt_main.addWidget(QLabel('审阅时间：'), 1, 0, 1, 1)
        lt_main.addWidget(self.review_time, 1, 1, 1, 1)
        ###################基本信息  第二行##################################
        lt_main.addWidget(self.review_item, 0, 2, 2, 1)
        lt_main.addWidget(self.review_film, 0, 3, 2, 1)
        lt_main.addWidget(self.review_comment, 0, 4, 2, 3)
        # 按钮
        lt_main.addWidget(self.btn_cancle, 0, 7, 2, 2)
        lt_main.addWidget(self.btn_review, 0, 9, 2, 2)

        lt_main.setHorizontalSpacing(10)            #设置水平间距
        lt_main.setVerticalSpacing(10)              #设置垂直间距
        lt_main.setContentsMargins(10, 10, 10, 10)  #设置外间距
        lt_main.setColumnStretch(4, 1)             #设置列宽，添加空白项的
        self.setLayout(lt_main)
        # 状态标签
        self.lb_review_bz = StateLable(self)
        self.lb_review_bz.show()

    # 清空数据
    def clearData(self):
        self.review_user.setText('')
        self.review_time.setText('')
        self.review_comment.setPlainText('')
        self.lb_review_bz.show2(False)

    # 设置数据
    def setData(self,data:dict):
        self.btn_review.stop()
        if data['syzt']=='已审核':
            self.lb_review_bz.show2(False)
            self.btn_review.start()
        else:
            if all([data['syxm'],data['syrq']]):
                self.lb_review_bz.show2()
                self.btn_review.setText('取消审阅')
            else:
                self.lb_review_bz.show2(False)
                self.btn_review.start()
        self.review_user.setText(data['syxm'])
        self.review_time.setText(data['syrq'])
        self.review_time.setToolTip(data['syrq'])
        self.review_comment.setPlainText(data['sybz'])

    # 显示是否有手动单项目，2018-09-27 新增，个人感觉价值不大，故不合并setData
    def setData2(self,item_name):
        self.review_item.setPlainText(item_name)

    # 状态变更
    def statechange(self):
        # 从完成审阅 -> 取消审阅
        if '完成' in self.btn_review.text():
            self.btn_review.stop()
            self.btn_review.setText('取消审阅')
        else:
            # 刷新控件
            self.btn_cancle.emit(self.review_comment.toPlainText())

    # 获取审阅备注信息
    def get_sybz(self):
        return self.review_comment.toPlainText()

    # 按钮点击
    def on_btn_review_click(self):
        if '完成审阅' in self.btn_review.text():
            syzt = True
        else:
            syzt = False
        try:
            num = self.btn_review.num
        except Exception as e:
            num = 0
        self.btnClick.emit(syzt,num)

    # 退回
    def on_btn_cancle_click(self):
        if self.btn_review.text()=='取消审阅':
            mes_about(self,'请先对报告进行取消审阅操作！')
        else:
            # 退回
            if not self.review_comment.toPlainText():
                mes_about(self,'请先输入报告退回原因')
            else:
                self.btnCancle.emit(self.review_comment.toPlainText())

class ReviewLabel(QLabel):

    def __init__(self,p_str=None,parent=None):
        super(ReviewLabel,self).__init__(p_str,parent)
        self.setStyleSheet('''border: 1px solid;''')
        #self.setStyleSheet('''border: 1px solid;font: 75 9pt \"微软雅黑\";''')
        self.setMinimumWidth(80)
        self.setCursor(QCursor(Qt.PointingHandCursor))

class StateLable(QLabel):

    def __init__(self,parent):
        super(StateLable,self).__init__(parent)
        self.setMinimumSize(200,200)
        self.setGeometry(200,-60,100,100)
        self.setStyleSheet('''font: 75 28pt "微软雅黑";color: rgb(255, 0, 0);''')
        self.setAttribute(Qt.WA_TranslucentBackground)                               #背景透明
        self.data = open(file_ico('已审阅.png'),'rb').read()

    def show2(self,flag = True):
        if flag:
            p = QPixmap()
            p.loadFromData(self.data)
            self.setPixmap(p)
        else:
            self.clear()

class ReportPrintProgress(Dialog):
    # 打印初始化 启动打印线程
    print_init = pyqtSignal(list,str,bool)
    # 打印完成的信号，传递参数给调用方
    printed = pyqtSignal(str, bool)

    def __init__(self,parent=None):
        super(ReportPrintProgress,self).__init__(parent)
        self.setWindowTitle('明州体检')
        self.initUI()
        # 绑定信号
        self.print_init.connect(self.initDatas)
        self.btn_start.clicked.connect(self.on_btn_start_click)
        self.btn_stop.clicked.connect(self.on_btn_stop_click)
        # 特殊变量
        self.datas = None
        self.printer = None
        self.report_print_thread = None
        self.is_remote = None
        # 总数
        self.num_all = 0
        # 完成
        self.num_finished = 0
        # 未完成
        self.num_unfinished = 0
        # 失败
        self.num_fail = 0

    def initUI(self):
        lt_main = QVBoxLayout()
        ###########################################################
        lt_top = QHBoxLayout()
        gp_top = QGroupBox('打印进度总览')
        # 待接收的总数
        self.lb_print_all = ProcessLable()
        # 已完成接收数
        self.lb_print_finished = ProcessLable()
        # 未完成总数
        self.lb_print_unfinished = ProcessLable()
        # 错误数
        self.lb_print_fail = ProcessLable()
        # 添加布局
        lt_top.addWidget(QLabel('打印总数：'))
        lt_top.addWidget(self.lb_print_all)
        lt_top.addWidget(QLabel('已打印数：'))
        lt_top.addWidget(self.lb_print_finished)
        lt_top.addWidget(QLabel('待打印数：'))
        lt_top.addWidget(self.lb_print_unfinished)
        lt_top.addWidget(QLabel('打印失败：'))
        lt_top.addWidget(self.lb_print_fail)
        gp_top.setLayout(lt_top)
        ###########################################################
        lt_middle = QHBoxLayout()
        gp_middle = QGroupBox('处理详情')
        ###########################################################
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox('打印进度')
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
        self.btn_stop.setDisabled(True)
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

    # 打印进度信号
    def on_progress_change(self,tjbh:str,state:bool):
        # 传递信号
        self.printed.emit(tjbh,state)
        # 更新变量
        # self.datas.remove(tjbh)             # 用于暂停功能，重启启动用
        if state:
            self.num_finished = self.num_finished + 1
        else:
            self.num_fail = self.num_fail + 1
        self.num_unfinished = self.num_all - self.num_finished - self.num_fail
        # 刷新UI
        self.lb_print_finished.setText(str(self.num_finished))
        self.lb_print_unfinished.setText(str(self.num_unfinished))
        self.lb_print_fail.setText(str(self.num_fail))
        self.pb_progress.setValue(self.num_finished + self.num_fail)
        # 刷新进度条
        dProgress = (self.pb_progress.value() - self.pb_progress.minimum()) * 100.0 / (self.pb_progress.maximum() - self.pb_progress.minimum())
        #self.progress.setFormat("当前进度为：%s%" %dProgress)
        self.pb_progress.setAlignment(Qt.AlignRight | Qt.AlignVCenter) #对齐方式

    # 启动
    def on_btn_start_click(self):
        # 刷新界面控件
        self.btn_start.setDisabled(True)
        # self.btn_stop.setDisabled(False)
        self.lb_timer.start()
        self.num_all = len(self.datas)
        self.lb_print_all.setText(str(self.num_all))
        self.pb_progress.setMaximum(self.num_all)
        if not self.report_print_thread:
            self.report_print_thread = ReportPrintThread()

        self.report_print_thread.setTask(self.datas,self.printer,self.is_remote)
        self.report_print_thread.signalCur.connect(self.on_progress_change, type=Qt.QueuedConnection)
        self.report_print_thread.signalExit.connect(self.on_thread_exit, type=Qt.QueuedConnection)
        self.report_print_thread.start()

    # 停止接收数据
    def on_btn_stop_click(self):
        # 刷新界面控件
        # self.btn_start.setDisabled(False)
        # self.btn_stop.setDisabled(True)
        self.lb_timer.stop()
        # 停止线程
        try:
            if self.report_print_thread:
                self.report_print_thread.stop()
        except Exception as e:
            print(e)
        self.close()

    # 初始化数据
    def initDatas(self,datas:list,printer:str,is_remote:bool):
        self.datas = datas
        self.printer = printer
        self.is_remote = is_remote
        self.on_btn_start_click()

    def on_thread_exit(self):
        self.on_btn_stop_click()
        self.report_print_thread = None
        mes_about(self,'打印完成！')
        self.close()

    def closeEvent(self, QCloseEvent):
        try:
            if self.report_print_thread:
                # button = mes_warn(self,"当前正在打印报告，您是否确定立刻退出？")
                # if button == QMessageBox.Yes:
                self.report_print_thread.stop()
                self.report_print_thread = None
                # else:
                #     return
        except Exception as e:
            print(e)
        super(ReportPrintProgress, self).closeEvent(QCloseEvent)

# 打印线程
class ReportPrintThread(QThread):

    signalCur = pyqtSignal(str,int)      # 处理过程：成功/失败
    signalExit = pyqtSignal()

    def __init__(self):
        super(ReportPrintThread,self).__init__()
        self.runing = False
        self.initParas()

    def initParas(self):
        # 初始化环境变量
        self.num = 1

    def stop(self):
        self.runing = False

    # 启动任务
    def setTask(self,tjbhs:list,printer:str,is_remote:bool):
        self.tjbhs = tjbhs
        self.printer = printer
        self.is_remote = is_remote
        self.runing = True

    def run(self):
        while self.runing:
            for tjbh in self.tjbhs:
            # for i in range(len(self.tjbhs)-1,-1,-1):
                # 中途暂停打印 处理
                if self.runing:
                    if self.is_remote:
                        # 网络打印
                        if api_print(tjbh, self.printer):
                            # 打印成功
                            self.signalCur.emit(tjbh, 1)
                        else:
                            # 打印失败
                            self.signalCur.emit(tjbh, 0)
                    else:
                        # 本地打印 需要下载
                        url = gol.get_value('api_report_down') % tjbh
                        filename = os.path.join(gol.get_value('path_tmp'), '%s.pdf' % tjbh)
                        if request_get(url, filename):
                            # 打印成功
                            if print_pdf_gsprint(filename) == 0:
                                # 打印成功
                                self.signalCur.emit(tjbh, 1)
                            else:
                                # 打印失败
                                self.signalCur.emit(tjbh, 0)
                        else:
                            # 打印失败
                            self.signalCur.emit(tjbh, 0)
                else:
                    return
            self.stop()
            self.signalExit.emit()

class ProcessLable(QLabel):

    def __init__(self):
        super(ProcessLable, self).__init__()
        self.setMinimumWidth(50)
        self.setStyleSheet('''font: 75 14pt \"微软雅黑\";color: rgb(0, 85, 255);''')

#在浏览器中打开PDF报告
def get_pdf_url(session,tjbh):
    # 优先打开 新系统生成的
    result = session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).scalar()
    if result:
        filename = os.path.join(result.bglj, '%s.pdf' % tjbh).replace('D:/activefile/', '')
        url = gol.get_value('api_pdf_new_show') % filename
        return url
    else:
        try:
            ora_session = gol.get_value('cxk_session')
            result = ora_session.query(MT_TJ_PDFRUL).filter(MT_TJ_PDFRUL.TJBH == tjbh).scalar()
            if result:
                url = gol.get_value('api_pdf_old_show') % result.PDFURL
                return url
            else:
                return False
        except Exception as e:
            return False