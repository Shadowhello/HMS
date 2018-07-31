from widgets.cwidget import *
from report.model import *
# 查看项目状态

class ItemsStateUI(Dialog):

    def __init__(self,tjbh=None,parent=None):
        super(ItemsStateUI,self).__init__(parent)
        self.setWindowTitle('项目查看')
        self.setMinimumHeight(600)
        self.initUI()
        if tjbh:
            results = self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,MT_TJ_TJJLMXB.sfzh=='1').all()
            self.table_item.load([result.item_result for result in results])

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
    def initDatas(self):
        pass



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = ItemsStateUI()
    ui.show()
    app.exec_()

