from widgets.cwidget import *
from widgets.bweb import *
from .model import *
from .report_item_ui import ItemsStateUI
from utils import cur_datetime,request_create_report,report_sms_content,sms_api

class ReportReviewUI(Widget):

    def __init__(self,parent=None):
        super(ReportReviewUI,self).__init__(parent)
        self.initUI()
        self.initParas()

    def initParas(self):
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()
        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)

        self.gp_where_search.s_dwbh.setValues(self.dwmc_bh,self.dwmc_py)

    def initUI(self):
        lt_main = QHBoxLayout()
        lt_left = QVBoxLayout()
        self.btn_query = ToolButton(Icon('query'), '查询')
        self.btn_review_batch = ToolButton(Icon('批量'), '批量审阅')
        self.btn_review_mode = ToolButton(Icon('全屏'), '全屏审阅')
        self.btn_review_mode2 = ToolButton(Icon('全屏'), '大屏审阅')

        self.gp_where_search = BaseCondiSearchGroup(1)
        self.gp_where_search.setText('审核日期')
        self.gp_where_search.setNoChoice()
        # 报告状态
        self.cb_report_state = ReportStateGroup()
        self.cb_report_state.addStates(['所有','未审阅','已审阅','老未打/新未审'])
        self.cb_report_type = ReportTypeGroup()
        # 区域
        self.cb_area = AreaGroup()
        # 人员
        self.cb_user = UserGroup('审阅护士：')
        self.cb_user.addUsers(['所有',self.login_name])
        # 添加布局
        self.gp_where_search.addItem(self.cb_area, 0, 3, 1, 2)
        self.gp_where_search.addItem(self.cb_report_state, 1, 3, 1, 2)
        self.gp_where_search.addItem(self.cb_user, 0, 5, 1, 2)
        self.gp_where_search.addItem(self.cb_report_type, 1, 5, 1, 2)
        # 按钮
        lt_1 = QHBoxLayout()
        self.gp_where_search.addWidget(self.btn_query, 0, 7, 2, 2)
        self.gp_quick_search = QuickSearchGroup(1)
        lt_1.addWidget(self.gp_quick_search)
        lt_1.addWidget(self.btn_review_batch)
        lt_1.addWidget(self.btn_review_mode)
        lt_1.addWidget(self.btn_review_mode2)

        self.table_report_review_cols = OrderedDict([
            ('bgzt', '状态'),
            ('tjlx', '类型'),
            ('tjqy', '区域'),
            ('tjbh', '体检编号'),
            ('xm', '姓名'),
            ('xb', '性别'),
            ('nl', '年龄'),
            ('syrq','审阅日期'),
            ('syxm','审阅护士'),
            ('dwmc', '单位名称'),
            ('sybz', '审阅备注')
        ])
        # 待审阅列表
        self.table_report_review = ReportReviewTable(self.table_report_review_cols)
        self.gp_table = QGroupBox('审阅列表（0）')
        lt_table = QHBoxLayout()
        lt_table.addWidget(self.table_report_review)
        self.gp_table.setLayout(lt_table)
        # 审阅信息
        self.gp_review_user = ReportReviewUser()
        # 添加布局
        lt_left.addWidget(self.gp_where_search,1)
        lt_left.addLayout(lt_1,1)
        lt_left.addWidget(self.gp_table,7)
        lt_left.addWidget(self.gp_review_user,1)

        ####################右侧布局#####################
        self.wv_report_equip = WebView()
        # self.wv_report_page = self.wv_report_equip.page().mainFrame()
        # self.wv_report_page.setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)#去掉滑动条
        # self.wv_report_page.setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
        lt_right = QHBoxLayout()
        lt_right.addWidget(self.wv_report_equip)
        self.gp_right = QGroupBox('报告预览')
        self.gp_right.setLayout(lt_right)
        lt_main.addLayout(lt_left,1)
        lt_main.addWidget(self.gp_right,2)

        self.setLayout(lt_main)

# 报告审阅列表
class ReportReviewTable(TableWidget):

    tjqy = None  # 体检区域
    tjlx = None  # 体检类型
    cur_data_set = []

    def __init__(self, heads, parent=None):
        super(ReportReviewTable, self).__init__(heads, parent)
        self.table_where = None

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        self.cur_data_set = []
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            tmp = []
            self.insertRow(row_index)
            for col_index, col_value in enumerate(row_data):
                item = QTableWidgetItem(str2(col_value))
                tmp.append(str2(col_value))
                if col_index==0:
                    if str2(col_value)=='已审核':
                        item.setBackground(QColor("#FF0000"))
                    else:
                        item.setBackground(QColor("#f0e68c"))

                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)
            self.cur_data_set.append(tmp)
        # 布局
        self.setColumnWidth(0, 50)  # 状态
        self.setColumnWidth(1, 50)  # 类型
        self.setColumnWidth(2, 55)  # 区域
        self.setColumnWidth(3, 75)  # 体检编号
        self.setColumnWidth(4, 60)  # 姓名
        self.setColumnWidth(5, 40)  # 性别
        self.setColumnWidth(6, 40)  # 年龄
        self.setColumnWidth(7, 100) # 审阅日期
        self.setColumnWidth(8, 60)  # 审阅人
        self.setColumnWidth(9, 100)  # 单位名称
        self.horizontalHeader().setStretchLastSection(True)

    def add_query(self,where_str):
        self.table_where = where_str

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
        self.setStyleSheet('''border: 1px solid;font: 75 12pt \"微软雅黑\";''')
        self.setMinimumWidth(80)

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

class ReportReviewFullScreen(Dialog):

    # 自定义 信号，封装对外使用
    opened = pyqtSignal(list,int) #待审阅的数据，和当前开始审阅的索引

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
            mes_about(self, '当前是最后一份报告')

    def initData(self,datas,index):
        self.datas=datas
        self.cur_index=index
        self.open_page(datas[self.cur_index])
        # self.cur_index = self.cur_index + 1

    # 放射检查项目接收
    def on_btn_pic_click(self):
        pass

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
        lt_middle.addWidget(self.btn_pic)
        lt_middle.addStretch()
        lt_middle.addWidget(lable)
        lt_middle.addWidget(self.btn_auto_next)
        lt_middle.addWidget(self.btn_auto_print)
        lt_middle.addWidget(self.btn_auto_sms)
        # 报告预览
        self.wv_report_equip = WebView()
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
            # 发送短信
            if self.btn_sms_auto.isChecked():
                try:
                    result = self.session.query(MV_RYXX).filter(MV_RYXX.tjbh == self.cur_tjbh).scalar()
                    if result.sjhm:
                        sms_api(result.sjhm,report_sms_content)
                except Exception as e:
                    mes_about(self,"短信发送失败！错误信息：%s" %e)

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

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = ReportReviewUI()
    ui.show()
    app.exec_()