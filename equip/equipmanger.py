from equip.equip_ui import *
from equip.model import *
from functools import partial

class EquipMager(DirTabWidget):

    def __init__(self,parent=None):
        super(EquipMager,self).__init__(parent)

class EquipManger(EquipInspect):

    def __init__(self,mes_queue):
        super(EquipManger,self).__init__(mes_queue)
        # self.num=num
        # self.refresh_data()
        #定时器
        # self.timer = QTimer(self)
        # self.timer.start(1000)
        # self.timer.timeout.connect(self.refresh_timer)

        # self.btn_all.clicked.connect(partial(self.seek, 3))
        # self.btn_check.clicked.connect(partial(self.seek, 2))
        # self.btn_uncheck.clicked.connect(partial(self.seek, 1))
        # self.btn_self.clicked.connect(partial(self.seek, 0))

        # self.table_check.horizontalHeader().sectionClicked.connect(self.shows)

    def shows(self,p_int):
        print(list(self.cols.values())[p_int])

    # 筛选
    def seek(self,p_int):
        finish_states = ['已拒检', '已小结']
        unfinish_states = ['核实', '已回写','已登记','已检查','未结束']
        if p_int == 0:
            # 显示自己完成的，
            self.table_check.rowsHide(unfinish_states,self.login_id)
        elif p_int == 1:
            # 显示 未完成的，即 隐藏完成的
            self.table_check.rowsHide(finish_states)
        elif p_int == 2:
            # 显示完成的，即隐藏未完成的
            self.table_check.rowsHide(unfinish_states)
        else:
            self.table_check.rowsHide([])


    # 定时刷新器
    def refresh_timer(self):
        if self.num==0:
            self.num = 30
            self.refresh_data()
        else:
            self.num=self.num-1
            self.lable_timer.setText("刷新倒计时：%s s" %str(self.num))

    # 刷新数据
    def refresh_data(self):
        count = 0
        count_finish = 0
        count_unfinish = 0

        query_results=self.session.query(MV_EQUIP_JCMX).filter(MV_EQUIP_JCMX.xmbh == '0806').all()
        results=[]
        for result in query_results:
            count = count +1
            if result.state in ['已拒检','已小结','已检查']:
                count_finish = count_finish+1
            else:
                count_unfinish = count_unfinish + 1

            results.append(result.dict())

        # self.table_inspect.load(self.inspect_cols,count,results)

        # self.btn_all.setText("所有(%s)" %count)
        # self.btn_check.setText("已检查(%s)" % count_finish)
        # self.btn_uncheck.setText("未检查(%s)" % count_unfinish)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = EquipManger()
    ui.show()
    app.exec_()