# 报告下载客户端
# 登录采用短信方式

from app_report_down import *

class Login_UI(QDialog):

    def __init__(self,parent=None):
        super(Login_UI,self).__init__(parent)
        self.initParas()
        self.initUI()

    def initParas(self):
        self.login_bg = file_ico("login.png")
        self.login_style = "font: 75 14pt \"微软雅黑\";" \
                      "color:  rgb(45, 135, 66);" \
                      "background-image: url(:/resource/image/login.png);"
        self.login_font = "font: 75 8pt;color:  #CD0000"

    def initUI(self):
        self.setWindowTitle("明州体检")
        self.setFixedSize(500,400)
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
        self.user_id   = LineEdit(None,"", LineEdit.SUCCESS_STYLE)
        regx=QRegExp("[a-zA-Z0-9]+$")
        validator=QRegExpValidator(regx,self.user_id)
        self.user_id.setValidator(validator)              #根据正则做限制，只能输入数字
        self.user_id.setMaximumWidth(200)
        # 用户密码
        self.user_pwd = LineEdit(None,"", LineEdit.SUCCESS_STYLE)
        self.user_pwd.setMaximumWidth(200)
        self.user_pwd.setEchoMode(QLineEdit.Password)
        ######################添加布局##########################################
        layout0 = QHBoxLayout()
        layout0.addStretch()
        layout1 = QHBoxLayout()
        layout.addWidget(QLabel(""))
        layout.addRow(QLabel("账户："), self.user_id)
        layout.addRow(QLabel("密码："), self.user_pwd)
        layout.addRow(QLabel(""), layout0)
        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(10)
        layout1.addStretch()
        layout1.addLayout(layout)
        layout1.addStretch()
        self.buttonBox=QDialogButtonBox()
        self.buttonBox.addButton("登录",QDialogButtonBox.YesRole)
        self.buttonBox.addButton("取消", QDialogButtonBox.NoRole)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.on_btn_login)
        self.buttonBox.rejected.connect(self.reject)

        mainLayout.addSpacing(30)
        mainLayout.addLayout(layout1)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

    # 验证短信
    def on_btn_login(self):
        user_id=self.user_id.text()
        user_pwd=self.user_pwd.text()
        if all([user_id,user_pwd]):
            pass
        else:
            mes_about("账户或密码不能为空")

        if _user_id:
            try:
                result = self.session.query(MT_TJ_USER).filter(MT_TJ_USER.xtsb == '101', MT_TJ_USER.yhdm == _user_id).filter(or_(MT_TJ_USER.yhkl==_user_pwd,MT_TJ_USER.yhkl==None)).scalar()
            except Exception as e:
                result = []
                mes_about(self,"验证密码失败！请检查网络，错误信息：%s" %e)
                return
            if result:
                results = self.session.query(MT_TJ_YGQSKS).filter(MT_TJ_YGQSKS.yggh == _user_id).all()
                ksbms = [result.ksbm.rstrip() for result in results]
                gol.set_value('login_user_ksbms', ksbms)
                gol.set_value('login_user_id',_user_id)
                gol.set_value('login_user_pwd', _user_pwd)
                gol.set_value('login_time', cur_datetime())
                ######################################################
                self.accept()
            else:
                if _user_name:
                    mes_about(self,"您输入的密码：%s 有误，请重新输入！" %_user_pwd)
                    return

                else:
                    mes_warn(self,"您输入的账户:%s,密码:%s，有误！\n请确认后重新登陆！" %(_user_id,_user_pwd))



if __name__=="__main__":
    from utils.envir import *
    set_env()
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    ui = Login_UI()
    ui.show()
    ui.exec_()
