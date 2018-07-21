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

    # from equip_dr import Equip2
    from login.login_ui import Login_UI
    from PyQt5.QtWidgets import QApplication
    import sys
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
                    from multiprocessing import Process, Queue
                    # 全局进程队列
                    gol_process_queue = Queue()
                    Process(target=run, args=(gol_process_queue,)).start()
                    ui = EquipManger(gol_process_queue)
                    ui.show()
                    app.exec_()






    else:
        from main.tj_main_ui import TJ_Main_UI
        main_ui(TJ_Main_UI(), app)

if __name__=="__main__":
    # 启动主进程
    set_env()
    start_run()