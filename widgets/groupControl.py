from widgets.cwidget import *

class UserInfoLable(QLabel):

    def __init__(self,font_size=12):
        super(UserInfoLable,self).__init__()
        #self.setMinimumWidth(75)
        self.setStyleSheet('''font: 75 %spt "微软雅黑";color: rgb(50, 150, 0);''' %font_size)

# 业务组件 用户详细信息
class UserDetailGroup(QGroupBox):

    def __init__(self):
        super(UserDetailGroup,self).__init__()
        self.setTitle('人员信息')

        ########################控件区#####################################
        self.lb_user_id   = UserInfoLable(14)          # 体检编号
        self.lb_user_name = UserInfoLable()          # 姓名
        self.lb_user_sex =  UserInfoLable()          # 性别
        self.lb_user_age =  UserInfoLable()          # 年龄
        self.lb_user_dwmc = UserInfoLable()          # 单位名称
        self.lb_user_phone = UserInfoLable()         # 手机号码
        self.lb_user_cardno = UserInfoLable()        # 身份证号
        self.lb_user_type = UserInfoLable()          # 用户类型：贵宾、职业病、招工、普通
        self.lb_user_pic = UserInfoLable()           # 用户照片

        lt_main = QGridLayout()
        ###################基本信息  第一行##################################
        lt_main.addWidget(QLabel('体检编号：'), 0, 0, 1, 1)
        lt_main.addWidget(self.lb_user_id, 0, 1, 1, 1)
        lt_main.addWidget(QLabel('姓    名：'), 0, 2, 1, 1)
        lt_main.addWidget(self.lb_user_name, 0, 3, 1, 1)
        lt_main.addWidget(QLabel('性    别：'), 0, 4, 1, 1)
        lt_main.addWidget(self.lb_user_sex, 0, 5, 1, 1)
        lt_main.addWidget(QLabel('年    龄：'), 0, 6, 1, 1)
        lt_main.addWidget(self.lb_user_age, 0, 7, 1, 1)
        lt_main.addWidget(QLabel('体检类型：'), 0, 8, 1, 1)
        lt_main.addWidget(self.lb_user_type, 0, 9, 1, 1)

        ###################基本信息  第二行##################################
        lt_main.addWidget(QLabel('手机号码：'), 1, 0, 1, 1)
        lt_main.addWidget(self.lb_user_phone, 1, 1, 1, 1)
        lt_main.addWidget(QLabel('身份证号：'), 1, 2, 1, 1)
        lt_main.addWidget(self.lb_user_cardno, 1, 3, 1, 3)
        lt_main.addWidget(QLabel('单位名称：'), 1, 6, 1, 1)
        lt_main.addWidget(self.lb_user_dwmc, 1, 7, 1, 3)

        lt_main.setHorizontalSpacing(10)            #设置水平间距
        lt_main.setVerticalSpacing(10)              #设置垂直间距
        lt_main.setContentsMargins(10, 10, 10, 10)  #设置外间距
        lt_main.setColumnStretch(11, 1)             #设置列宽，添加空白项的
        self.setLayout(lt_main)

    def setData(self,data:dict):
        self.clearData()
        self.lb_user_id.setText(data['tjbh'])
        self.lb_user_name.setText(data['xm'])
        self.lb_user_sex.setText(data['xb'])
        self.lb_user_age.setText(data['nl'])
        self.lb_user_dwmc.setText(data['dwmc'])
        self.lb_user_phone.setText(data['sjhm'])
        self.lb_user_cardno.setText(data['sfzh'])
        self.lb_user_type.setText('')
        self.lb_user_pic.setText('')

    def clearData(self):
        self.lb_user_id.setText('')
        self.lb_user_name.setText('')
        self.lb_user_sex.setText('')
        self.lb_user_age.setText('')
        self.lb_user_dwmc.setText('')
        self.lb_user_phone.setText('')
        self.lb_user_cardno.setText('')
        self.lb_user_type.setText('')
        self.lb_user_pic.setText('')

# 科室项目信息
class DepartItemsGroup(QGroupBox):

    # 自定义 信号，封装对外使用
    currentTextChanged = pyqtSignal(str,str)

    def __init__(self):
        super(DepartItemsGroup,self).__init__()
        self.setTitle('科室信息')
        self.initUI()
        self.cb_depart.currentTextChanged.connect(self.on_cb_derpat_change)
        self.cb_item.currentTextChanged.connect(self.on_db_item_change)

    def initUI(self):
        lt_main = QHBoxLayout()
        self.cb_depart = QComboBox()
        self.cb_item = QComboBox()
        self.lb_jcys = UserInfoLable()
        self.lb_jcrq = UserInfoLable()
        lt_main.addWidget(QLabel('当前科室：'))
        lt_main.addWidget(self.cb_depart)
        lt_main.addWidget(QLabel('组合项目：'))
        lt_main.addWidget(self.cb_item)
        lt_main.addWidget(QLabel('检查医生：'))
        lt_main.addWidget(self.lb_jcys)
        lt_main.addWidget(QLabel('检查时间：'))
        lt_main.addWidget(self.lb_jcrq)
        self.setLayout(lt_main)

    def setData(self,data):
        pass

    def clearData(self):
        self.cb_depart.clear()
        self.cb_item.clear()

    # 科室下拉->刷新组合项目
    def on_cb_derpat_change(self):
        pass

    # 组合项目下拉
    def on_db_item_change(self):
        pass

# 项目默认结果列
class ItemDefaultwidget(QListWidget):

    is_left=True

    def __init__(self,parent=None):
        super(ItemDefaultwidget,self).__init__(parent)

    def mouseDoubleClickEvent(self, event):
        super(ItemDefaultwidget, self).mouseDoubleClickEvent(event)
        if event.button() == Qt.LeftButton:
            self.is_left=True
        elif event.button() == Qt.RightButton:
            self.is_left=False
        else:
            pass


# 条件搜索组
class condiSearchGroup(QGroupBox):
    def __init__(self):
        super(condiSearchGroup, self).__init__()
        # 日期
        self.s_date = DateGroup(-3)
        self.s_dwbh = TUintGroup({}, {})
        self.s_depart = DepartGroup()
        self.s_area = AreaGroup()

        ###################基本信息  第一行##################################
        self.addItem(self.s_date, 0, 0, 1, 3)

        ###################基本信息  第二行##################################
        self.addItem(self.s_dwbh, 1, 0, 1, 5)
        self.addItem(self.s_depart, 1, 5, 1, 2)
        self.addItem(self.s_area, 1, 7, 1, 2)

        self.setHorizontalSpacing(10)  # 设置水平间距
        self.setVerticalSpacing(10)  # 设置垂直间距
        self.setContentsMargins(10, 10, 10, 10)  # 设置外间距
        self.setColumnStretch(14, 1)  # 设置列宽，添加空白项的

    @property
    def date_range(self):
        return self.s_date.get_date_range

    @property
    def where_tjqy(self):
        return self.s_area.where_tjqy

    @property
    def where_dwmc(self):
        return self.s_dwbh.where_dwmc

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = UserDetailGroup()
    ui.show()
    app.exec_()