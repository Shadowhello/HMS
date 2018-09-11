from widgets.cwidget import *
from app_interface.model import *
from utils import cur_datetime

class PhoneUI(Dialog):

    # 自定义 信号，封装对外使用
    returnPressed = pyqtSignal(str,str)

    def __init__(self,parent=None):
        super(PhoneUI,self).__init__(parent)
        self.setWindowTitle('电话记录')
        self.setFixedSize(500,500)
        self.initUI()
        # 绑定信号槽
        self.returnPressed.connect(self.setData)
        self.le_tjbh.returnPressed.connect(self.on_le_tjbh_press)
        self.btn_see.clicked.connect(partial(self.on_le_tjbh_press,True))
        self.btn_add.clicked.connect(self.on_btn_add_click)

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_top = QHBoxLayout()
        gp_top = QGroupBox()
        lt_middle = QHBoxLayout()
        gp_middle = QGroupBox('电话记录列表')
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox('电话记录内容')
        self.le_tjbh = QTJBH()
        self.le_sjhm = QSJHM()
        self.btn_see = QPushButton(Icon('查询'), '查询')
        self.btn_add = QPushButton(Icon('新增'),'新增')
        # self.btn_edit = QPushButton(Icon('编辑'),'编辑')
        lt_top.addWidget(QLabel('体检编号：'))
        lt_top.addWidget(self.le_tjbh)
        lt_top.addWidget(QLabel('手机号码：'))
        lt_top.addWidget(self.le_sjhm)
        lt_top.addWidget(self.btn_see)
        lt_top.addWidget(self.btn_add)
        # lt_top.addWidget(self.btn_edit)
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
        lt_middle.addWidget(self.table_phone)
        gp_middle.setLayout(lt_middle)
        self.pt_phone_content = QPlainTextEdit()
        lt_bottom.addWidget(self.pt_phone_content)
        gp_bottom.setLayout(lt_bottom)
        lt_main.addWidget(gp_top)
        lt_main.addWidget(gp_middle)
        lt_main.addWidget(gp_bottom)

        self.setLayout(lt_main)

    def on_btn_add_click(self):
        sjhm = self.le_sjhm.text()
        content = self.pt_phone_content.toPlainText()
        if all([sjhm,content]):
            data1_obj = {
                'jllx': '0080', 'jlmc': '0080', 'tjbh': self.le_tjbh.text(), 'mxbh': sjhm, 'czgh': self.login_id,
                'czxm': self.login_name,'czqy': self.login_area, 'jlnr': content, 'bz': None
            }
            data2_obj = {
                'tjbh': self.le_tjbh.text(),
                'jllx': 1,
                'jlnr': content,
                'jlr': self.login_name,
                'jlsj': cur_datetime()
            }
            try:
                self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data1_obj])
                self.session.bulk_insert_mappings(MT_TJ_DHGTJLB, [data2_obj])
                self.session.commit()

            except Exception as e:
                self.session.rollback()
                mes_about(self, "执行数据库出错！错误信息：%s" % e)
                return
            mes_about(self, '记录成功！')
            self.on_le_tjbh_press()
        else:
            mes_about(self,'手机号码与记录内容不能为空！')

    # 设置体检编号值
    def setData(self,p1_str,p2_str):
        self.le_tjbh.setText(p1_str)
        self.le_sjhm.setText(p2_str)
        self.on_le_tjbh_press()

    # 查询
    def on_le_tjbh_press(self,is_mes=False):
        if not self.le_tjbh.text():
            mes_about(self,'请输入体检编号！')
            return
        results = self.session.query(MT_TJ_DHGTJLB).filter(MT_TJ_DHGTJLB.tjbh == self.le_tjbh.text()).all()
        self.table_phone.load([result.to_dict for result in results])
        if is_mes:
            mes_about(self,'检索出 %s 条数据！' %self.table_phone.rowCount())

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = PhoneUI()
    ui.show()
    app.exec_()



