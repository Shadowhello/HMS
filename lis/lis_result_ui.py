from widgets.cwidget import *

class LisResultUI(QDialog):

    def __init__(self):
        super(LisResultUI,self).__init__()
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
        self.inspect_master_cols = OrderedDict([
                        ('bgzt','报告状态'),
                        ('xmmc','项目名称'),
                        ('bgys', '报告医生'),
                        ('bgsj', '报告时间'),
                        ('shys', '审核医生'),
                        ('shsj', '审核时间'),
                        ('djsj', '登记时间'),
                        ('jczt', '检查状态'),
                     ])
        self.inspect_detail_cols = OrderedDict([
                        ('bgzt', '项目状态'),
                        ('xmbh', '项目编号'),
                        ('xmmc', '项目名称'),
                        ('xmjg', '项目结果')
                     ])
        self.table_inspect_master = LisInspectResultTable(self.inspect_master_cols)
        self.table_inspect_detail = LisInspectResultTable(self.inspect_detail_cols)

        lt_middle.addWidget(self.table_inspect_master)
        lt_middle.addWidget(self.table_inspect_detail)
        gp_middle.setLayout(lt_middle)

        # 下 布局
        # lt_bottom = QVBoxLayout()
        # gp_bottom = QGroupBox()
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox('检查信息')

        self.bgys = Lable()
        self.bgsj = Lable()
        self.shys = Lable()
        self.shsj = Lable()
        lt_bottom.addWidget(QLabel('报告医生：'))
        lt_bottom.addWidget(self.bgys)
        lt_bottom.addWidget(QLabel('报告时间：'))
        lt_bottom.addWidget(self.bgsj)
        lt_bottom.addWidget(QLabel('审核医生：'))
        lt_bottom.addWidget(self.shys)
        lt_bottom.addWidget(QLabel('审核时间：'))
        lt_bottom.addWidget(self.shsj)
        gp_bottom.setLayout(lt_bottom)
        lt_main.addLayout(lt_top)
        lt_main.addWidget(gp_middle)
        lt_main.addWidget(gp_bottom)
        self.setLayout(lt_main)




if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    ui = LisResultUI()
    ui.exec_()

