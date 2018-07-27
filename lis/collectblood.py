from functools import partial
from queue import Queue
from lis.collectblood_ui import *
from lis.model import *
from utils.readparas import GolParasMixin
from utils.buildbarcode import BarCodeBuild
from utils.api import APIRquest
from utils.base import cur_datetime

# 上传队列
UPLOAD_QUEUE = Queue()

class CollectBlood(GolParasMixin,CollectBlood_UI):

    def __init__(self):
        super(CollectBlood,self).__init__("采血台")
        self.init()
        self.initParas()
        self.serialno.returnPressed.connect(self.serialno_validate)
        self.btn_take_photo.clicked.connect(self.on_btn_photo_take)

    # 初始化 页面参数
    def initParas(self):
        self.api = APIRquest(self.login_id,self.api_host,self.api_port,self.log)
        self.api_file_upload_url = gol.get_value('api_file_upload')
        results = self.session.execute(get_yblx_sql()).fetchall()
        self.yblx = dict([(str2(result[0]),result[1]) for result in  results])        # 样本类型
        results = self.session.execute(get_tmsg_sql()).fetchall()
        self.tmsg = dict([(str2(result[1]), str2(result[2])) for result in results])  # 条码试管名称
        self.barCodeBuild = BarCodeBuild(path=self.tmp_file)                          # 条形码生成器
        self.all_serialno = {}
        # 待插入的 数据对象
        self.data_obj = {'jllx':'0010','jlmc':'抽血','tjbh':'','mxbh':'',
                         'czgh':self.login_id,'czxm':self.login_name,'czqy':self.login_area,'jlnr':None,'bz':None}

        if self.camera:
            if self.camera.cap.isOpened():
                # 如果摄像头打开了，则开启上传线程
                    self.timer_upload_thread = ThreadUpload(self.api,self.api_file_upload_url,self.log)
                    #self.timer_upload_thread.signalUploadState.connect(self.refresh_upload_state, type=Qt.QueuedConnection)
                    self.timer_upload_thread.start()

    def serialno_validate(self):
        hm = self.serialno.text()
        if len(hm)<9:
            mes_about(self, "请输入正确的体检编号/条码编号！")

        elif len(hm)==9:
            # 判断当前的人条码是否都采集完毕
            # 如果不是都采集完毕，剩余是否都是尿管
            if self.refresh_ryxx(hm):
                self.refreshAllSerialNo(hm)
                # 拍照 是否应该获取历史拍照记录
                try:
                    if self.cb_is_photo.isChecked():
                        self.on_btn_photo_take()
                except Exception as e:
                    self.log.info('体检顾客：%s，拍照失败！错误信息：%s' %(hm,e))

        else:
            # 判断当前界面是否是同一人，根据体检编号判断或者当前条码记录
            if self.all_serialno:
                if hm in list(self.all_serialno.keys()):
                    # 是同一人
                    button = self.all_serialno[hm]
                    self.refreshSerial(button)
                    self.on_blood_table_insert(button)
                    self.serialno.setText('')
                    return
            # self.all_serialno 为空 说明 还未刷单，刚打开
            # hm not in list(self.all_serialno.keys()) 说明 不是同一个人
            # 与当前界面不是同一人，刷新整个过程
            tjbh = self.session.execute(get_tjbh_sql(hm)).scalar()
            if tjbh:
                if self.refresh_ryxx(tjbh):
                    self.refreshAllSerialNo(tjbh)
                    button = self.all_serialno[hm]
                    self.refreshSerial(button)
                    self.on_blood_table_insert(button)
                    # 拍照 是否应该获取历史拍照记录
                    try:
                        if self.cb_is_photo.isChecked():
                            self.on_btn_photo_take()
                    except Exception as e:
                        self.log.info('体检顾客：%s，拍照失败！错误信息：%s' %(tjbh,e))
            else:
                mes_about(self,'请输入正确的体检编号/条码编号！')

        self.serialno.setText('')

    # 刷新数据
    def refresh_ryxx(self,tjbh):
        query_result=self.session.query(MV_RYXX).filter(MV_RYXX.tjbh == tjbh).scalar()
        photo_result = self.session.query(MT_TJ_PHOTO).filter(MT_TJ_PHOTO.tjbh == tjbh).scalar()
        if photo_result:
            #filename = os.path.join(gol.get_value('path_tmp'),'%s_sfz.jpg' %tjbh)
            self.lb_pic.show2(photo_result.picture)
        else:
            self.lb_pic.setText('身\n份\n证\n照\n片')

        if query_result:
            # 刷新人员信息
            self.user_id.setText(query_result.tjbh)
            self.user_name.setText(str2(query_result.xm))
            self.user_sex.setText(str2(query_result.xb))
            self.user_age.setText('%s 岁' %str(query_result.nl))
            # self.depart.setText(str2(query_result.depart))
            self.dwmc.setText(str2(query_result.dwmc))
            # self.tj_qdrq.setText(query_result.qdrq)
            self.sjhm.setText(query_result.sjhm)
            self.sfzh.setText(query_result.sfzh)
            # self.tj_djrq.setText(query_result.djrq)

            # 特殊项目提醒
            results = dict(self.session.query(MT_TJ_TJJLMXB.xmbh,MT_TJ_TJJLMXB.xmmc).filter(MT_TJ_TJJLMXB.tjbh == tjbh).all())
            xmbhs = results.keys()
            if list_in_list(['501722','501702'],xmbhs):
                self.widget1 = PreviewWidget('该顾客有前列腺彩超，请您提醒：做完前列腺彩超后，再进行留尿！')
                self.serialno.setFocus()

            if list_in_list(['5004','5001'],xmbhs):
                self.widget2 = PreviewWidget('该顾客有C13/C14，请您提醒：先留尿，再做C13/C14吹气！')
                self.serialno.setFocus()

            if list_in_list(['1103','1104','1105','1106','1107'],xmbhs):
                self.widget3 = PreviewWidget('该顾客有餐后血糖（OGTT），请您提醒：先留尿，再喝糖水！')
                self.serialno.setFocus()

            return True
        else:
            mes_about(self,'请输入正确的体检编号/条码编号！')

    # 刷新所有条码信息
    def refreshAllSerialNo(self,tjbh):
        # 销毁 旧的 按钮组
        while self.layout3.count():
            item = self.layout3.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
        while self.layout4.count():
            item = self.layout4.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
        while self.layout5.count():
            item = self.layout5.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
        #############初始化#####################
        size=5
        tm_num = 0          # 总数量
        cx_num = 0          # 抽血数量
        cx_done_num =0      # 抽血/留样完成的数量
        ly_num = 0          # 留样数量
        jj_num = 0          # 拒检数量

        # 获取条码信息
        results = self.session.execute(get_tmxx_sql(tjbh)).fetchall()
        for i,result in enumerate(results):
            # 获取条码属性
            btn_no = result[1]          # 条码号
            btn_name = result[2]        # 条码对应项目组
            btn_state = result[-2]      # 条码状态：是否已抽、已采集
            btn_state2 = result[-1]      # 条码状态：是否已拒检
            # 生成按钮
            if not btn_state:
                filename=self.barCodeBuild.create(btn_no)       # 采集过就变色
            else:
                filename = self.barCodeBuild.alter(btn_no)      # 未采集就不变色
                # 如果不是 拒检 则计算 抽血
                if not bool(btn_state2):
                    cx_done_num = cx_done_num +1

            button = SerialNoButton(filename, btn_name)
            # 添加按钮
            self.all_serialno[btn_no] = button
            # 更新按钮属性
            button.setCollectNo(btn_no)                     # 采集号码
            button.setCollectTJBH(tjbh)                     # 采集号码
            button.setCollectState(bool(btn_state))         # 采集状态
            button.setCollectCancle(bool(btn_state2))       # 拒检状态
            # 设置右键
            button.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
            button.customContextMenuRequested.connect(partial(self.onSerialNoBtnMenu,button))  ####右键菜单
            # 存储试管颜色
            button.setCollectColor(self.tmsg.get(btn_name.split()[0],'未知'))
            # 根据样本类型：拒检，未拒检，再分 抽血、留样，分到不同的位置
            if button.collectCancle:
                # 获取坐标
                btn_pos_x = jj_num // size
                btn_pos_y = jj_num % size
                # 更新按钮属性
                button.setCollectPos(btn_pos_x, btn_pos_y)
                button.setCollectType(False)
                # 添加布局
                self.layout5.addWidget(button, btn_pos_x, btn_pos_y, 1, 1)
                jj_num = jj_num + 1
            else:
                if self.yblx.get(btn_name.split()[0],0) in [0,'1','4','5']:           # 修复
                    # 获取坐标
                    btn_pos_x = cx_num // size
                    btn_pos_y = cx_num % size
                    # 更新按钮属性
                    button.setCollectPos(btn_pos_x,btn_pos_y)
                    button.setCollectType(False)
                    # 添加布局
                    self.layout3.addWidget(button, btn_pos_x, btn_pos_y, 1, 1)
                    # 更新
                    cx_num = cx_num + 1
                else:
                    # 获取 坐标
                    btn_pos_x = ly_num // size
                    btn_pos_y = ly_num % size
                    # 更新按钮属性
                    button.setCollectPos(btn_pos_x,btn_pos_y)
                    button.setCollectType(True)
                    # 添加布局
                    self.layout4.addWidget(button, btn_pos_x, btn_pos_y, 1, 1)
                    # 更新
                    ly_num = ly_num + 1

            # 条码总数量
            tm_num = tm_num + 1

        self.layout3.setHorizontalSpacing(10)               # 设置水平间距
        self.layout3.setVerticalSpacing(10)                 # 设置垂直间距
        self.layout3.setContentsMargins(10, 10, 10, 10)     # 设置外间距
        self.layout3.setColumnStretch(5, 1)                 # 设置列宽，添加空白项的

        self.layout4.setHorizontalSpacing(10)               # 设置水平间距
        self.layout4.setVerticalSpacing(10)                 # 设置垂直间距
        self.layout4.setContentsMargins(10, 10, 10, 10)     # 设置外间距
        self.layout4.setColumnStretch(5, 1)                 # 设置列宽，添加空白项的

        self.layout5.setHorizontalSpacing(10)               # 设置水平间距
        self.layout5.setVerticalSpacing(10)                 # 设置垂直间距
        self.layout5.setContentsMargins(10, 10, 10, 10)     # 设置外间距
        self.layout5.setColumnStretch(5, 1)                 # 设置列宽，添加空白项的

        self.ser_all.setText("%s" % str(tm_num))
        self.ser_cx.setText("%s" % str(cx_num))
        self.ser_ly.setText("%s" % str(ly_num))
        self.ser_jj.setText("%s" % str(jj_num))
        self.ser_done.setText("%s" % str(cx_done_num))
        self.ser_undone.setText("%s" % str(tm_num-cx_done_num-jj_num))

    # 判断是否是第二次刷条码，对方法 refreshSerialNo 进行封装
    def refreshSerial(self,button):
        # 已采集
        if button.collectState:
            dialog = mes_warn(self, '该条码已采集，是否重新扫码采集？')
            if dialog == QMessageBox.Yes:
                self.refreshSerialNo(button)
        else:
            self.refreshSerialNo(button)

    # 刷新 条形码 UI
    # 刷新 数据：采集状态，采集时间、采集人、采集地点
    def refreshSerialNo(self,button:SerialNoButton):
        # 如果是拒检的条码，则不允许扫描
        if button.collectCancle:
            mes_about(self,'该条码已拒检，不允许扫描！')
            return
        # 获取旧条码 信息
        btn_name = button.collectTxt       # 原条码 项目文本
        btn_no = button.collectNo          # 原条码 号码
        btn_tjbh = button.collectTJBH      # 原条码 体检编号
        btn_pos_x =button.collectPos_X     # 原条码 X 位置
        btn_pos_y = button.collectPos_Y    # 原条码 Y 位置
        btn_type = button.collectType      # 原条码 采集类型
        btn_color = button.collectColor    # 原条码 采集类型
        # 根据旧的 创建生成 新的
        filename = self.barCodeBuild.alter(btn_no)
        button2 = SerialNoButton(filename, btn_name)
        # 更新 按钮属性
        button2.setCollectState(True)
        button2.setCollectNo(btn_no)
        button2.setCollectTJBH(btn_tjbh)
        button2.setCollectType(btn_type)
        button2.setCollectPos(btn_pos_x,btn_pos_y)
        button2.setCollectColor(btn_color)
        # 设置右键
        button2.setContextMenuPolicy(Qt.CustomContextMenu)                                    ######允许右键产生子菜单
        button2.customContextMenuRequested.connect(partial(self.onSerialNoBtnMenu, button2))  ####右键菜单
        # 更新 容器
        self.all_serialno[btn_no] = button2
        # 从UI布局中 删除旧的 添加 新的
        if not btn_type:
            self.layout3.removeWidget(button)
            button.hide()                      # 对象隐藏，如何销毁呢？？？
            self.layout3.addWidget(button2, btn_pos_x, btn_pos_y, 1, 1)
        else:
            self.layout4.removeWidget(button)
            button.hide()
            self.layout4.addWidget(button2, btn_pos_x, btn_pos_y, 1, 1)
        # 更新界面UI
        self.ser_done.setText("%s" % str(int(self.ser_done.text())+1))
        self.ser_undone.setText("%s" % str(int(self.ser_undone.text())-1))
        # 刷新 入库
        self.data_obj['tjbh'] = self.user_id.text()
        self.data_obj['mxbh'] = btn_no
        self.data_obj['jlnr'] = btn_name
        self.data_obj['bz'] = btn_color
        # 采血处可能也扫 留样管
        if btn_type:
            self.data_obj['jllx'] = '0011'
            self.data_obj['jlmc'] = '留样'
        try:
            self.session.bulk_insert_mappings(MT_TJ_CZJLB, [self.data_obj])
            self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == self.user_id.text(),MT_TJ_TJJLMXB.tmbh1 == btn_no).update({MT_TJ_TJJLMXB.zxpb:'4'})
            self.session.commit()
        except Exception as e:
            mes_about(self,'插入 TJ_CZJLB 记录失败！错误代码：%s' %e)

    def onSerialNoBtnMenu(self,button,pos):
        menu = QMenu()
        item1 = menu.addAction(Icon("取消"), "取消")
        item2 = menu.addAction(Icon("拒检"), "拒检")
        item3 = menu.addAction(Icon("print"), "打印")
        # 按是否已采集过区分按钮
        if not button.collectState:
            item1.setVisible(False)
        else:
            item1.setVisible(True)

        action = menu.exec_(button.mapToGlobal(pos))
        # 按钮功能
        if action == item1:
            dialog = mes_warn(self, "当前条码已抽血，是否取消该次扫描工作！" )
            if dialog == QMessageBox.Yes:
                qxbz = '取消当前条码扫描，操作人：%s，操作时间：%s，操作区域：%s 。' %(self.login_name,cur_datetime(),self.login_area)
                try:
                    self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.tjbh == button.collectTJBH,
                                                           MT_TJ_CZJLB.mxbh == button.collectNo).update({MT_TJ_CZJLB.jllx: '0000',MT_TJ_CZJLB.bz: qxbz})
                    self.session.commit()
                except Exception as e:
                    mes_about(self,'取消该条码出错！错误信息：%s' %e)
            else:
                pass

        elif action == item2:
            try:
                self.session.execute(get_xmjj_sql(button.collectTJBH,button.collectNo,self.login_id,self.login_name,self.login_area))
                self.session.commit()
            except Exception as e:
                mes_about(self,'拒检失败！错误代码：%s' %e)
        if action == item3:
            pass
            # mes_about(self,'此功能未开放！')
        else:
            pass

    # 拍照
    def on_btn_photo_take(self):
        if self.camera:
            if self.user_id.text():
                file_photo = image_file(self.user_id.text())
                img = self.camera.onTakeImage(file_photo)
                self.photo_lable.setPixmap(QPixmap.fromImage(img, Qt.AutoColor))
                #self.on_status_widget_show('拍照完成') 发射信号
                UPLOAD_QUEUE.put(file_photo)
            else:
                mes_about(self,'请扫描体检编号或者条码号！')
        else:
            pass
            #mes_about(self,'摄像头功能未打开，无法拍照！')

    # 刷新采血列表
    def on_blood_table_insert(self,button:SerialNoButton):
        data=['已抽血',button.collectNo,self.user_id.text(),self.user_name.text(),self.user_sex.text(),self.user_age.text(),button.collectTxt]
        self.blood_table.insert(data)
        self.left_down_gp.setTitle('采血列表（%s）' % str(self.blood_table.rowCount()))

    def closeEvent(self, *args, **kwargs):
        try:
            if self.camera:
                self.camera.deleteLater()
            if self.timer_upload_thread:
                self.timer_upload_thread.stop()
        except Exception as e:
            print(e)
        super(CollectBlood, self).closeEvent(*args, **kwargs)


