from widgets.cwidget import *
from app_interface.model import *

class PhoneUI(Dialog):

    # 自定义 信号，封装对外使用
    returnPressed = pyqtSignal(str)

    def __init__(self,parent=None):
        super(PhoneUI,self).__init__(parent)
        self.setWindowTitle('电话记录')
        self.setFixedSize(500,500)
        self.initUI()
        # 绑定信号槽
        self.returnPressed.connect(self.setData)
        self.le_tjbh.returnPressed.connect(self.on_le_tjbh_press)
        self.btn_see.clicked.connect(self.on_le_tjbh_press)

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_top = QHBoxLayout()
        gp_top = QGroupBox()
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox('电话记录列表')
        self.le_tjbh = QTJBH()
        self.btn_see = QPushButton(Icon('查询'), '查询')
        self.btn_add = QPushButton(Icon('新增'),'新增')
        self.btn_edit = QPushButton(Icon('编辑'),'编辑')
        lt_top.addWidget(self.le_tjbh)
        lt_top.addWidget(self.btn_see)
        lt_top.addWidget(self.btn_add)
        lt_top.addWidget(self.btn_edit)
        lt_top.addStretch()
        gp_top.setLayout(lt_top)
        ###############################################
        self.table_phone_cols = OrderedDict(
            [
                ("tjbh", "体检编号"),
                ("jllx", "记录类型"),
                ("jlr", "记录人"),
                ("jlsj", "记录时间"),
                ("jlnr", "记录内容"),
             ])
        self.table_phone = PhoneTable(self.table_phone_cols)
        lt_bottom.addWidget(self.table_phone)
        gp_bottom.setLayout(lt_bottom)
        lt_main.addWidget(gp_top)
        lt_main.addWidget(gp_bottom)
        # lt_main.addStretch()

        self.setLayout(lt_main)

    # 设置体检编号值
    def setData(self,p_str):
        self.le_tjbh.setText(p_str)
        self.on_le_tjbh_press()

    # 查询
    def on_le_tjbh_press(self):
        if not self.le_tjbh.text():
            mes_about(self,'请输入体检编号！')
            return
        results = self.session.query(MT_TJ_DHGTJLB).filter(MT_TJ_DHGTJLB.tjbh == self.le_tjbh.text()).all()
        self.table_phone.load([result.to_dict for result in results])

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = PhoneUI()
    ui.show()
    app.exec_()



