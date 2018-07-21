from widgets.cwidget import *
from lis.model import *
from utils.buildbarcode import BarCodeBuild
# 留样

class CollectUrine_UI(Widget):

    def __init__(self):

        super(CollectUrine_UI,self).__init__()
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        ####################左边布局#####################################
        gp_left = QGroupBox()
        lt_left = QVBoxLayout()
        lt_left_top = QHBoxLayout()
        self.lt_left_bottom = QGridLayout()
        gp_left_bottom = QGroupBox('留样详情')
        gp_left_bottom.setLayout(self.lt_left_bottom)

        label = QLabel('条码号：')
        self.tmbh = QSerialNo()
        self.tmbh.setFixedHeight(200)
        self.tmbh.setFont(QFont("微软雅黑" , 50,  QFont.Bold))
        label.setFont(QFont("微软雅黑" , 50,  QFont.Bold))
        self.urine_cols = OrderedDict([
                                ("cjzt", ""),
                                ("tmbh", "条码号"),
                                ("tjbh","体检编号"),
                                ("xmhz", "条码项目")
                            ])
        self.table_urine = TableWidget(self.urine_cols)
        self.table_urine.verticalHeader().setVisible(False)  # 去掉行头


        lt_left_top.addWidget(label)
        lt_left_top.addWidget(self.tmbh)

        lt_left.addLayout(lt_left_top)
        lt_left.addWidget(gp_left_bottom)

        gp_left.setLayout(lt_left)
        ############################ 布局右边 ############################
        self.gp_right = QGroupBox('留样扫码')
        lt_right = QVBoxLayout()
        lt_right.addWidget(self.table_urine)
        self.gp_right.setLayout(lt_right)
        main_layout.addWidget(gp_left)
        main_layout.addWidget(self.gp_right)

        self.setLayout(main_layout)