class ThreadUpload(QThread):
    # 定义信号,定义参数为str类型
    # signalUploadState = pyqtSignal(bool,str)  # 上传状态，体检标识
    # signalPost = pyqtSignal(dict)     # 更新界面
    signalExit = pyqtSignal()

    def __init__(self,api,api_url,log,timer=2):
        super(ThreadUpload, self).__init__()
        self.running = True
        self.timer = timer
        self.log = log
        self.api = api
        self.api_url = api_url

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            time.sleep(self.timer)
            try:
                item=UPLOAD_QUEUE.get_nowait()
                self.log.info('后台线程，提取队列数据：%s 上传！' %item)
            except Exception as e:
                item = None
            if item:
                response = self.api.request(self.api_url,'post',filename=item)
                print(response)
                # if response:
                #     # 更新
                #     self.signalUploadState.emit(True, item['jglr_tjbs'])
                # else:
                #     self.signalUploadState.emit(False, item['jglr_tjbs'])

def list_in_list(a_list,b_list):
    for i in a_list:
        if i in b_list:
            return True

    return False

def image_file(tjbh):
    filename=os.path.join('%s' %gol.get_value('path_tmp') ,'%s_000001.%s' %(tjbh,gol.get_value('photo_save_type')))
    return filename

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = CollectBlood()
    ui.show()
    app.exec_()