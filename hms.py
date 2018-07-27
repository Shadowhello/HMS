from utils.envir import *
from multiprocessing import Process, Queue
import multiprocessing

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
    from login.login_ui import Login_UI
    from PyQt5.QtWidgets import QApplication
    import sys
    ##########################################
    app = QApplication(sys.argv)
    if gol.get_value('system_is_login',1) == 1:
        login_ui = Login_UI()
        if login_ui.exec_():
            if gol.get_value('system_is_equip', 0) == 0:
                from main.tj_main_ui import TJ_Main_UI
                main_ui(TJ_Main_UI(), app)
            else:
                if gol.get_value('equip_type', 0) == 12:
                    pass
                    #ui = Equip2()
                else:
                    from equip.equipmanger import EquipManger
                    from pdfparse import run
                    #################无论是否，均启动后台进程#################### 为临时解决子进程启动被UI化的问题
                    # 全局进程队列
                    gol_process_queue = Queue()
                    multiprocessing.freeze_support()
                    monitor_process = Process(target=run, args=(gol_process_queue,))
                    monitor_process.start()
                    ui = EquipManger(gol_process_queue)
                    ui.show()
                    app.exec_()
                    # 退出后台子进程
                    if monitor_process.is_alive:
                        # 停止子进程
                        monitor_process.terminate()
                        # 随主进程退出
                        monitor_process.join()
    else:
        from main.tj_main_ui import TJ_Main_UI
        main_ui(TJ_Main_UI(), app)

if __name__=="__main__":
    multiprocessing.freeze_support()
    # 启动主进程
    set_env()
    start_run()