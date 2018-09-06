from widgets.cwidget import *
from widgets.bweb import *

class ReportEquipUI(Widget):

    def __init__(self,parent=None):
        super(ReportEquipUI,self).__init__(parent)
        self.initUI()

    def initUI(self):
        lt_main = QHBoxLayout()
        lt_left = QVBoxLayout()
        self.btn_query = ToolButton(Icon('query'), '查询')
        self.gp_where_search = BaseCondiSearchGroup(1)
        self.gp_where_search.setNoChoice()
        # 报告状态
        self.cb_report_state = ReportStateGroup()
        self.cb_report_state.addStates(['所有','未审核','已审核'])
        self.cb_equip_type = EquipTypeLayout()
        self.cb_user = UserGroup('检查医生：')
        self.cb_user.addUsers(['所有',self.login_name])
        # 区域
        self.cb_area = AreaGroup()
        self.gp_where_search.addItem(self.cb_area, 0, 3, 1, 2)
        self.gp_where_search.addItem(self.cb_report_state, 1, 3, 1, 2)
        self.gp_where_search.addItem(self.cb_user, 0, 5, 1, 2)
        self.gp_where_search.addItem(self.cb_equip_type, 1, 5, 1, 2)
        # 按钮
        self.gp_where_search.addWidget(self.btn_query, 0, 7, 2, 2)
        self.gp_quick_search = QuickSearchGroup()
        self.gp_quick_search.setLabelDisable('sfzh')
        self.gp_quick_search.setLabelDisable('sjhm')
        self.table_report_equip_cols = OrderedDict([
            ('ename', '设备名称'),
            ('tjbh', '体检编号'),
            ('patient', '姓名'),
            ('jcrq','检查日期'),
            ('jcys','检查医生'),
            ('jcqy', '检查区域'),
            ('fpath', '文件路径')
        ])
        # 待审阅列表
        self.table_report_equip = ReportEquipTable(self.table_report_equip_cols)
        self.gp_table = QGroupBox('检查完成列表（0）')
        lt_table = QHBoxLayout()
        lt_table.addWidget(self.table_report_equip)
        self.gp_table.setLayout(lt_table)
        # 审阅信息
        self.gp_review_user = ReportEquipUser()
        # 添加布局
        lt_left.addWidget(self.gp_where_search,1)
        lt_left.addWidget(self.gp_quick_search,1)
        lt_left.addWidget(self.gp_table,7)
        lt_left.addWidget(self.gp_review_user,1)

        ####################右侧布局#####################
        self.wv_report_equip = WebView()
        lt_right = QHBoxLayout()
        lt_right.addWidget(self.wv_report_equip)
        gp_right = QGroupBox('报告预览')
        gp_right.setLayout(lt_right)
        lt_main.addLayout(lt_left,1)
        lt_main.addWidget(gp_right,2)

        self.setLayout(lt_main)

# 报告审阅列表
class ReportEquipTable(TableWidget):

    tjqy = None  # 体检区域
    tjlx = None  # 体检类型

    def __init__(self, heads, parent=None):
        super(ReportEquipTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # 字典载入
        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)                # 插入一行
            for col_index, col_name in enumerate(heads.keys()):
                item = QTableWidgetItem(row_data[col_name])
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)
        # 布局
        self.setColumnWidth(0, 70)  # 设备名称
        self.setColumnWidth(1, 70)  # 体检编号
        self.setColumnWidth(2, 50)  # 姓名
        self.setColumnWidth(3, 80)  # 检查日期
        self.setColumnWidth(4, 70)  # 检查姓名
        self.setColumnWidth(5, 100) # 检查区域
        self.horizontalHeader().setStretchLastSection(True)

class ReportEquipUser(QGroupBox):

    # 自定义 信号，封装对外使用
    btnClick = pyqtSignal(bool,int)

    def __init__(self):
        super(ReportEquipUser,self).__init__()
        self.initUI()
        self.btn_audit.clicked.connect(self.on_btn_audit_click)

    def initUI(self):
        self.setTitle('审核信息')
        lt_main = QGridLayout()
        self.al_audit_user = AuditLabel()
        self.al_audit_time = AuditLabel()
        self.al_audit_content = QPlainTextEdit()
        self.al_audit_content.setStyleSheet('''font: 75 12pt '微软雅黑';color: rgb(255,0,0);height:20px;''')
        self.btn_audit = ToolButton(Icon('样本签收'),'取消审核')
        ###################基本信息  第一行##################################
        lt_main.addWidget(QLabel('审核者：'), 0, 0, 1, 1)
        lt_main.addWidget(self.al_audit_user, 0, 1, 1, 1)
        lt_main.addWidget(QLabel('审核时间：'), 1, 0, 1, 1)
        lt_main.addWidget(self.al_audit_time, 1, 1, 1, 1)
        # 按钮
        lt_main.addWidget(self.btn_audit, 0, 9, 2, 2)
        ###################基本信息  第二行##################################
        # lt_main.addWidget(QLabel('审阅备注：'), 0, 2, 2, 2)
        lt_main.addWidget(self.al_audit_content, 0, 2, 2, 7)

        lt_main.setHorizontalSpacing(10)            #设置水平间距
        lt_main.setVerticalSpacing(10)              #设置垂直间距
        lt_main.setContentsMargins(10, 10, 10, 10)  #设置外间距
        lt_main.setColumnStretch(6, 1)             #设置列宽，添加空白项的
        self.setLayout(lt_main)
        # 状态标签
        self.lb_audit_bz = StateLable(self)
        self.lb_audit_bz.show()


    # 清空数据
    def clearData(self):
        self.al_audit_user.setText('')
        self.al_audit_time.setText('')
        self.al_audit_content.setPlainText('')
        self.lb_audit_bz.show2(False)

    # 设置数据
    def setData(self,data:dict):
        self.btn_review.stop()
        if data['shzt']=='已审核':
            self.lb_audit_bz.show2(False)
            self.btn_audit.start()
        else:
            self.lb_audit_bz.show2()
            self.btn_audit.setText('取消审阅')
        self.al_audit_user.setText(data['shxm'])
        self.al_audit_time.setText(data['shrq'])
        self.al_audit_content.setPlainText(data['jg'])

    # 状态变更
    def statechange(self):
        # 从完成审阅 -> 取消审阅
        if '完成' in self.btn_review.text():
            self.btn_audit.stop()
            self.btn_audit.setText('取消审阅')
        else:
            pass

    # 获取审阅备注信息
    def get_sybz(self):
        return self.al_audit_content.toPlainText()

    # 按钮点击
    def on_btn_audit_click(self):
        if '完成审核' in self.btn_audit.text():
            syzt = True
        else:
            syzt = False
        self.btnClick.emit(syzt)


class AuditLabel(QLabel):

    def __init__(self,p_str=None,parent=None):
        super(AuditLabel,self).__init__(p_str,parent)
        self.setStyleSheet('''border: 1px solid;font: 75 12pt \"微软雅黑\";''')
        self.setMinimumWidth(80)

class StateLable(QLabel):

    def __init__(self,parent):
        super(StateLable,self).__init__(parent)
        self.setMinimumSize(200,200)
        self.setGeometry(200,-60,100,100)
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


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = ReportEquipUI()
    ui.show()
    app.exec_()