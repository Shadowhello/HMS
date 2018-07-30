from widgets.cwidget import *

class BreathCheckUI(Widget):

    def __init__(self,parent=None):
        super(BreathCheckUI,self).__init__(parent)
        self.c13_cols = OrderedDict(
            [
                ("tjbh","体检编号"),
                ("xm","姓名"),
                ("xb","性别"),
                ("nl", "年龄"),
                ("xmmc", "项目名称"),
                ("tjqy", "体检区域")
             ])
        self.c13_cols2 = OrderedDict(
            [
                ("tjbh","体检编号"),
                ("xm","姓名"),
                ("xb","性别"),
                ("nl", "年龄"),
                ("xmmc", "项目名称"),
                ("tjqy", "体检区域"),
                ("time", "倒计时"),
                ("s_time", "计时开始时间"),
                ("e_time", "计时结束时间")
             ])
        self.initUI()

    def initUI(self):
        lt_main = QHBoxLayout()
        lt_right = QVBoxLayout()
        lt_right_down = QHBoxLayout()
        # 初始化
        self.initUILeft()
        self.initUIRightUp()
        self.initUIRightMiddle()
        self.initUIRightDown()
        # 子布局

        lt_right_down.addWidget(self.gp_right_down_1)
        lt_right_down.addWidget(self.gp_right_down_2)
        lt_right.addLayout(self.lt_up, 1)
        lt_right.addWidget(self.gp_right_up, 5)
        lt_right.addLayout(lt_right_down,5)
        # 主布局
        lt_main.addWidget(self.gp_left,1)
        lt_main.addLayout(lt_right,3)
        #
        self.setLayout(lt_main)


    def initUILeft(self):
        # 控件
        self.lb_update = QLabel()
        self.btn_update = QPushButton(Icon('刷新'),'刷新')
        self.table_c13_nocheck = C13InspectTable(self.c13_cols)
        self.table_c13_nocheck.setAlternatingRowColors(False)
        self.table_c13_nocheck.verticalHeader().setVisible(False)  # 列表头
        self.gp_left = QGroupBox('1、待测：总人数 0 人')
        lt_1 = QHBoxLayout()
        lt_1.addWidget(QLabel('刷新时间：'))
        lt_1.addWidget(self.lb_update)
        lt_1.addWidget(self.btn_update)
        lt_left = QVBoxLayout()
        lt_left.addLayout(lt_1)
        lt_left.addWidget(self.table_c13_nocheck)
        self.gp_left.setLayout(lt_left)

    def initUIRightUp(self):
        self.lt_up = QHBoxLayout()
        self.le_tjbh = QTJBH()
        self.lt_up.addWidget(QLabel('体检编号：'))
        self.lt_up.addWidget(self.le_tjbh)

    def initUIRightMiddle(self):
        self.table_c13_checking_1 = C13InspectTable(self.c13_cols2)
        self.table_c13_checking_1.verticalHeader().setVisible(False)  # 列表头
        self.gp_right_up = QGroupBox('2、吃药丸 计时中：总人数 0')
        ###########################
        lt_right_up = QVBoxLayout()
        lt_right_up.addWidget(self.table_c13_checking_1)
        self.gp_right_up.setLayout(lt_right_up)

    def initUIRightDown(self):
        # 计时完成，待吹气
        self.table_c13_checking_2 = C13InspectTable(self.c13_cols)
        self.table_c13_checking_2.verticalHeader().setVisible(False)  # 列表头
        self.gp_right_down_1 = QGroupBox('3、计时完成待吹气：总人数 0')
        lt_right_1 = QHBoxLayout()
        # 布局
        lt_right_1.addWidget(self.table_c13_checking_2)
        self.gp_right_down_1.setLayout(lt_right_1)
        # 吹气完成的
        self.table_c13_checked = C13InspectTable(self.c13_cols)
        self.table_c13_checked.verticalHeader().setVisible(False)  # 列表头
        self.gp_right_down_2 = QGroupBox('4、完成吹气：总人数 0')
        lt_right_2 = QHBoxLayout()
        ## 布局
        lt_right_2.addWidget(self.table_c13_checked)
        self.gp_right_down_2.setLayout(lt_right_2)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = BreathCheckUI()
    ui.show()
    app.exec_()
