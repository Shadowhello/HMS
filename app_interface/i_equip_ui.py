from widgets.cwidget import *
from widgets.bweb import *
from .model import get_equip_sql

class EquipUI(Dialog):

    # 自定义 信号，封装对外使用
    returnPressed = pyqtSignal(str)

    def __init__(self,parent=None):
        super(EquipUI,self).__init__(parent)
        self.setWindowTitle('设备报告')
        # self.setMinimumHeight(500)
        # self.setMinimumWidth(880)
        self.initUI()
        # 信号槽
        self.returnPressed.connect(self.setQuery)
        self.btn_query.clicked.connect(self.on_btn_query_click)
        self.le_tjbh.returnPressed.connect(self.on_le_tjbh_return)
        # 查看报告
        self.table_equip.itemClicked.connect(self.on_table_equip_click)

    def setQuery(self,tjbh):
        self.le_tjbh.setText(tjbh)
        self.on_le_tjbh_return()

    def on_le_tjbh_return(self):
        tjbh = self.le_tjbh.text()
        if not tjbh:
            mes_about(self,'请您输入体检编号')
            return
        else:
            sql = get_equip_sql(tjbh)
            results = self.session.execute(sql)
            self.table_equip.load(results)
            self.gp_middle.setTitle('项目信息(%s)' %self.table_equip.rowCount())
            if self.table_equip.rowCount()>0:
                self.on_table_equip_click(self.table_equip.item(0,0))
            # mes_about(self,'共检索出数据 %s 条' %self.table_equip.rowCount())

        self.le_tjbh.setText('')

    def on_btn_query_click(self):
        if self.le_tjbh.text():
            self.on_le_tjbh_return()

    def on_table_equip_click(self,QTableWidgetItem):
        path = self.table_equip.getItemValueOfKey(QTableWidgetItem.row(),'path')
        url = gol.get_value('api_equip_show','')
        if url:
            self.wv_report_equip.load(url %path)

            # self.wv_report_equip.show()

        else:
            mes_about(self,'未配置：api_equip_show 参数！')


    def initUI(self):
        self.table_equip_cols = OrderedDict([
            ('tjbh', '体检编号'),
            ('xmzt', '状态'),
            ('equip', '设备'),
            ('jcrq','检查日期'),
            ('jcys','检查医生'),
            ('shrq', '报告日期'),
            ('shys', '报告医生'),
            ('xmjg', '项目结果'),
            ('xmzd', '项目诊断'),
            ('path', '文件路径')
        ])
        lt_main = QVBoxLayout()
        # 搜索
        lt_top = QHBoxLayout()
        self.le_tjbh = QTJBH()
        self.btn_query = QPushButton(Icon('query'),'查询')
        gp_search = QGroupBox('检索条件')
        lt_top.addWidget(QLabel('体检编号：'))
        lt_top.addWidget(self.le_tjbh)
        lt_top.addWidget(self.btn_query)
        lt_top.addStretch()
        gp_search.setLayout(lt_top)
        lt_middle = QHBoxLayout()
        self.gp_middle = QGroupBox('项目信息(0)')
        # 用户基本信息
        # self.gp_user = EquipUserGroup()
        self.table_equip = EquipTable(self.table_equip_cols)
        self.table_equip.setAlternatingRowColors(False)                       # 使用行交替颜色
        self.table_equip.verticalHeader().setVisible(False)
        lt_middle.addWidget(self.table_equip)
        self.gp_middle.setLayout(lt_middle)
        ####################右侧布局#####################
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox('报告预览')
        self.wv_report_equip = WebView()
        lt_bottom.addWidget(self.wv_report_equip)
        gp_bottom.setLayout(lt_bottom)
        # 添加布局
        lt_main.addWidget(gp_search)
        lt_main.addWidget(self.gp_middle)
        # lt_main.addLayout(self.gp_user)
        lt_main.addWidget(gp_bottom)
        self.setLayout(lt_main)

