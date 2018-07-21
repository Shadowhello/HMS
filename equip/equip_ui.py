from widgets.cwidget import *
from equip.model import *
from utils.base import *

# 设备检查
class EquipInspect(Widget):

    def __init__(self,queue,parent=None):
        super(EquipInspect,self).__init__(parent)
        self.process_queue =queue
        self.inspect_cols = OrderedDict(
            [
                ("state","状态"),
                ("xmmc", "项目名称"),
                ("tjbh","体检编号"),
                ("xm","姓名"),
                ("xb","性别"),
                ("nl", "年龄")
             ])
        self.equip_type = str(gol.get_value('equip_type', '00')).zfill(2)
        self.equip_no = EquipNo.get(self.equip_type, '')
        self.equip_name = EquipName.get(self.equip_type, '')
        self.equip_action = EquipAction.get(self.equip_type, '')
        self.initUI()
        self.tjbh.returnPressed.connect(self.tjbh_validate)
        #
        self.timer_update_thread = EquipDataThread(self.process_queue)
        self.timer_update_thread.signalPost.connect(self.update_mes, type=Qt.QueuedConnection)
        self.timer_update_thread.start()

    def update_mes(self,p_str):
        mes_about(self,'获得设备端数据：%s' %p_str)

    def initUI(self):
        # 位置大小等
        window_x=QApplication.desktop().width()-330
        window_y=QApplication.desktop().height()-150
        self.setGeometry(window_x,100,300, window_y)
        self.setWindowTitle("明州体检")
        self.setWindowIcon(Icon('mztj'))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # 布局
        lt_main = QVBoxLayout(self)
        group1 = QGroupBox("体检编号")
        self.gp_inspect = QGroupBox("检查列表(0)")
        group3 = QGroupBox()
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QHBoxLayout()

        ################# 控件区 ############################
        self.tjbh=QTJBH()
        self.table_inspect = TableWidget(self.inspect_cols)

        # 添加布局
        layout.addWidget(self.tjbh)
        layout2.addWidget(self.table_inspect)
        layout2.addLayout(layout1)
        layout3.addWidget(QLabel("登录工号：%s" %self.login_id))
        layout3.addWidget(QLabel("登录用户：%s" % self.login_name))
        group1.setLayout(layout)
        self.gp_inspect.setLayout(layout2)
        group3.setLayout(layout3)
        lt_main.addWidget(group1)
        lt_main.addWidget(self.gp_inspect)
        lt_main.addWidget(group3)
        self.setLayout(lt_main)

    def tjbh_validate(self):
        tjbh = self.tjbh.text()
        if  len(tjbh)==9:
            # 先判断项目是否完成
            result = self.session.query(MV_EQUIP_JCMX).filter(MV_EQUIP_JCMX.tjbh == tjbh, MV_EQUIP_JCMX.xmbh == self.equip_no).scalar()
            if result:
                self.table_inspect.insert(result.to_dict)
                self.gp_inspect.setTitle('留样列表（%s）' % str(self.table_inspect.rowCount()))
            else:
                mes_about(self,'体检顾客：%s,无检查项目：%s ' %(tjbh,self.equip_name))
            # result = self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.tjbh == tjbh,MT_TJ_CZJLB.mxbh==self.equip_no,MT_TJ_CZJLB.jllx==self.equip_action).scalar()
            # if not result:
                # 插入动作记录表



        else:
            mes_about(self, "请输入正确的体检编号！")

        self.tjbh.setText('')

    # 刷新采血列表
    def on_table_urine_insert(self,button:SerialNoButton):
        data=['检查中',button.collectNo,button.collectTJBH,button.collectTxt]
        self.table_urine.insert(data)
        self.gp_inspect.setTitle('留样列表（%s）' % str(self.table_inspect.rowCount()))

# 设备数据更新线程
class EquipDataThread(QThread):

    # 定义信号,定义参数为str类型
    signalPost = pyqtSignal(str)     # 更新界面
    signalExit = pyqtSignal()

    def __init__(self,queue,timer=2):
        super(EquipDataThread, self).__init__()
        self.running = True
        self.process_queue = queue
        self.timer = timer

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            print('后台线程已启动。。。')
            try:
                result = self.process_queue.get()
                print(result)
                if result:
                    self.signalPost.emit('获得数据：%s' %result)
            except Exception as e:
                print(e)
            time.sleep(self.timer)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = EquipInspect()
    ui.show()
    app.exec_()