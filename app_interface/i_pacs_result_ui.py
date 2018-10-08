from widgets.cwidget import *

class PacsResultUI(PacsDialog):

    def __init__(self,title,parent=None):
        super(PacsResultUI,self).__init__(parent)
        self.setWindowTitle(title)
        self.initUI()

    def initUI(self):
        # self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setFixedSize(700,600)
        lt_main = QVBoxLayout()
        # 上 布局
        lt_top = QHBoxLayout()
        self.p_tjbh = QTJBH()
        self.btn_query = QPushButton(Icon('query'),'查询')
        self.btn_receive = QPushButton(Icon('接收'),'强制接收')
        lt_top.addStretch()
        # lt_top.addWidget(QLabel('体检编号：'))
        # lt_top.addWidget(self.p_tjbh)
        # lt_top.addWidget(self.btn_query)
        lt_top.addWidget(self.btn_receive)

        lt_middle = QHBoxLayout()
        gp_middle = QGroupBox('检查列表')
        self.inspect_cols = OrderedDict([
            ('CBGZT', '报告状态'),
            ('CJCZT', '检查状态'),
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
        self.shgh = Lable()         #隐藏
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

        self.lb_bz = StateLable(gp_bottom_2)
        self.lb_bz.show()
        self.setLayout(lt_main)

class StateLable(QLabel):

    def __init__(self,parent):
        super(StateLable,self).__init__(parent)
        self.setMinimumSize(200,200)
        self.setGeometry(400,-40,100,100)
        self.setStyleSheet('''font: 75 28pt "微软雅黑";color: rgb(255, 0, 0);''')
        self.setAttribute(Qt.WA_TranslucentBackground)                               #背景透明
        self.data = open(file_ico('已审核.png'),'rb').read()

    def show2(self,flag = True):
        if flag:
            p = QPixmap()
            p.loadFromData(self.data)
            self.setPixmap(p)
        else:
            self.clear()





if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    ui = PacsResultUI('')
    ui.exec_()

