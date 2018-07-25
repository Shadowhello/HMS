from widgets.cwidget import *

class PacsResultUI(QDialog):

    def __init__(self,title,parent=None):
        super(PacsResultUI,self).__init__(parent)
        self.setWindowTitle(title)
        self.initUI()
        self.table_inspect.itemClicked.connect(self.on_table_refresh)
        self.painter = None

    def initUI(self):
        # self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setFixedSize(700,600)
        lt_main = QVBoxLayout()
        # 上 布局
        lt_top = QHBoxLayout()
        self.p_tjbh = QTJBH()
        self.btn_query = QPushButton(Icon('query'),'查询')
        self.btn_receive = QPushButton(Icon('接收'),'强制接收')
        lt_top.addWidget(QLabel('体检编号：'))
        lt_top.addWidget(self.p_tjbh)
        lt_top.addWidget(self.btn_query)
        lt_top.addWidget(self.btn_receive)

        lt_middle = QHBoxLayout()
        gp_middle = QGroupBox('检查列表')
        self.inspect_cols = OrderedDict([
            ('CBGZT', '报告状态'),
            ('SYSTYPE', '系统类别'),
            ('CMODALITY', '检查类别'),
            ('XMMC','项目名称'),
            ('CNAME','姓名'),
            ('CSEX', '性别'),
            ('CAGE', '年龄'),
            ('BGYS', '报告医生'),
            ('BGSJ', '报告时间'),
            ('SHYS', '审核医生'),
            ('SHSJ', '审核时间'),
            ('XMJG', '项目结果'),
            ('XMZD', '项目诊断'),
            ('CJCZT', '检查状态'),
            ('DDJSJ', '登记时间'),
            ('DCHECKDATE', '检查时间'),
            ('BGYSGH', '报告医生工号'),
            ('SHYSGH', '审核医生工号'),
            ('CACCNO', '影像号'),
            ('CBLKH', '顾客编号'),
            ('HISORDER_IID', '唯一码')
            ])
        self.table_inspect = PacsInspectResultTable(self.inspect_cols)
        self.table_inspect.setMinimumHeight(250)
        lt_middle.addWidget(self.table_inspect)
        gp_middle.setLayout(lt_middle)

        # 下 布局
        # lt_bottom = QVBoxLayout()
        # gp_bottom = QGroupBox()

        lt_bottom_1 = QHBoxLayout()
        gp_bottom_1 = QGroupBox('检查结论')
        self.pacs_zd = QLabel()
        lt_bottom_1.addWidget(self.pacs_zd)
        gp_bottom_1.setLayout((lt_bottom_1))

        lt_bottom_2 = QHBoxLayout()
        gp_bottom_2 = QGroupBox('检查结果')
        self.pacs_jg = QTextEdit()
        self.pacs_jg.setDisabled(True)
        self.pacs_jg.setStyleSheet("background:transparent;border-width:0;border-style:outset");
        lt_bottom_2.addWidget(self.pacs_jg)
        gp_bottom_2.setLayout((lt_bottom_2))

        lt_bottom_3 = QHBoxLayout()
        gp_bottom_3 = QGroupBox('检查信息')

        self.bgys = Lable()
        self.bgsj = Lable()
        self.shys = Lable()
        self.shsj = Lable()
        lt_bottom_3.addWidget(QLabel('报告医生：'))
        lt_bottom_3.addWidget(self.bgys)
        lt_bottom_3.addWidget(QLabel('报告时间：'))
        lt_bottom_3.addWidget(self.bgsj)
        lt_bottom_3.addWidget(QLabel('审核医生：'))
        lt_bottom_3.addWidget(self.shys)
        lt_bottom_3.addWidget(QLabel('审核时间：'))
        lt_bottom_3.addWidget(self.shsj)
        gp_bottom_3.setLayout(lt_bottom_3)
        lt_main.addLayout(lt_top)
        lt_main.addWidget(gp_middle)
        lt_main.addWidget(gp_bottom_1)
        lt_main.addWidget(gp_bottom_2)
        lt_main.addWidget(gp_bottom_3)

        # self.lb_bz = QLabel('测试文字',self)
        # self.lb_bz.setGeometry(50,50,200,200)
        # self.lb_bz.installEventFilter(self)  #这行不能省
        # # lt_main.addWidget(self.lb_bz)
        self.setLayout(lt_main)

    # def eventFilter(self, watched, QEvent):
    #     if watched ==self.lb_bz or QEvent.type() == QEvent.Paint:
    #         self.paint()
    #
    # def paint(self):
    #
    #     painter= QPainter(self.lb_bz)
    #     painter.setPen(Qt.blue)
    #     # // painter.drawLine(100, 100, 200, 200);
    #     painter.drawEllipse(30, 15, 50, 65)
    #     painter.drawLine(0, 100, 111, 100)

    def on_table_refresh(self,tableWidgetItem):
        row = tableWidgetItem.row()
        bgys = self.table_inspect.item(row, 7).text()
        bgrq = self.table_inspect.item(row, 8).text()
        shys = self.table_inspect.item(row, 9).text()
        shrq = self.table_inspect.item(row, 10).text()
        xmjg = self.table_inspect.item(row, 11).text()
        xmzd = self.table_inspect.item(row, 12).text()
        self.bgys.setText(bgys)
        self.bgsj.setText(bgrq)
        self.shys.setText(shys)
        self.shsj.setText(shrq)
        self.pacs_jg.setText(xmjg)
        self.pacs_zd.setText(xmzd)
        # self.update()

    def setData(self,datas):
        # 清空数据
        self.bgys.setText('')
        self.bgsj.setText('')
        self.shys.setText('')
        self.shsj.setText('')
        self.pacs_jg.setText('')
        self.pacs_zd.setText('')
        self.table_inspect.load(datas)

    # def paintEvent(self, QPaintEvent):
    #     # 先绘制父对象内容，
    #     super(PacsResultUI,self).paintEvent(QPaintEvent)
    #     # 再绘制自身
    #     painter = QPainter(self.lb_bz)
    #     # QPainter负责所有的绘制工作:在它的begin()与end()间放置了绘图代码。
    #     # 实际的绘制工作由drawText()方法完成。
    #     painter.begin(self.lb_bz)
    #     self.drawText(QPaintEvent, painter)
    #     painter.end()
    #
    # def drawText(self, QPaintEvent, painter):
    #     # 反走样
    #     painter.setRenderHint(QPainter.Antialiasing, True)
    #     # 设置画笔颜色、宽度
    #     painter.setPen(QPen(QColor(0, 160, 230), 2))
    #     # 设置画刷颜色
    #     painter.setBrush(QColor(255, 160, 90))
    #     painter.drawText(QRect(), Qt.AlignCenter, "测试文本啊！")

if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    ui = PacsResultUI('')
    ui.exec_()

