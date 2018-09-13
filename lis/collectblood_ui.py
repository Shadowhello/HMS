from widgets.cwidget import *
from utils import gol

def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)
        f.close()

class Lable(QLabel):

    def __init__(self):
        super(Lable,self).__init__()
        self.setMinimumWidth(75)
        self.setStyleSheet('''font: 75 11pt '黑体';color: rgb(0, 85, 255);''')

class PicLable(QLabel):

    def __init__(self):
        super(PicLable,self).__init__()
        self.setText('身\n份\n证\n照\n片')
        self.setAlignment(Qt.AlignCenter)
        # 一寸照大小
        self.setFixedWidth(102)
        self.setFixedHeight(126)
        self.setFrameShape(QFrame.Box)
        self.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);")

    def show2(self,datas):
        # write_file(datas, filename)
        p = QPixmap()
        p.loadFromData(datas)          # 数据不落地,高效
        self.setPixmap(p)

class CollectBlood_UI(UI):

    def __init__(self,title):
        super(CollectBlood_UI,self).__init__(title)

        ####################左边布局#####################################
        left_up_gp = QGroupBox('筛选条件')
        left_up_lt = QVBoxLayout()
        self.serialno= QSerialNo()
        left_up_lt.addWidget(self.serialno)
        left_up_gp.setLayout(left_up_lt)

        self.left_down_gp = QGroupBox('采血列表')
        left_down_lt = QVBoxLayout()
        self.blood_cols = OrderedDict([
            ("cjzt", "状态"),
            ("tmbh", "条码号"),
            ("tjbh","体检编号"),
            ("xm","姓名"),
            ("xb", "性别"),
            ("xb", "性别"),
            ("nl", "年龄"),
            ("xmhz", "条码项目")
        ])
        self.blood_table = TableWidget(self.blood_cols)
        self.blood_table.verticalHeader().setVisible(False)   # 去掉行头
        self.blood_table.setMinimumWidth(200)

        left_down_lt.addWidget(self.blood_table)
        self.left_down_gp.setLayout(left_down_lt)

        self.left_layout.addWidget(left_up_gp)
        self.left_layout.addWidget(self.left_down_gp)
        #self.left_layout.addStretch()

        ######################中间布局######################################
        group1 = QGroupBox('人员信息')
        layout1 = QGridLayout()
        group2 = QGroupBox('条码信息')
        layout2 = QHBoxLayout()
        group3 = QGroupBox('抽血详情')
        self.layout3 = QGridLayout()
        group4 = QGroupBox('留样详情')
        self.layout4 = QGridLayout()
        group5 = QGroupBox('拒检详情')
        self.layout5 = QGridLayout()

        ########################控件区#####################################
        self.user_id   = Lable()          # 体检编号
        self.user_name = Lable()          # 姓名
        self.user_sex =  Lable()          # 性别
        self.user_age =  Lable()          # 年龄->自动转换出生年月
        # self.depart   =  Lable()          #班级
        self.dwmc    =   Lable()          #单位名称
        # self.tj_qdrq =   Lable()          # 签到日期，默认当天
        self.sjhm   =    Lable()          #手机号码
        self.sfzh    =   Lable()          #身份证号
        # self.tj_djrq =   Lable()          # 登记日期
        self.lb_pic = PicLable()

        self.ser_all = Lable()
        self.ser_cx = Lable()
        self.ser_ly = Lable()
        self.ser_done = Lable()
        self.ser_undone = Lable()
        self.ser_jj = Lable()

        ###################基本信息  第一行##################################
        layout1.addWidget(QLabel('体检编号：'), 0, 0, 1, 1)
        layout1.addWidget(self.user_id, 0, 1, 1, 1)
        layout1.addWidget(QLabel('姓    名：'), 0, 2, 1, 1)
        layout1.addWidget(self.user_name, 0, 3, 1, 1)
        layout1.addWidget(QLabel('性    别：'), 0, 4, 1, 1)
        layout1.addWidget(self.user_sex, 0, 5, 1, 1)
        layout1.addWidget(self.lb_pic, 0, 6, 3, 3)

        ###################基本信息  第二行##################################
        layout1.addWidget(QLabel('年    龄：'), 1, 0, 1, 1)
        layout1.addWidget(self.user_age, 1, 1, 1, 1)
        layout1.addWidget(QLabel('单位名称：'), 1, 2, 1, 1)
        layout1.addWidget(self.dwmc, 1, 3, 1, 3)

        ###################基本信息  第三行##################################
        layout1.addWidget(QLabel('手机号码：'), 2, 0, 1, 1)
        layout1.addWidget(self.sjhm, 2, 1, 1, 1)
        layout1.addWidget(QLabel('身份证号：'), 2, 2, 1, 1)
        layout1.addWidget(self.sfzh, 2, 3, 1, 3)

        layout1.setHorizontalSpacing(10)            #设置水平间距
        layout1.setVerticalSpacing(10)              #设置垂直间距
        layout1.setContentsMargins(10, 10, 10, 10)  #设置外间距
        layout1.setColumnStretch(11, 1)             #设置列宽，添加空白项的

        group1.setLayout(layout1)

        layout2.addWidget(QLabel("总条码数："))
        layout2.addWidget(self.ser_all)
        layout2.addSpacing(10)
        layout2.addWidget(QLabel("抽血条码："))
        layout2.addWidget(self.ser_cx)
        layout2.addSpacing(10)
        layout2.addWidget(QLabel("留样条码："))
        layout2.addWidget(self.ser_ly)
        layout2.addSpacing(10)
        layout2.addWidget(QLabel("已抽条码："))
        layout2.addWidget(self.ser_done)
        layout2.addSpacing(10)
        layout2.addWidget(QLabel("拒检条码："))
        layout2.addWidget(self.ser_jj)
        layout2.addSpacing(10)
        layout2.addWidget(QLabel("剩余条码："))
        layout2.addWidget(self.ser_undone)
        layout2.addSpacing(10)
        layout2.addStretch()
        group2.setLayout(layout2)

        group3.setLayout(self.layout3)
        group4.setLayout(self.layout4)
        group5.setLayout(self.layout5)

        self.middle_layout.addWidget(group1)
        self.middle_layout.addWidget(group2)
        self.middle_layout.addWidget(group3)
        self.middle_layout.addWidget(group4)
        self.middle_layout.addWidget(group5)
        self.middle_layout.addStretch()

        ####################右边布局#####################################
        self.cb_is_photo = QCheckBox('扫单自动拍照')
        self.cb_is_photo.setChecked(True)
        self.btn_take_photo = QPushButton(Icon('体检拍照'),'手动拍照')
        right_up_gp = QGroupBox('摄像头')
        right_up_gp.setAlignment(Qt.AlignHCenter)
        right_up_lt = QVBoxLayout()
        # 是否载入摄像头
        if gol.get_value('photo_enable'):
            show_x = gol.get_value('photo_capture_width')
            show_y = gol.get_value('photo_capture_height')
            capture = gol.get_value('photo_capture')
            fps = gol.get_value('photo_fps')
            try:
                self.camera = CameraUI(show_x,show_y,capture,fps)
                right_up_lt.addWidget(self.camera)
            except Exception as e:
                mes_about(self,'载入摄像头功能失败，错误信息：%s' %e)
                self.camera = None
        else:
            self.camera = None
            # 不载入摄像头 则关闭右侧栏
            self.on_right_clicked()
            # 关闭 自动拍照
            self.cb_is_photo.setChecked(False)

        right_up_lt.addStretch()
        right_up_gp.setLayout(right_up_lt)
        # 按钮区
        right_middle_gp = QGroupBox()
        right_middle_lt = QHBoxLayout()

        right_middle_lt.addWidget(self.cb_is_photo)
        right_middle_lt.addWidget(self.btn_take_photo)
        right_middle_gp.setLayout(right_middle_lt)

        # 照片显示位置
        right_down_gp = QGroupBox('采血照片')
        right_down_gp.setAlignment(Qt.AlignHCenter)
        right_down_lt = QVBoxLayout()
        self.photo_lable = QLabel()
        # self.photo_lable.setStyleSheet("QLabel{border:2px solid rgb(0, 85, 255);}")
        # self.photo_lable.setFixedWidth(gol.get_value('photo_capture_width'))
        # self.photo_lable.setFixedHeight(gol.get_value('photo_capture_height'))
        right_down_lt.addWidget(self.photo_lable)
        right_down_lt.addStretch()
        right_down_gp.setLayout(right_down_lt)
        self.right_layout.addWidget(right_up_gp)
        self.right_layout.addWidget(right_middle_gp)
        self.right_layout.addWidget(right_down_gp)
        self.right_layout.addStretch()


