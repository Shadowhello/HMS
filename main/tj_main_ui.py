import requests
from main.main_ui import *
from utils import gol
from utils.base import cur_date,get_system
# 动态模块需加入，打包工具无法检测自省模块，要不然需以源码形式跑
# 采血留样 管理
from lis import SampleManager
# C13/14 管理
from C13 import BreathManager
# 报告管理
from report import ReportManager
# 慢病管理
from mbgl import NCDManager
# 结果录入管理
from result import ResultManager
# 加入VIP 管理
from vip import VipManager
# 加入绩效
from statistics import DN_MeritPay
# 体检登记
from register import RegisterManager
# OA
from app_interface import OaUI,PhoneUI,JHJKGLUI,MediaUI

WindowsTitle="明州体检"
WindowsIcon="mztj"

class TJ_Main_UI(QMainWindow):

    def __init__(self):
        super(TJ_Main_UI, self).__init__()

        #载入参数
        self.initParas()
        # 载入公共组件：菜单栏、工具栏、状态栏
        self.initUI()
        # 载入样式
        with open(self.stylesheet) as f:
            self.setStyleSheet(f.read())
        # 载入当前用户默认界面
        action = self.menuBar().default_action(self.user_menu_sid)
        if action:
            self.openWidget(action)
        else:
            mes_about(self,'用户登录默认界面配置不正确或者未开放，按钮SID是%s' %str(self.user_menu_sid))

        # 启动自动更新线程
        if self.update_auto:
            self.timer_update_thread = AutoUpdateThread(600)
            self.timer_update_thread.setTask(self.url)
            self.timer_update_thread.signalPost.connect(self.update_mes, type=Qt.QueuedConnection)
            self.timer_update_thread.start()

    # 初始化界面
    def initUI(self):
        self.setWindowTitle(WindowsTitle)
        self.setWindowIcon(Icon(WindowsIcon))
        self.initMenuBar()
        self.initStatusBar()

        self.mdiArea=QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.SubWindowView)                       #子窗口模式
        self.setCentralWidget(self.mdiArea)

    # 初始化参数
    def initParas(self):
        self.log = gol.get_value('log')
        self.stylesheet = file_style(gol.get_value('file_qss','mztj.qss'))
        self.update_auto = gol.get_value('update_auto',True)
        self.update_timer = gol.get_value('update_timer',360)
        self.user_menu_sid = gol.get_value('menu_sid',5001)
        self.login_id = gol.get_value('login_user_id')
        sys_version = gol.get_value('system_version', 1.0)
        update_url = gol.get_value('system_update', "http://10.7.200.101:5005/api/version/%s/%s")
        self.url = update_url % (get_system(), sys_version)

    def initStatusBar(self):
        self.setStatusBar(StatusBar())

    def initMenuBar(self):
        self.setMenuBar(MenuBar(self))

    # 打开中央窗口
    def openWidget(self,action):
        module = action.module
        class_name = action.cls_name   # 必须在上一句后面，因为才赋值
        #print(module,class_name)
        if module and class_name:
            # if class_name=='DN_MeritPay' and self.login_id=='BSSA':
            #     mes_about(self,"对不起，您没有该功能权限，请联系管理员！")
            #     return
            if not hasattr(self, class_name):
                module_class = getattr(module, class_name)
                setattr(self, class_name, module_class())
                self.mdiArea.addSubWindow(getattr(self, class_name))
                getattr(self, class_name).showMaximized()
                if class_name in ['OaUI','PhonePlatUI','JHJKGLUI','MediaUI']:
                    getattr(self, class_name).load()
            elif getattr(getattr(self, class_name), 'status'): # 窗口被关闭了
                module_class = getattr(module, class_name)
                setattr(self, class_name, module_class())
                self.mdiArea.addSubWindow(getattr(self, class_name))
                getattr(self, class_name).showMaximized()
                if class_name in ['OaUI','PhonePlatUI','JHJKGLUI','MediaUI']:
                    getattr(self, class_name).load()
            # # 未关闭
            getattr(self, class_name).setFocus()
        else:
            print(44444444444)

    # #打开OA，临时解决 无法最大化的问题
    # def open_oa(self):
    #     if not hasattr(self, "widget1"):
    #         self.widget1 = OaUI('OA办公')
    #         self.mdiArea.addSubWindow(self.widget1)
    #         self.widget1.showMaximized()
    #     elif self.widget1.status:   #窗口被关闭了
    #         self.widget1 = Detail_UI(ToolButton1)
    #         self.mdiArea.addSubWindow(self.widget1)
    #         self.widget1.showMaximized()
    #     self.widget1.setFocus()

    # 注销
    def login_out(self):
        self.close()
        from main.login_ui import Login_UI
        login_ui = Login_UI()
        if login_ui.exec_():
                pass

    def update_mes(self,version,message):
        dialog = UpdateDialog(self)
        dialog.sure_update.connect(self.update_sys)
        dialog.setDatas(version,message)
        dialog.exec_()
        # dialog = mes_warn(self,"系统已有新版本")
        # if dialog != QMessageBox.Yes:
        #     pass
        # 历史版本，优先下载到本地，再提示是否更新，速度更优
        # dialog = mes_warn(self,message)
        # if dialog != QMessageBox.Yes:
        #     pass
        # else:
        #     self.close()
        #     # 启动更新进程
        #     try:
        #         sub_process_name = gol.get_value('main_process_sub', 'autoupdate.exe')
        #         os.popen(sub_process_name)
        #         self.log.info('启动更新进程！')
        #     except Exception as e:
        #         self.log.info('启动更新进程失败，错误信息：%s' %e)

    def update_sys(self):
        # self.close()
        process = QProcess()
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        update_process_name = os.path.join(dirname, 'autoupdate.exe')
        # print(update_process_name)
        try:
            process.startDetached(update_process_name)
            print("准备更新程序，启动更新进程！")
            # log.info("准备更新程序，启动更新进程！")
            sys.exit(0)
            # os._exit()
        except Exception as e:
            print("准备更新程序，启动更新进程失败，错误信息：%s" % e)
            # log.info("准备更新程序，启动更新进程失败，错误信息：%s" % e)
            return

    def on_status_widget_show(self,p_str:str):
        self.statusBar().on_change_mes(p_str)

    def closeEvent(self, *args, **kwargs):
        super(TJ_Main_UI, self).closeEvent(*args, **kwargs)
        try:
            if hasattr(self, 'SampleManager'):
                getattr(self, 'SampleManager').close()
        except Exception as e:
            self.log.info("关闭时发生错误：%s " %e)

        QThread.currentThread().quit()
        self.log.info("用户：%s(%s) 退出成功！" % (gol.get_value('login_user_name', '未知'), gol.get_value('login_user_id', ''),))