# 设备用户信息
class EquipUserGroup(QVBoxLayout):

    def __init__(self):
        super(EquipUserGroup,self).__init__()
        gp_user = QGroupBox('人员信息')
        lt_user = QHBoxLayout()
        gp_inspect = QGroupBox('检查信息')
        lt_inspect = QHBoxLayout()
        ########################控件区#####################################
        self.lb_user_id   = Lable()          # 体检编号
        self.lb_user_name = Lable()          # 姓名
        self.lb_user_sex =  Lable()          # 性别
        self.lb_user_age =  Lable()          # 年龄->自动转换出生年月
        self.lb_sjhm   =    Lable()          #手机号码
        self.lb_sfzh    =   Lable()          #身份证号
        ##################################################################
        self.lb_jcrq = Lable()               # 检查日期
        self.lb_jcrq.setMinimumWidth(80)
        self.lb_jcys = Lable()               # 检查医生
        self.lb_jcys.setMinimumWidth(50)
        self.lb_shrq =  Lable()              # 审核日期
        self.lb_shrq.setMinimumWidth(80)
        self.lb_shys =  Lable()              # 审核医生
        self.lb_shys.setMinimumWidth(50)

        lt_user.addWidget(QLabel('体检编号：'))
        lt_user.addWidget(self.lb_user_id)
        lt_user.addWidget(QLabel('姓名：'))
        lt_user.addWidget(self.lb_user_name)
        lt_user.addWidget(QLabel('性别：'))
        lt_user.addWidget(self.lb_user_sex)
        lt_user.addWidget(QLabel('年龄：'))
        lt_user.addWidget(self.lb_user_age)
        lt_user.addWidget(QLabel('手机号码：'))
        lt_user.addWidget(self.lb_sjhm)
        # lt_main.addWidget(QLabel('身份证号：'))
        # lt_main.addWidget(self.lb_sfzh)
        lt_user.addStretch()                  #设置列宽，添加空白项的
        gp_user.setLayout(lt_user)
        #######################################################
        lt_inspect.addWidget(QLabel('检查医生：'))
        lt_inspect.addWidget(self.lb_jcys)
        lt_inspect.addWidget(QLabel('检查日期：'))
        lt_inspect.addWidget(self.lb_jcrq)
        lt_inspect.addWidget(QLabel('审核医生：'))
        lt_inspect.addWidget(self.lb_shys)
        lt_inspect.addWidget(QLabel('审核日期：'))
        lt_inspect.addWidget(self.lb_shrq)
        lt_inspect.addStretch()                  #设置列宽，添加空白项的
        gp_inspect.setLayout(lt_inspect)
        self.addWidget(gp_user)
        self.addWidget(gp_inspect)

    # 赋值
    def setData(self,data:dict):
        self.clearData()
        self.lb_user_id.setText(data.get('tjbh','未获取到'))
        self.lb_user_name.setText(data.get('xm','未获取到'))
        self.lb_user_sex.setText(data.get('xb','未获取到'))
        self.lb_user_age.setText(data.get('nl','未获取到'))
        self.lb_sjhm.setText(data.get('sjhm','未获取到'))
        # self.lb_sfzh.setText(data.get('sfzh','未获取到'))
        self.lb_zjys.setText(data.get('jcys',''))
        self.lb_zjrq.setText(data.get('jcrq', ''))
        self.lb_shys.setText(data.get('shys', ''))
        self.lb_shrq.setText(data.get('shrq', ''))

    # 清空数据
    def clearData(self):
        self.lb_user_id.setText('')
        self.lb_user_name.setText('')
        self.lb_user_sex.setText('')
        self.lb_user_age.setText('')
        self.lb_sjhm.setText('')
        # self.lb_sfzh.setText('')
        self.lb_jcys.setText('')
        self.lb_jcrq.setText('')
        self.lb_shys.setText('')
        self.lb_shrq.setText('')

    @property
    def get_tjbh(self):
        return self.lb_user_id.text()

# 报告审阅列表
class EquipTable(TableWidget):

    tjqy = None  # 体检区域
    tjlx = None  # 体检类型

    def __init__(self, heads, parent=None):
        super(EquipTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # 字典载入
        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)  # 插入一行
            for col_index, col_value in enumerate(row_data):
                if col_index == len(heads)-1:
                    if col_value:
                        col_value = col_value.replace(r'D:/activefile','')
                    item = QTableWidgetItem(col_value)

                item = QTableWidgetItem(str2(col_value))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)
        # 布局
        self.setColumnWidth(0, 70)  # 体检编号
        self.setColumnWidth(1, 50)  # 体检状态
        self.setColumnWidth(2, 50)  # 设备名称
        self.setColumnWidth(3, 80)  # 检查日期
        self.setColumnWidth(4, 55)  # 检查姓名
        self.setColumnWidth(5, 80)  # 报告日期
        self.setColumnWidth(6, 55)  # 报告医生
        # self.setColumnWidth(5, 80)  # 项目结果
        # self.setColumnWidth(6, 50)  # 项目诊断
        self.horizontalHeader().setStretchLastSection(True)