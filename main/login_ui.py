from main.model import *
from widgets.LineEdit import *
from widgets.bwidget import *
from utils import gol
from utils import *


class Login_UI(QDialog):

    def __init__(self,parent=None):
        super(Login_UI,self).__init__(parent)
        self.initParas()
        self.initUI()

    def initParas(self):
        self.login_title = gol.get_value('login_title', '明州体检')
        self.lgoin_width = gol.get_value('login_width',500)
        self.login_height = gol.get_value('login_height',400)
        self.login_bg = file_ico("login.png")
        self.login_style = "font: 75 14pt \"微软雅黑\";" \
                      "color:  rgb(45, 135, 66);" \
                      "background-image: url(:/resource/image/login.png);"
        self.login_font = "font: 75 8pt;color:  #CD0000"
        # 获取用户名
        self.session = gol.get_value("tjxt_session_local")
        self.log = gol.get_value("log")

    def initUI(self):
        self.setWindowTitle(self.login_title)
        self.setFixedSize(self.lgoin_width,self.login_height)
        self.setWindowIcon(Icon("mztj"))
        self.setStyleSheet(self.login_style)
        self.setWindowFlags(Qt.FramelessWindowHint)     #窗口模式，去掉标题栏

        # 给窗体再加一个widget控件，对widget设置背景图片
        self.widget=QWidget(self)
        self.widget.setFixedSize(self.lgoin_width,self.login_height)
        palette=QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(self.login_bg)))
        self.widget.setPalette(palette)
        self.widget.setAutoFillBackground(True)

        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignCenter)
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.setFormAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        # 用户ID
        self.userid   = LineEdit(None,"", LineEdit.SUCCESS_STYLE)
        regx=QRegExp("[a-zA-Z0-9]+$")
        validator=QRegExpValidator(regx,self.userid)
        self.userid.setValidator(validator)              #根据正则做限制，只能输入数字
        self.userid.setMaximumWidth(200)
        # self.userid.setFocusPolicy(Qt.ClickFocus)
        # 用户姓名
        self.user = LineEdit(None,"", LineEdit.SUCCESS_STYLE)
        self.user.setDisabled(True)
        self.user.setMaximumWidth(200)
        # 用户密码
        self.passwd = LineEdit(None,"", LineEdit.SUCCESS_STYLE)
        self.passwd.setMaximumWidth(200)
        self.passwd.setEchoMode(QLineEdit.Password)
        # 是否自动填充
        self.is_rem=QCheckBox("记住最近登录")
        self.is_rem.setStyleSheet(self.login_font)
        # 进入主界面还是接口界面
        self.is_equip=QCheckBox("进入设备接口")
        self.is_equip.setStyleSheet(self.login_font)

        if gol.get_value('login_auto_record',0)==0:
            self.is_rem.setChecked(False)
        else:
            self.is_rem.setChecked(True)
            # 自动填充最近登录信息
            self.userid.setText(str(gol.get_value('login_user_id', 'BSSA')))
            self.user.setText(gol.get_value('login_user_name', '管理员'))

        if gol.get_value('system_is_equip',0)==0:
            self.is_equip.setChecked(False)
        else:
            self.is_equip.setChecked(True)

        ######################添加布局##########################################
        layout0 = QHBoxLayout()
        layout0.addWidget(self.is_rem)
        layout0.addWidget(self.is_equip)
        layout0.addStretch()
        login_user = "                       "
        layout.addWidget(QLabel(""))
        layout.addRow(QLabel("账户："), self.userid)
        layout.addRow(login_user,self.user)
        layout.addRow(QLabel("密码："), self.passwd)
        layout.addRow(QLabel(""), layout0)
        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(10)

        self.buttonBox=QDialogButtonBox()
        self.buttonBox.addButton("登录",QDialogButtonBox.YesRole)
        self.buttonBox.addButton("取消", QDialogButtonBox.NoRole)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.buttons()[0].setEnabled(False)
        # 失去焦点
        # self.buttonBox.buttons()[0].setFocusPolicy(Qt.ClickFocus)
        # self.buttonBox.buttons()[1].setFocusPolicy(Qt.NoFocus)

        # 对登录进行限制
        if self.user.text():
            self.buttonBox.buttons()[0].setEnabled(True)
        else:
            self.buttonBox.buttons()[0].setEnabled(False)

        self.userid.textEdited.connect(self.set_empty)
        self.userid.editingFinished.connect(self.user_get)
        self.is_equip.stateChanged.connect(self.on_equip_change)
        self.buttonBox.accepted.connect(self.login)
        self.buttonBox.rejected.connect(self.reject)

        mainLayout.addSpacing(30)
        mainLayout.addLayout(layout)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

    def on_equip_change(self,p_int):
        gol.set_value("system_is_equip",p_int)

    def user_get(self):
        userid = self.userid.text()
        if userid:
            result=self.session.query(MT_TJ_USER).filter(MT_TJ_USER.xtsb=='101',MT_TJ_USER.yhdm==userid).scalar()
            if result:
                self.user.setText(str2(result.yhmc))
                self.buttonBox.buttons()[0].setEnabled(True)

    def set_empty(self,p_str):
        self.userid.setText(p_str.upper())
        self.user.setText("")
        self.buttonBox.buttons()[0].setEnabled(False)

    # 验证密码
    def login(self):
        _user_id=self.userid.text()
        _user_name = self.user.text()
        _user_pwd=self.passwd.text()
        if _user_id:
            result = self.session.query(MT_TJ_USER).filter(MT_TJ_USER.xtsb == '101', MT_TJ_USER.yhdm == _user_id).filter(or_(MT_TJ_USER.yhkl==_user_pwd,MT_TJ_USER.yhkl==None)).scalar()
            if result:
                results = self.session.query(MT_TJ_YGQSKS).filter(MT_TJ_YGQSKS.yggh == _user_id).all()
                ksbms = [result.ksbm.rstrip() for result in results]
                gol.set_value('login_user_ksbms', ksbms)
                gol.set_value('login_user_id',_user_id)
                gol.set_value('login_user_name', _user_name)
                gol.set_value('login_user_pwd', _user_pwd)
                gol.set_value('login_time', cur_datetime())
                ############### 写入配置 #########################
                if self.is_rem.isChecked():
                    auto_record = 1
                else:
                    auto_record = 0
                if self.is_equip.isChecked():
                    is_equip = 1
                else:
                    is_equip = 0
                login={
                    "auto_record":auto_record,
                    "user_id":_user_id,
                    "user_name":_user_name
                }
                system={
                    "is_equip":is_equip
                }
                config_write("custom.ini", "login", login)
                config_write("custom.ini", "system", system)
                self.log.info('写入配置(custom.ini)文件成功')
                self.log.info("用户：%s(%s) 登陆成功！" %(_user_name,_user_id))
                self.accept()
            else:
                if _user_name:
                    mes_about(self,"您输入的密码：%s 有误，请重新输入！" %_user_pwd)
                    return

                else:
                    mes_warn(self,"您输入的账户:%s,密码:%s，有误！\n请确认后重新登陆！" %(_user_id,_user_pwd))
        else:
            mes_about("请输入账户！！")


if __name__=="__main__":
    from utils.envir import *
    set_env()
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    ui = Login_UI()
    ui.show()
    ui.exec_()