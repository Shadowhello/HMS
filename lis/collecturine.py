from lis.collecturine_ui import *

class CollectUrine(CollectUrine_UI):

    def __init__(self):

        super(CollectUrine,self).__init__()
        self.initParas()
        self.tmbh.returnPressed.connect(self.serialno_validate)
        # self.tmbh.returnPressed.connect(self.on_table_urine_insert)

    # 初始化参数
    def initParas(self):
        results = self.session.execute(get_yblx_sql()).fetchall()
        self.yblx = dict([(str2(result[0]),result[1]) for result in results])
        self.barCodeBuild = BarCodeBuild(path=self.tmp_file)                      # 条形码生成器
        self.all_serialno = {}
        # 待插入的 数据对象
        self.data_obj = {'jllx':'0010','jlmc':'抽血','tjbh':'','mxbh':'',
                         'czgh':self.login_id,'czxm':self.login_name,'czqy':self.login_area,'jlnr':None}



    # 留样台  属于无人管理区，顾无对话框
    def serialno_validate(self):
        hm = self.tmbh.text()
        # 判断当前界面是否是同一人，根据体检编号判断或者当前条码记录
        if self.all_serialno:
            if hm in list(self.all_serialno.keys()):
                # 是同一人
                button = self.all_serialno[hm]
                self.refreshSerial(button)
                self.on_table_urine_insert(button)
                self.tmbh.setText('')
                return
        # self.all_serialno 为空 说明 还未刷单，刚打开
        # hm not in list(self.all_serialno.keys()) 说明 不是同一个人
        # 与当前界面不是同一人，刷新整个过程
        tjbh = self.session.execute(get_tjbh_sql(hm)).scalar()
        if tjbh:
            self.refreshAllSerialNo(tjbh)
            button = self.all_serialno[hm]
            self.refreshSerial(button)
            self.on_table_urine_insert(button)

        self.tmbh.setText('')

    # 判断是否是第二次刷条码，对方法 refreshSerialNo 进行封装
    def refreshSerial(self,button):
        # 已采集
        if button.collectState:
            pass
            # 已采集则跳过
            # dialog = mes_warn(self, '该条码已采集，是否重新扫码采集？')
            # if dialog == QMessageBox.Yes:
            #     self.refreshSerialNo(button)
        else:
            self.refreshSerialNo(button)

    # 刷新所有条码信息
    def refreshAllSerialNo(self, tjbh):
        # 销毁 旧的 按钮组
        while self.lt_left_bottom.count():
            item = self.lt_left_bottom.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
        #############初始化#####################
        size = 5
        tm_num = 0  # 总数量
        cx_num = 0  # 抽血数量
        cx_done_num = 0  # 抽血/留样完成的数量
        ly_num = 0  # 留样数量

        # 获取条码信息
        results = self.session.execute(get_tmxx_sql(tjbh)).fetchall()
        for i, result in enumerate(results):
            # 获取条码属性
            btn_no = result[1]
            btn_name = result[2]
            btn_state = result[-1]
            # 生成按钮
            if not btn_state:
                filename = self.barCodeBuild.create(btn_no)
            else:
                filename = self.barCodeBuild.alter(btn_no)
                cx_done_num = cx_done_num + 1

            button = SerialNoButton(filename, btn_name)
            # 添加按钮
            self.all_serialno[btn_no] = button
            # 更新按钮属性
            button.setCollectNo(btn_no)  # 采集号码
            button.setCollectTJBH(tjbh)  # 采集号码
            button.setCollectState(bool(btn_state))  # 采集状态

            # 根据样本类型，分到不同的位置
            if self.yblx.get(btn_name.strip(), 0) in [0, '1', '4', '5']:
                pass
            else:
                # 获取 坐标
                btn_pos_x = ly_num // size
                btn_pos_y = ly_num % size
                # 更新按钮属性
                button.setCollectPos(btn_pos_x, btn_pos_y)
                button.setCollectType(True)
                # 添加布局
                self.lt_left_bottom.addWidget(button, btn_pos_x, btn_pos_y, 1, 1)
                # 更新
                ly_num = ly_num + 1

            # 条码总数量
            tm_num = tm_num + 1

        self.lt_left_bottom.setHorizontalSpacing(10)  # 设置水平间距
        self.lt_left_bottom.setVerticalSpacing(10)  # 设置垂直间距
        self.lt_left_bottom.setContentsMargins(10, 10, 10, 10)  # 设置外间距
        self.lt_left_bottom.setColumnStretch(5, 1)  # 设置列宽，添加空白项的

    # 刷新 条形码 UI
    # 刷新 数据：采集状态，采集时间、采集人、采集地点
    def refreshSerialNo(self,button):
        # 获取旧条码 信息
        btn_name = button.collectTxt       # 原条码 项目文本
        btn_no = button.collectNo          # 原条码 号码
        btn_tjbh = button.collectTJBH      # 原条码 体检编号
        btn_pos_x =button.collectPos_X     # 原条码 X 位置
        btn_pos_y = button.collectPos_Y    # 原条码 Y 位置
        btn_type = button.collectType      # 原条码 采集类型
        # 根据旧的 创建生成 新的
        filename = self.barCodeBuild.alter(btn_no)
        button2 = SerialNoButton(filename, btn_name)
        # 更新 按钮属性
        button2.setCollectState(True)
        button2.setCollectNo(btn_no)
        button2.setCollectTJBH(btn_tjbh)
        button2.setCollectType(btn_type)
        button2.setCollectPos(btn_pos_x,btn_pos_y)
        # 更新 容器
        self.all_serialno[btn_no] = button2
        # 从UI布局中 删除旧的 添加 新的
        if not btn_type:
            pass
        else:
            self.lt_left_bottom.removeWidget(button)
            button.hide()
            self.lt_left_bottom.addWidget(button2, btn_pos_x, btn_pos_y, 1, 1)
        # 更新界面UI
        # self.ser_done.setText("%s" % str(int(self.ser_done.text())+1))
        # self.ser_undone.setText("%s" % str(int(self.ser_undone.text())-1))
        # 刷新 入库
        self.data_obj['tjbh'] = btn_tjbh
        self.data_obj['mxbh'] = btn_no
        self.data_obj['jlnr'] = btn_name
        try:
            self.session.bulk_insert_mappings(MT_TJ_CZJLB, [self.data_obj])
            self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == btn_tjbh,
                                                     MT_TJ_TJJLMXB.tmbh1 == btn_no).update({MT_TJ_TJJLMXB.zxpb: '5'})
            self.session.commit()
        except Exception as e:
            mes_about(self,'插入 TJ_CZJLB 记录失败！错误代码：%s' %e)

    # 刷新采血列表
    def on_table_urine_insert(self,button:SerialNoButton):
        data=['已留样',button.collectNo,button.collectTJBH,button.collectTxt]
        self.table_urine.insert(data)
        self.gp_right.setTitle('留样列表（%s）' % str(self.table_urine.rowCount()))