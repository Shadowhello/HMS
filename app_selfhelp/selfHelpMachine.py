from widgets.cwidget import *
from .model import *
from report.model import MT_TJ_BGGL
from utils import gol,print_pdf_gsprint,pdfSplit
from utils.api import request_get


# 自助机
class SelfHelpMachine(Widget):

    def __init__(self,parent=None):
        super(SelfHelpMachine,self).__init__(parent)
        # 载入样式
        self.stylesheet = file_style(gol.get_value('file_qss', 'mztj.qss'))
        with open(self.stylesheet) as f:
            self.setStyleSheet(f.read())
        self.setWindowTitle('明州体检')
        self.setWindowIcon(Icon('mztj'))
        self.initUI()
        self.setBackgroundImage()
        # 绑定信号槽
        self.le_tjbh.returnPressed.connect(self.on_le_tjbh_press)
        self.btn_sfz.clicked.connect(self.on_btn_sfz_read)
        self.btn_keyboard.clicked.connect(self.on_btn_keyboard_click)
        # 右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单
        # 特殊变量
        self.gp_keyboard = None       #键盘区域
        self.print_thread = None
        self.dg_p = None              #进度窗口，温馨提示
        self.pd_ui_num = 0

    def initUI(self):
        lt_main = QHBoxLayout(self)
        lt_top = QHBoxLayout()
        lt_middle1 = QHBoxLayout()
        lt_middle2 = QHBoxLayout()
        lt_middle3 = QHBoxLayout()
        lt_middle = QHBoxLayout()
        lt_bottom = QHBoxLayout()
        self.le_tjbh = QSFZH()
        self.le_tjbh.setMinimumWidth(400)
        self.le_tjbh.setFixedHeight(175)
        self.le_tjbh.setStyleSheet('''font: 75 50pt \"微软雅黑\";''')
        self.btn_keyboard = ToolButton(Icon('键盘'),'')
        self.btn_keyboard.setIconSize(QSize(120,120))
        self.btn_keyboard.setObjectName("toolB")
        self.btn_sfz = ToolButton(Icon('身份证'),'读身份证')
        self.btn_sfz.setIconSize(QSize(120,120))
        self.btn_sfz.setObjectName("toolB")
        lt_middle2.addWidget(self.le_tjbh)
        lt_middle2.addWidget(self.btn_keyboard)
        lt_middle2.addWidget(self.btn_sfz)
        # lt_middle.addStretch()
        lt_middle.addLayout(lt_middle2)
        # lt_middle.addStretch()
        # 添加布局
        lt_main.addStretch()
        lt_main.addLayout(lt_middle,1)
        lt_main.addStretch()
        self.setLayout(lt_main)
        self.table_user_cols = OrderedDict([
            ('tjbh', '体检编号'),
            ('xm', '姓名'),
            ('xb', '性别'),
            ('nl', '年龄'),
            ('sfzh', '身份证号'),
            ('sjhm', '手机号码'),
            ('qdrq', '体检日期'),
            ('shrq', '审核日期'),
            ('ck', '')
        ])
        self.table_user = UserTable(self.table_user_cols)

    def setBackgroundImage(self):
        palette=QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(file_ico("mztjbj.jpg"))))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    # 扫描体检编号或者手工输入回车
    def on_le_tjbh_press(self):
        if len(self.le_tjbh.text())==9:
            mes_about(self, '请输入正确的身份证号！')
            # self.on_print_thread(self.le_tjbh.text())
            # self.dg_p = ProgressDialog(self)
            # self.dg_p.show()
        elif len(self.le_tjbh.text())==18:
            results = self.session.execute(get_report_detail_sql(self.le_tjbh.text())).fetchall()
            if results:
                try:
                    self.on_print_thread(results[0][0])
                    # 键盘区域存在则隐藏
                    if self.gp_keyboard:
                        if not self.gp_keyboard.isHidden():
                            self.gp_keyboard.hide()
                    self.dg_p = ProgressDialog(self)
                    self.dg_p.show()
                except Exception as e:
                    mes_about(self,'数据获取失败！请联系管理员！')

        else:
            mes_about(self,'请输入正确的身份证号！')

        self.le_tjbh.setText('')

    # 右键功能
    def onTableMenu(self,pos):
        menu = QMenu()
        item1 = menu.addAction(Icon("退出"), "退出")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == item1:
            button = mes_warn(self, '您确认退出吗？')
            if button == QMessageBox.Yes:
                self.close()

    def on_print_thread(self,p_str):
        if self.print_thread:
            self.print_thread.setData(p_str)
            self.print_thread.signalPost.connect(self.on_mes_show, type=Qt.QueuedConnection)
            self.print_thread.start()
        else:
            self.print_thread = PrintThread(self.session)
            self.print_thread.setData(p_str)
            self.print_thread.signalPost.connect(self.on_mes_show, type=Qt.QueuedConnection)
            self.print_thread.start()

    # 消息提示
    def on_mes_show(self,p_bool:bool,mes:str,num:int):
        if self.pd_ui_num == num:
            return
        else:
            self.pd_ui_num = num
        if self.dg_p:
            if not self.dg_p.isHidden():
                self.dg_p.hide()
        # mes_about(self,mes)
        MessageBox(self, text=mes).exec_()
        self.le_tjbh.setText('')

    # 读身份证号
    def on_btn_sfz_read(self):
        # 键盘区域存在则隐藏
        if self.gp_keyboard:
            if not self.gp_keyboard.isHidden():
                self.gp_keyboard.hide()
        dialog = ReadChinaIdCard_UI(self)
        dialog.sendIdCard.connect(self.setData)
        dialog.exec_()

    # 读取后设置身份证号
    def setData(self,idCard:str,xm:str):
        # 设置身份证号
        self.le_tjbh.setText(idCard)
        # 检索
        self.on_le_tjbh_press()

    # 数字小键盘，用于手工输入内容
    def on_btn_keyboard_click(self):
        # 不存在 则新建
        if not self.gp_keyboard:
            self.gp_keyboard = QGroupBox(self)
            rect=self.le_tjbh.geometry()
            width = rect.width()
            bottom = rect.bottom()
            left = rect.left()
            # 数字 字母 中文
            btn_names = ['1','2','3','4','5','6','7','8','9','','0','X','ESC','<- 退回','搜索']
            # 一行几个按钮
            size = 3
            height = 400

            lt_keyboard = QGridLayout()
            for i,btn_name in enumerate(btn_names):
                # 获取坐标
                btn_pos_x = i // size
                btn_pos_y = i % size
                btn_obj = QPushButton(btn_name)
                btn_obj.setMinimumWidth(width//10)
                btn_obj.setFixedHeight(height//4)
                btn_obj.setStyleSheet('''font: 75 28pt \"微软雅黑\";''')
                # 添加布局
                btn_obj.clicked.connect(partial(self.on_btn_obj_click,btn_name))
                lt_keyboard.addWidget(btn_obj, btn_pos_x, btn_pos_y, 1, 1)

            lt_keyboard.setHorizontalSpacing(10)               # 设置水平间距
            lt_keyboard.setVerticalSpacing(10)                 # 设置垂直间距
            lt_keyboard.setContentsMargins(10, 10, 10, 10)     # 设置外间距
            #lt_keyboard.setColumnStretch(5, 1)                 # 设置列宽，添加空白项的

            self.gp_keyboard.setLayout(lt_keyboard)
            self.gp_keyboard.setGeometry(QRect(left,bottom,width,height))
            self.gp_keyboard.show()
        else:
            if self.gp_keyboard.isHidden():
                self.gp_keyboard.show()
            else:
                # 再次点击 则隐藏
                self.gp_keyboard.hide()

    # 数字键盘信号槽
    def on_btn_obj_click(self,btn_name):
        if btn_name=='ESC':
            self.gp_keyboard.hide()
        elif btn_name=='搜索':
            # 先隐藏
            self.gp_keyboard.hide()
            # 后检索
            self.on_le_tjbh_press()
        elif btn_name=='<- 退回':
            self.le_tjbh.setText(self.le_tjbh.text()[:-1])
        else:
            self.le_tjbh.setText(self.le_tjbh.text()+btn_name)

# 打印线程
class PrintThread(QThread):

    # 定义信号,定义参数为str类型
    signalMes = pyqtSignal(str)          # 消息反馈
    signalPost = pyqtSignal(bool,str,int)        # 消息反馈
    signalExit = pyqtSignal()

    def __init__(self,session):
        super(PrintThread,self).__init__()
        self.session = session
        self.runing = False
        self.tjbh = None
        self.num = 1

    def stop(self):
        self.runing = False

    def setData(self,p_str):
        self.tjbh =p_str
        self.runing = True

    def run(self):
        while self.runing:
            if self.tjbh:
                url = gol.get_value('api_report_down',None) %self.tjbh
                filename = os.path.join(gol.get_value('path_tmp'),'%s.pdf' %self.tjbh)
                filename_xdt = os.path.join(gol.get_value('path_tmp'), '%s_08.pdf' % self.tjbh)
                if os.path.exists(filename):
                    os.remove(filename)
                if os.path.exists(filename_xdt):
                    os.remove(filename_xdt)
                if url:
                    if request_get(url,filename):
                        # 2018-09-27 特别处理 真心蛋疼
                        # 这里需要判断是否是老的，老的PDF心电图是横向的，直接打印有问题
                        # 如果是老的 需要拆分PDF，并且将心电图PDF 旋转90度
                        result = self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == self.tjbh,MT_TJ_BGGL.bgzt == '2').scalar()
                        if result:
                            # 新报告模式
                            if print_pdf_gsprint(filename) == 0:
                                self.signalPost.emit(True, '打印成功！',self.num)
                            else:
                                self.signalPost.emit(False, '打印失败！',self.num)
                        else:
                            #老报告模式，判断是否有心电图
                            result = self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == self.tjbh,MT_TJ_TJJLMXB.xmbh == '0806').scalar()
                            if result:
                                page_num = pdfSplit(filename,filename_xdt)
                                if page_num>0:
                                    print_pdf_gsprint(filename, page_end=page_num)
                                    if print_pdf_gsprint(filename_xdt) == 0:
                                        self.signalPost.emit(True, '打印成功！', self.num)
                                    else:
                                        self.signalPost.emit(False, '打印失败！', self.num)
                                else:
                                    self.signalPost.emit(False, '报告打印存在问题，请联系管理员！', self.num)

                            else:
                                if print_pdf_gsprint(filename) == 0:
                                    self.signalPost.emit(True, '打印成功！', self.num)
                                else:
                                    self.signalPost.emit(False, '打印失败！', self.num)

                        # try:
                        #     win32api.ShellExecute(0, 'print', filename,self.printer , '.', 0)
                        #     time.sleep(2)
                        #     self.signalPost.emit(True,'打印成功！')
                        # except Exception as e:
                        #     self.signalPost.emit(False,'打印失败！错粗信息：%s \n 处理方式：请安装PDF阅读器 AcroRd32.exe 并设置为默认打开方式。' %e)
                    else:
                        self.signalPost.emit(False,'未找到您的报告！',self.num)

                else:
                    self.signalPost.emit(False,'请联系管理员配置节点：api_pdf_old_down')
            self.num = self.num + 1
            self.stop()


