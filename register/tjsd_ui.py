from widgets.cwidget import *

# 导检收单
class TJSD_UI(UI):

    def __init__(self,title):
        super(TJSD_UI,self).__init__(title)
        self.initUI()

    def initUI(self):
        ####################左边布局#####################################
        gp_left_up = QGroupBox('筛选条件')
        lt_left_up = QVBoxLayout()
        self.le_tjbh = QTJBH()
        self.cb_is_pacs = QCheckBox('关联检查项目')
        self.cb_is_pacs.setIcon(Icon('pacs'))
        self.cb_is_pacs.setChecked(True)
        self.cb_is_myd = QCheckBox('打开满意度')
        self.cb_is_myd.setIcon(Icon('满意度'))
        self.cb_is_myd.setChecked(True)
        lt_left_up.addWidget(self.le_tjbh)
        lt_left_up.addWidget(self.cb_is_pacs)
        lt_left_up.addWidget(self.cb_is_myd)
        gp_left_up.setLayout(lt_left_up)
        #######
        self.gp_left_bottom = QGroupBox('收单列表')
        lt_left_bottom = QHBoxLayout()
        self.table_tjsd_cols = OrderedDict([
            ('state',"状态"),
            ('tjbh', "体检编号"),
            ('xm', "姓名")
        ])
        self.table_tjsd = TableWidget(self.table_tjsd_cols)
        self.table_tjsd.setColumnWidth(0, 30)
        self.table_tjsd.setColumnWidth(1, 70)
        self.table_tjsd.setColumnWidth(2, 30)
        self.table_tjsd.setFixedWidth(150)
        lt_left_bottom.addWidget(self.table_tjsd)
        self.gp_left_bottom.setLayout(lt_left_bottom)
        # 添加左布局
        self.left_layout.addWidget(gp_left_up)
        self.left_layout.addWidget(self.gp_left_bottom)

        ####################中间布局#####################################
        self.gp_user = TJSDUser()
        self.gp_middle_bottom = QGroupBox('项目状态（0）')
        lt_middle_bottom = QHBoxLayout()
        self.table_item_state_cols = OrderedDict(
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
                ("btn", "")
             ])
        self.table_item_state = ItemsStateTable(self.table_item_state_cols)
        lt_middle_bottom.addWidget(self.table_item_state)
        self.gp_middle_bottom.setLayout(lt_middle_bottom)

        self.middle_layout.addWidget(self.gp_user)
        self.middle_layout.addWidget(self.gp_middle_bottom)

        ####################右边布局#####################################
        self.camera = CameraGroup()
        self.right_layout.addLayout(self.camera)
        # gp_right_up = QGroupBox('摄像头')
        # gp_right_up.setAlignment(Qt.AlignHCenter)
        # lt_right_up = QVBoxLayout()
        # # 是否载入摄像头
        # if gol.get_value('photo_enable'):
        #     show_x = gol.get_value('photo_capture_width')
        #     show_y = gol.get_value('photo_capture_height')
        #     capture = gol.get_value('photo_capture')
        #     fps = gol.get_value('photo_fps')
        #     try:
        #         self.camera = CameraUI(595,842,capture,fps)
        #         lt_right_up.addWidget(self.camera)
        #         gp_right_up.setLayout(lt_right_up)
        #     except Exception as e:
        #         mes_about(self,'载入摄像头功能失败，错误信息：%s' %e)
        #         self.camera = None
        # else:
        #     self.camera = None
        #
        # #################################################
        # self.btn_take_photo = QPushButton(Icon('体检拍照'), '手动拍照')
        # lt_right_middle = QHBoxLayout()
        # lt_right_middle.addWidget(self.btn_take_photo)
        # self.right_layout.addWidget(gp_right_up)
        # self.right_layout.addLayout(lt_right_middle)

class TJSDUser(QGroupBox):

    def __init__(self):
        super(TJSDUser,self).__init__()
        self.setTitle('人员信息')
        self.initUI()
        self.btn_read.clicked.connect(self.on_btn_sfzh_read)

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_1 = QHBoxLayout()
        lt_2 = QHBoxLayout()
        ########################控件区#####################################
        self.lb_user_id   = UserLable()          # 体检编号
        self.lb_user_name = UserLable()          # 姓名
        self.lb_user_sex =  UserLable()          # 性别
        self.lb_user_age =  UserLable()          # 年龄->自动转换出生年月
        self.lb_user_sjhm = UserLable()          # 手机号码
        self.lb_user_sfzh = UserLable()          # 身份证号
        self.btn_read = QPushButton('...')       # 读身份证号
        self.lb_user_dwmc = UserLable()          # 单位名称

        lt_1.addWidget(QLabel('体检编号：'))
        lt_1.addWidget(self.lb_user_id)
        lt_1.addWidget(QLabel('姓名：'))
        lt_1.addWidget(self.lb_user_name)
        lt_1.addWidget(QLabel('性别：'))
        lt_1.addWidget(self.lb_user_sex)
        lt_1.addWidget(QLabel('年龄：'))
        lt_1.addWidget(self.lb_user_age)
        lt_1.addWidget(QLabel('手机号码：'))
        lt_1.addWidget(self.lb_user_sjhm)
        lt_2.addWidget(QLabel('身份证号：'))
        lt_2.addWidget(self.lb_user_sfzh)
        lt_2.addWidget(self.btn_read)
        lt_2.addWidget(QLabel('单位名称：'))
        lt_2.addWidget(self.lb_user_dwmc)
        lt_main.addLayout(lt_1)
        lt_main.addLayout(lt_2)
        # lt_main.addStretch()                  #设置列宽，添加空白项的
        self.setLayout(lt_main)

    @property
    def user_id(self):
        return self.lb_user_id.text()

    # 赋值
    def setData(self,data:dict):
        self.clearData()
        self.lb_user_id.setText(data.get('tjbh',''))
        self.lb_user_name.setText(data.get('xm',''))
        self.lb_user_sex.setText(data.get('xb',''))
        self.lb_user_age.setText(data.get('nl',''))
        self.lb_user_sjhm.setText(data.get('sjhm',''))
        self.lb_user_sfzh.setText(data.get('sfzh',''))
        self.lb_user_dwmc.setText(data.get('dwmc', ''))

    # 清空数据
    def clearData(self):
        self.lb_user_id.setText('')
        self.lb_user_name.setText('')
        self.lb_user_sex.setText('')
        self.lb_user_age.setText('')
        self.lb_user_sjhm.setText('')
        self.lb_user_sfzh.setText('')
        self.lb_user_dwmc.setText('')

    def on_btn_sfzh_read(self):
        dialog = ReadChinaIdCard_UI(self)
        dialog.sendIdCard.connect(self.UpdateData)
        dialog.exec_()

    #赋值
    def UpdateData(self,sfzh,xm):
        self.s_sfzh.setText(sfzh)
        self.s_xm.setText(xm)

# 定制化组件
class UserLable(QLabel):

    def __init__(self):
        super(UserLable,self).__init__()
        self.setStyleSheet('''font: 75 12pt '微软雅黑';color: rgb(0, 85, 255);''')


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = TJSD_UI('111')
    ui.show()
    app.exec_()