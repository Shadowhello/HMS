from widgets.cwidget import *
from equip.model import *
from utils.base import *
from equip.equiphandle import *

# 设备检查界面
class EquipInspectUI(Widget):

    def __init__(self,parent=None):
        super(EquipInspectUI,self).__init__(parent)
        self.initPara()
        self.initUI()

    # 初始化必要参数
    def initPara(self):
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
        self.equip_entry_auto = gol.get_value('equip_entry_auto', False)

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
        layout = QHBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QHBoxLayout()
        ################# 控件区 ############################
        self.cb_auto = QCheckBox('自动录入')
        self.cb_auto.setChecked(gol.get_value('equip_entry_auto',False))
        self.tjbh=QTJBH()
        self.tjbh.setFocus(Qt.OtherFocusReason)
        self.table_inspect = EquipInspectTable(self.inspect_cols)
        # 添加布局
        layout.addWidget(self.cb_auto)
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

# 设备数据更新线程 只读取
class EquipDataThread(QThread):

    # 定义信号,定义参数为str类型
    signalPost = pyqtSignal(str)     # 更新界面
    signalExit = pyqtSignal()
    tjbh = None

    def __init__(self,queue,timer=2):
        super(EquipDataThread, self).__init__()
        self.running = True
        self.process_queue = queue
        self.timer = timer

    def stop(self):
        self.running = False

    def setStart(self,tjbh):
        self.tjbh = tjbh
        self.running = True

    def run(self):
        while self.running:
            try:
                result = self.process_queue.get()
                if result:
                    self.signalPost.emit(result)
            except Exception as e:
                print(e)
            #
            time.sleep(self.timer)


# 后台线程 处理是否自动录入
class BackGroundThread(QThread):

    # 定义信号,定义参数为str类型
    signalPost = pyqtSignal(str)     # 更新界面
    signalExit = pyqtSignal()
    tjbh = None

    def __init__(self):
        super(BackGroundThread, self).__init__()
        self.session = gol.get_value('tjxt_session_thread')
        self.log = gol.get_value('log')
        self.running = False
        # 初始化 坐标
        self.pos = {}
        self.pos['position_tj'] = gol.get_value('position_tj')
        self.pos['position_tjbh'] = gol.get_value('position_tjbh')
        self.pos['position_xm'] = gol.get_value('position_xm')
        self.pos['position_xb1'] = gol.get_value('position_xb1')
        self.pos['position_xb2'] = gol.get_value('position_xb2')
        self.pos['position_nl'] = gol.get_value('position_nl')
        self.pos['position_sure'] = gol.get_value('position_sure')
        self.pos['position_gx'] = gol.get_value('position_gx')
        self.pos['position_cj'] = gol.get_value('position_cj')

    def stop(self):
        self.running = False

    # 传递体检编号
    def setStart(self,tjbh):
        self.tjbh = tjbh
        self.running = True

    def run(self):
        while self.running:
            try:
                if self.tjbh:
                    result = self.session.execute(get_tjxx_sql(self.tjbh)).first()
                    if result:
                        tmp = {}
                        tmp['tjbh'] = result[0]
                        tmp['xm'] = str2(result[1])
                        tmp['xb'] = str2(result[2])
                        tmp['nl'] = str(result[3])
                        autoInputXDT(tmp,self.pos)
                        self.log.info('体检编号：%s,自动录入成功！' %self.tjbh)
            except Exception as e:
                self.log.info('体检编号：%s,自动录入失败,错误信息：%s' % (self.tjbh, e))
            self.running = False
            self.tjbh = None

# 设备检查：
# 线程1：自动录入：开启与关闭与否
# 线程2：更新界面状态：已上传 默认检查中
class EquipInspect(EquipInspectUI):

    def __init__(self,queue,parent=None):
        '''
        :param queue: 跨进程队列
        :param parent: 父窗口
        '''
        super(EquipInspect,self).__init__(parent)
        # 自动录入功能
        self.tjbh.returnPressed.connect(self.tjbh_validate)
        # 自动录入线程
        self.background_thread = None
        # 后台进程回传状态读取线程
        self.real_update_thread = EquipDataThread(queue)
        self.real_update_thread.signalPost.connect(self.update_state, type=Qt.QueuedConnection)
        self.real_update_thread.start()

    def update_state(self,p_tjbh):
        items = self.table_inspect.findItems(p_tjbh, Qt.MatchContains)
        for item in items:
            self.table_inspect.item(item.row(), 0).setText('已上传')
            for col_index in range(self.table_inspect.columnCount()):
                self.table_inspect.item(item.row(), col_index).setBackground(QColor("#f0e68c"))

        # mes_about(self,'获得设备端数据：%s' %p_str)

    def tjbh_validate(self):
        tjbh = self.tjbh.text()
        if  len(tjbh)==9:
            # 先判断项目是否完成
            result = self.session.query(MV_EQUIP_JCMX).filter(MV_EQUIP_JCMX.tjbh == tjbh, MV_EQUIP_JCMX.xmbh == self.equip_no).scalar()
            if result:
                # 更新界面
                self.on_table_insert(result)
                # 启动后台线程
                if self.cb_auto.isChecked():
                    self.on_thread_start(tjbh)

            else:
                mes_about(self,'体检顾客：%s,无检查项目：%s ' %(tjbh,self.equip_name))

        else:
            mes_about(self, "请输入正确的体检编号！")

        self.tjbh.setText('')
        self.tjbh.setFocus(Qt.OtherFocusReason)

    # 刷新采血列表
    def on_table_insert(self,result):
        self.table_inspect.insert2(result.to_dict)
        self.gp_inspect.setTitle('检查列表（%s）' % str(self.table_inspect.rowCount()))

    # 自动录入线程
    def on_thread_start(self,tjbh):
        if self.background_thread:
            self.background_thread.setStart(tjbh)
            self.background_thread.start()
        else:
            self.background_thread = BackGroundThread()
            self.background_thread.setStart(tjbh)
            self.background_thread.start()

    def closeEvent(self, *args, **kwargs):
        super(EquipInspect, self).closeEvent(*args, **kwargs)
        try:
            if self.background_thread:
                self.background_thread.stop()
                self.background_thread = None
            if self.real_update_thread:
                self.real_update_thread.stop()
                self.real_update_thread = None
        except Exception as e:
            self.log.info("关闭时发生错误：%s " %e)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = EquipInspectUI()
    ui.show()
    app.exec_()