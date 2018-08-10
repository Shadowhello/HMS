from widgets.cwidget import *
from report.model import *
# 查看项目状态

class ItemsStateUI(Dialog):

    # 自定义 信号，封装对外使用
    returnPressed = pyqtSignal(str)

    def __init__(self,parent=None):
        super(ItemsStateUI,self).__init__(parent)
        self.setWindowTitle('项目查看')
        self.setMinimumHeight(600)
        self.initUI()
        # 绑定信号槽
        self.returnPressed.connect(self.setDatas)
        self.le_tjbh.returnPressed.connect(self.on_le_tjbh_press)

    def initUI(self):
        self.item_cols = OrderedDict(
            [
                ("state","状态"),
                ("ksbm", "科室编号"),
                ("xmbh", "项目编号"),
                ("xmmc", "项目名称"),
                ("btn_dy", ""),
                ("btn_jj", ""),
                ("btn_hs", "")
             ])
        lt_main = QVBoxLayout()
        # 搜索
        self.le_tjbh = QTJBH()
        # 用户基本信息
        self.gp_user = UserBaseGroup()
        self.table_item = ItemsStateTable(self.item_cols)
        self.table_item.setAlternatingRowColors(False)                       # 使用行交替颜色
        lt_main.addWidget(self.le_tjbh)
        lt_main.addWidget(self.gp_user)
        lt_main.addWidget(self.table_item)
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
        results = self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == self.le_tjbh.text(),MT_TJ_TJJLMXB.sfzh=='1').all()
        self.table_item.load([result.item_result for result in results])

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = ItemsStateUI()
    ui.show()
    app.exec_()

