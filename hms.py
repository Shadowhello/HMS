from PyQt5.QtCore import PYQT_VERSION_STR,QCoreApplication,Qt


# 判断版本号
if int(PYQT_VERSION_STR.replace('.',''))>=560:
    from PyQt5.QtWebEngineWidgets import *
    # 处理闪屏、黑屏问题 必须放在 Application 实例化前
    QCoreApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
else:
    from PyQt5.QtWebKit import *
    from PyQt5.QtWebKitWidgets import *

import multiprocessing
from multiprocessing import Process, Queue
from utils.envir import *


# 主界面
def main_ui(ui,app):
    if gol.get_value('ui_show', 0) == 0:
        ui.showMaximized()
    elif gol.get_value('ui_show', 0) == 1:
        ui.showFullScreen()
    else:
        ui.show()
    app.exec_()

#
def equip_ui(ui,app):
    ui.show()
    app.exec_()

def start_run():
    from main import Login_UI
    from widgets import CefApplication
    from cefpython3 import cefpython as cef
    from PyQt5.QtWidgets import QApplication
    import sys
    ##########################################
    #app = QApplication(sys.argv)
    sys.excepthook = cef.ExceptHook
    cef.Initialize()
    app = CefApplication(sys.argv)
    # 是否通过用户密码验证登陆
    if gol.get_value('system_is_login',1) == 1:
        login_ui = Login_UI()
        if login_ui.exec_():
            # 是否进入设备接口
            if gol.get_value('system_is_equip', 0) == 0:
                from main import TJ_Main_UI
                main_ui(TJ_Main_UI(), app)
            # 进入设备接口
            else:
                if gol.get_value('equip_type', 0) == 12:
                    pass
                    #ui = Equip2()
                else:
                    from app_equip import EquipManager
                    from pdfparse import run
                    #################无论是否，均启动后台进程#################### 为临时解决子进程启动被UI化的问题
                    # 全局进程队列
                    gol_process_queue = Queue()
                    multiprocessing.freeze_support()
                    monitor_process = Process(target=run, args=(gol_process_queue,))
                    monitor_process.start()
                    ui = EquipManager(gol_process_queue)
                    ui.show()
                    app.exec_()
                    # 退出后台子进程
                    if monitor_process.is_alive:
                        # 停止子进程
                        monitor_process.terminate()
                        # 随主进程退出
                        monitor_process.join()

    # 不需要通过用户密码验证，直接进入主界面
    elif gol.get_value('system_is_login',1) == 0:
        from main import TJ_Main_UI
        main_ui(TJ_Main_UI(), app)
    # 进入自助机模式
    else:
        from app_selfhelp import selfHelpManager,SelfHelpMachine
        ui = SelfHelpMachine()
        main_ui(ui,app)

    cef.Shutdown()

if __name__=="__main__":
    import cgitb
    # 非pycharm编辑器可用输出错误
    #sys.excepthook = cgitb.Hook(1, None, 5, sys.stderr, 'text')
    cgitb.enable(logdir="./error/",format="text")
    multiprocessing.freeze_support()
    # 启动主进程
    set_env()
    # 增加全局异常处理
    start_run()
    # try:
    #     start_run()
    # except Exception as e:
    #     error = '%s' %e
    #     ctypes.windll.user32.MessageBoxA(0,error.encode('gb2312'),'明州体检'.encode('gb2312'),0)


