from widgets.cwidget import *

class LisResultUI(QDialog):

    def __init__(self,title,parent=None):
        super(LisResultUI,self).__init__(parent)
        self.setWindowTitle(title)
        self.initUI()
        self.table_inspect_master.itemClicked.connect(self.on_table_show_detail)
        # 右侧详细结果 字典
        self.detail_datas = None

    def initUI(self):
        #self.setWindowFlags(Qt.WindowCloseButtonHint)
        # self.setFixedSize(700,500)
        self.setMinimumHeight(500)
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
                        ('bgzt', '状态'),
                        ('tmbh', '条码编号'),
                        ('xmhz', '条码项目'),
                        ('jcys', '检验医生'),
                        ('jcsj', '检验时间'),
                        ('shys', '审核医生'),
                        ('shsj', '审核时间'),
                        ('tjbh', '体检编号')
                     ])
        self.inspect_detail_cols = OrderedDict([
                        ('xmbh', '项目编号'),
                        ('xmmc', '项目名称'),
                        ('xmjg', '项目结果'),
                        ('xmzt', '项目状态'),
                        ('ckfw', '参考范围'),
                        ('xmdw', '项目单位')

                     ])
        self.table_inspect_master = MLisInspectResultTable(self.inspect_master_cols)
        self.table_inspect_detail = DLisInspectResultTable(self.inspect_detail_cols)
        self.table_inspect_detail.setMinimumWidth(480)
        self.table_inspect_detail.resizeColumnsToContents()  # 设置列适应大小

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
        lt_bottom.addWidget(QLabel('检验医生：'))
        lt_bottom.addWidget(self.bgys)
        lt_bottom.addWidget(QLabel('检验时间：'))
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

    def setData(self,datas):
        # 清空数据
        self.bgys.setText('')
        self.bgsj.setText('')
        self.shys.setText('')
        self.shsj.setText('')
        #self.pacs_jg.setText('')
        #self.pacs_zd.setText('')
        self.table_inspect_master.load(datas['pes'])
        self.detail_datas = datas['lis']

    #单击主的 出来子的
    def on_table_show_detail(self,tableWidgetItem):
        row = tableWidgetItem.row()
        tjtm = self.table_inspect_master.item(row,7).text()+self.table_inspect_master.item(row,1).text()
        self.table_inspect_detail.load(self.detail_datas.get(tjtm,[]))
        bgys = self.table_inspect_master.item(row, 3).text()
        bgrq = self.table_inspect_master.item(row, 4).text()
        shys = self.table_inspect_master.item(row, 5).text()
        shrq = self.table_inspect_master.item(row, 6).text()
        self.bgys.setText(bgys)
        self.bgsj.setText(bgrq)
        self.shys.setText(shys)
        self.shsj.setText(shrq)




if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    ui = LisResultUI('检验')
    ui.exec_()