# 自动检测更新包线程
class AutoUpdateThread(QThread):

    # 定义信号,定义参数为str类型
    signalPost = pyqtSignal(str,str)     # 更新界面
    signalExit = pyqtSignal()

    def __init__(self,timer=360):
        super(AutoUpdateThread, self).__init__()
        self.running = False
        self.timer = timer
        # self.api_url = gol.get_value('api_version') % str(gol.get_value('system_version'))
        # self.update_path = '%s/%s' %(gol.get_value('app_path') ,gol.get_value('update_path'))   # 更新目录

    def setTask(self,url):
        self.url = url
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            try:
                response = requests.get(self.url)
                if response.status_code == 200:
                    describe = response.json()['describe']
                    version = response.json()['version']
                    self.signalPost.emit(str(version),describe)
                # 先下载到本地，提示是否更新
                # result = request_get(self.api_url,os.path.join(self.update_path,'%s.rar' %cur_date()))
                # if result:
                #     self.signalPost.emit('程序已有新版，单击YES后将自动更新完成！')
            except Exception as e:
                print(e)
            time.sleep(self.timer)


class UpdateDialog(QDialog):

    sure_update = pyqtSignal()

    def __init__(self,parent=None):
        super(UpdateDialog,self).__init__(parent)
        self.setWindowIcon(Icon('mztj'))
        self.setWindowTitle('明州体检')
        self.setFixedSize(500,400)
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 窗口模式，去掉标题栏
        self.initUI()
        self.setBackgroundImage()
        # 信号槽
        self.buttonBox.accepted.connect(self.on_btn_update)
        self.buttonBox.rejected.connect(self.reject)

    def initUI(self):
        lt_main = QVBoxLayout()
        ######## 更新内容 #########################
        self.gp_top = QGroupBox('更新内容')
        lt_top = QHBoxLayout()
        self.tb_up_describe = QTextBrowser()
        self.tb_up_describe.setStyleSheet('''font: 75 12pt '微软雅黑';color: rgb(0,128,0);''')
        lt_top.addWidget(self.tb_up_describe)
        self.gp_top.setLayout(lt_top)
        #### 按钮组
        self.buttonBox=QDialogButtonBox()
        self.buttonBox.addButton("更新",QDialogButtonBox.YesRole)
        self.buttonBox.addButton("取消", QDialogButtonBox.NoRole)
        self.buttonBox.setCenterButtons(True)
        # 添加布局
        lt_main.addWidget(self.gp_top)
        lt_main.addWidget(self.buttonBox)
        self.setLayout(lt_main)

    def setBackgroundImage(self):
        palette=QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(file_ico("17_big.png"))))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def setDatas(self,version,describe):
        self.gp_top.setTitle('版本V%s：更新内容' %version)
        self.tb_up_describe.setPlainText('；\r\n'.join(describe.split('；')))

    def on_btn_update(self):
        self.sure_update.emit()


if __name__ == '__main__':
    pass