# 进度动态图
class ProgressDialog(Dialog):

    def __init__(self,parent):
        super(ProgressDialog,self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 窗口模式，去掉标题栏
        self.setFixedSize(700,700)
        lt_main = QVBoxLayout()
        lb_p = QLabel()
        lb_dec = QLabel('正在查找打印，请您稍等！')
        lb_dec.setStyleSheet('''font: 75 40pt \"微软雅黑\";''')
        movie = QMovie(file_ico('35.gif'))
        lb_p.setMovie(movie)
        movie.start()
        # 用于控件移动居中 不考虑任务与考虑任务栏
        # move((desktop->width() - this->width()) / 2, (desktop->height() - this->height()) / 2);
        # self.move((qApp.desktop().availableGeometry().width() - self.width()) / 2 + qApp.desktop().availableGeometry().x(),
        #           (qApp.desktop().availableGeometry().height() - self.height()) / 2 + qApp.desktop().availableGeometry().y()
        #           )
        lt_main.addWidget(lb_p)
        lt_main.addWidget(lb_dec)
        self.setLayout(lt_main)


class UserTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(UserTable, self).__init__(heads, parent)
        self.setStyleSheet('''QHeaderView{font-size:28px;}QTableView::item {font-size:20px;}''')

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # list 实现
        for row_index, row_data in enumerate(datas):
            # 插入一行
            self.insertRow(row_index)
            for col_index, col_value in enumerate(row_data):
                if col_index in [1,2]:
                    item = QTableWidgetItem(str2(col_value))
                else:
                    item = QTableWidgetItem(col_value)
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

            self.setColumnWidth(0, 80)
            self.setColumnWidth(1, 70)
            self.setColumnWidth(2, 70)
            self.setColumnWidth(3, 80)
            self.setColumnWidth(4, 150)
            self.setColumnWidth(5, 90)
            # self.horizontalHeader().setStretchLastSection(True)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = SelfHelpMachine()
    ui.showMaximized()
    app.exec_()
