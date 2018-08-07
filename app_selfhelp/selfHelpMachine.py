from widgets.cwidget import *
from utils import gol

# 自助机
class SelfHelpMachine(Widget):

    def __init__(self,parent=None):
        super(SelfHelpMachine,self).__init__(parent)
        # 载入样式
        self.stylesheet = file_style(gol.get_value('file_qss', 'mztj.qss'))
        with open(self.stylesheet) as f:
            self.setStyleSheet(f.read())
        self.setWindowTitle('明州体检')
        self.setWindowIcon(Icon('mztj'))
        self.initUI()
        # 绑定信号槽
        self.le_tjbh.returnPressed.connect(self.on_le_tjbh_press)
        self.btn_sfz.clicked.connect(self.on_btn_sfz_read)
        self.btn_keyboard.clicked.connect(self.on_btn_keyboard_click)
        # 特殊变量
        self.gp_keyboard = None       #键盘区域

    def initUI(self):
        lt_main = QHBoxLayout(self)
        lt_top = QHBoxLayout()
        lt_middle1 = QHBoxLayout()
        lt_middle2 = QHBoxLayout()
        lt_middle3 = QHBoxLayout()
        lt_middle = QHBoxLayout()
        lt_bottom = QHBoxLayout()
        self.le_tjbh = QTJBH()
        self.btn_keyboard = QPushButton(Icon('键盘'),'')
        self.btn_keyboard.setIconSize(QSize(32,32))
        self.btn_sfz = QPushButton('读身份证')
        lt_middle2.addWidget(self.le_tjbh)
        lt_middle2.addWidget(self.btn_keyboard)
        lt_middle2.addWidget(self.btn_sfz)
        lt_middle.addStretch()
        lt_middle.addLayout(lt_middle1, 1)
        lt_middle.addStretch()
        lt_middle.addLayout(lt_middle2, 1)
        lt_middle.addStretch()
        lt_middle.addLayout(lt_middle3, 1)
        # 添加布局
        lt_main.addLayout(lt_top,1)
        lt_main.addLayout(lt_middle,1)
        lt_main.addLayout(lt_bottom,1)
        self.setLayout(lt_main)

    # 扫描体检编号或者手工输入回车
    def on_le_tjbh_press(self):
        pass

    # 读身份证号
    def on_btn_sfz_read(self):
        dialog = ReadChinaIdCard_UI(self)
        dialog.sendIdCard.connect(self.setData)
        dialog.exec_()

    # 读取后设置身份证号
    def setData(self,idCard:str):
        # 设置身份证号
        self.le_tjbh.setText(idCard)
        # 检索
        self.on_le_tjbh_press()

    # 数字小键盘，用于手工输入内容
    def on_btn_keyboard_click(self):
        if not self.gp_keyboard:
            rect=self.le_tjbh.geometry()
            width = rect.width()
            bottom = rect.bottom()
            left = rect.left()

            # 数字 字母 中文
            btn_names = ['ESC','0','1','2','3','4','5','6','7','8','9','搜索']
            # 一行几个按钮
            size = 3
            height = 300
            self.gp_keyboard = QGroupBox(self)
            lt_keyboard = QGridLayout()
            for i,btn_name in enumerate(btn_names):
                # 获取坐标
                btn_pos_x = i // size
                btn_pos_y = i % size
                # 初始化按钮
                btn_obj = QPushButton(btn_name)
                btn_obj.setMinimumWidth(width//10)
                btn_obj.setFixedHeight(height//4)
                btn_obj.setStyleSheet('''font: 75 28pt \"微软雅黑\";''')
                # 添加布局
                btn_obj.clicked.connect(partial(self.on_btn_obj_click,btn_name))
                lt_keyboard.addWidget(btn_obj, btn_pos_x, btn_pos_y, 1, 1)


            lt_keyboard.setHorizontalSpacing(10)               # 设置水平间距
            lt_keyboard.setVerticalSpacing(10)                 # 设置垂直间距
            lt_keyboard.setContentsMargins(10, 10, 10, 10)     # 设置外间距
            #lt_keyboard.setColumnStretch(5, 1)                 # 设置列宽，添加空白项的

            self.gp_keyboard.setLayout(lt_keyboard)
            self.gp_keyboard.setGeometry(QRect(left,bottom,width,height))
        self.gp_keyboard.show()

    # 数字键盘信号槽
    def on_btn_obj_click(self,btn_name):
        if btn_name=='ESC':
            self.gp_keyboard.hide()
        elif btn_name=='搜索':
            # 先隐藏
            self.gp_keyboard.hide()
            # 后检索
            self.on_le_tjbh_press()
        else:
            self.le_tjbh.setText(self.le_tjbh.text()+btn_name)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = SelfHelpMachine()
    ui.showMaximized()
    app.exec_()
