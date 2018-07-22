from widgets.cwidget import *

class PacsResultUI(QDialog):

    def __init__(self):
        super(PacsResultUI,self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setFixedSize(600,500)
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
            ('bgzt','报告状态'),
            ('xmmc','项目名称'),
            ('bgys', '报告医生'),
            ('bgsj', '报告时间'),
            ('shys', '审核医生'),
            ('shsj', '审核时间'),
            ('djsj', '登记时间'),
            ('jczt', '检查状态'),
            ])
        self.table_inspect = PacsInspectResultTable(self.inspect_cols)

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
        self.setLayout(lt_main)


if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    ui = PacsResultUI()
    ui.exec_()

