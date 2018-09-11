from widgets.cwidget import *
from report.model import *
# 查看项目状态

class ItemsStateUI(Dialog):

    # 自定义 信号，封装对外使用
    returnPressed = pyqtSignal(str)

    def __init__(self,parent=None):
        super(ItemsStateUI,self).__init__(parent)
        self.setWindowTitle('项目查看')
        self.setMinimumHeight(500)
        self.initUI()
        # 绑定信号槽
        self.returnPressed.connect(self.setDatas)
        self.le_tjbh.returnPressed.connect(self.on_le_tjbh_press)
        self.btn_query.clicked.connect(self.on_le_tjbh_press)

    def initUI(self):
        self.item_cols = OrderedDict(
            [
                ("state","状态"),
                ("xmbh", "项目编号"),
                ("xmmc", "项目名称"),
                ("ksmc", "科室名称"),
                ("jcrq", "检查日期"),
                ("jcys", "检查医生"),
                ("shrq", "审核日期"),
                ("shys", "审核医生"),
                ("tmbh", "条码号"),
                ("btn_name", "")
             ])
        lt_main = QVBoxLayout()
        # 搜索
        lt_top = QHBoxLayout()
        self.le_tjbh = QTJBH()
        self.btn_query = QPushButton(Icon('query'),'查询')
        gp_top = QGroupBox()
        lt_top.addWidget(QLabel('体检编号：'))
        lt_top.addWidget(self.le_tjbh)
        lt_top.addWidget(self.btn_query)
        lt_top.addStretch()
        gp_top.setLayout(lt_top)
        lt_middle = QHBoxLayout()
        self.gp_middle = QGroupBox('项目状态')
        # 用户基本信息
        self.gp_user = UserBaseGroup()
        self.table_item = ItemsStateTable(self.item_cols)
        self.table_item.setAlternatingRowColors(False)                       # 使用行交替颜色
        self.table_item.verticalHeader().setVisible(False)
        lt_middle.addWidget(self.table_item)
        self.gp_middle.setLayout(lt_middle)

        lt_main.addWidget(gp_top)
        lt_main.addWidget(self.gp_user)
        lt_main.addWidget(self.gp_middle)
        self.setLayout(lt_main)

    # 初始化数据
    def setDatas(self,p_str):
        self.le_tjbh.setText(p_str)
        self.on_le_tjbh_press()

    # 查询
    def on_le_tjbh_press(self):
        if not self.le_tjbh.text():
            mes_about(self,'请输入体检编号！')
            return
        # 人员信息
        result = self.session.query(MV_RYXX).filter(MV_RYXX.tjbh == self.le_tjbh.text()).scalar()
        if result:
            self.gp_user.setData(result.to_dict)
        else:
            mes_about(self,'不存在，请确认后重新输入！')
            self.gp_user.clearData()
        # 项目结果
        #results = self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == self.le_tjbh.text(),MT_TJ_TJJLMXB.sfzh=='1').all()
        #self.table_item.load([result.item_result for result in results])
        results = self.session.execute(get_item_state_sql(tjbh=self.le_tjbh.text())).fetchall()
        self.table_item.load(results)
        self.gp_middle.setTitle('项目状态 (%s)' %self.table_item.rowCount())

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = ItemsStateUI()
    ui.show()
    app.exec_()

