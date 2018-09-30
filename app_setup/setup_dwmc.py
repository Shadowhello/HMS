from widgets.cwidget import *
from app_setup.model import *

class SetupDwmc(Dialog):

    def __init__(self,parent=None):
        super(SetupDwmc,self).__init__(parent)
        self.initUI()
        self.initParas()

    def initParas(self):
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()
        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)

        self.lt_dwmc.setValues(self.dwmc_bh,self.dwmc_py)

    def initUI(self):
        lt_main = QVBoxLayout()
        ####################################
        lt_top = QVBoxLayout()
        gp_top = QGroupBox()
        self.lt_dwmc = TUintGroup({},{})
        lt_top.addLayout(self.lt_dwmc)
        gp_top.setLayout(lt_top)
        ####################################
        lt_middle = QHBoxLayout()
        gp_middle = QGroupBox()
        self.lw_dwmc_all = QListWidget()
        self.lw_dwmc_user = QListWidget()

        lt_middle.addWidget(self.lw_dwmc_all)
        lt_middle.addWidget(self.lw_dwmc_user)
        gp_middle.setLayout(lt_middle)

        lt_main.addWidget(gp_top)
        lt_main.addWidget(gp_middle)

        self.setLayout(lt_main)



if __name__=="__main__":
    from utils.envir import *
    set_env()
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    ui = SetupDwmc()
    ui.show()
    ui.exec_()