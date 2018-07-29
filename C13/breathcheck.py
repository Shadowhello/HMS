from C13.breathcheck_ui import *
from C13.model import *

class BreathCheck(BreathCheckUI):

    def __init__(self,parent=None):
        super(BreathCheck,self).__init__(parent)
        self.initDatas()

    def initDatas(self):
        result = self.session.execute(get_nocheck_sql()).fetchall()
        self.table_c13_nocheck.load_set(result)
        self.gp_left.setTitle('1、待测：总人数 %s 人' %str(self.table_c13_nocheck.rowCount()))
        self.lb_update.setText(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = BreathCheck()
    ui.show()
    app.exec_()