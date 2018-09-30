from widgets.cwidget import *

class TJ_MYD_UI(Widget):

    def __init__(self,parent=None):
        super(TJ_MYD_UI,self).__init__(parent)
        self.initUI()

    def initUI(self):
        lt_main = QVBoxLayout()
        for title in ['预约排程','体检流程','专业水平','医护服务','早餐服务']:
            gp_score = OptionGroup(title)
            lt_main.addWidget(gp_score)
        # gp_suggest
        lt_main.addStretch()
        self.setLayout(lt_main)

class OptionGroup(QGroupBox):

    def __init__(self,title):
        super(OptionGroup,self).__init__()
        lt_main = QVBoxLayout()
        self.setTitle(title)
        lt_score = QHBoxLayout()
        for i in range(6):
            btn_score = QRadioButton(str(i))
            lt_score.addWidget(btn_score)
            if i==5:
                btn_score.setChecked(True)

        lt_main.addLayout(lt_score)
        self.setLayout(lt_main)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = TJ_MYD_UI()
    ui.showMaximized()
    app.exec_()