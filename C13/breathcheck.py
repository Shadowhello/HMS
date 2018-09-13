from C13.breathcheck_ui import *
from C13.model import *

def cur_time():
    return time.strftime("%H:%M:%S", time.localtime(int(time.time())))

def cur_time_15():
    return time.strftime("%H:%M:%S", time.localtime(int(time.time()+900)))

def cur_datetime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

class BreathCheck(BreathCheckUI):

    def __init__(self,parent=None):
        super(BreathCheck,self).__init__(parent)
        # 状态容器: tjbh:state
        self.c13_items = {}
        # 初始化刷新列表
        self.initDatas()
        # 样本号计算器
        self.simpleno_1 = 0     # 明州1楼
        self.simpleno_2 = 0     # 明州2楼
        self.simpleno_3 = 0     # 明州3楼
        self.simpleno_4 = 0     # 江东
        self.simpleno_5 = 0     # 贵宾
        # 待插入的 数据对象
        self.data_obj = {'jllx':'0026','jlmc':'C13/14吹气','tjbh':'','mxbh':'5001','sjfs':'',
                         'czgh':self.login_id,'czxm':self.login_name,'czqy':self.login_area,'jlnr':None,'bz':None}
        # 绑定信号
        self.btn_update.clicked.connect(partial(self.on_btn_update_click,self.lb_update.text()))
        self.le_tjbh.returnPressed.connect(self.on_le_tjbh_press)
        self.table_c13_nocheck.itemClicked.connect(partial(self.on_table_oncheck_show,self.table_c13_nocheck))
        self.table_c13_checking_2.itemClicked.connect(partial(self.on_table_oncheck_show,self.table_c13_checking_2))
        self.table_c13_checking_1.itemDroped.connect(self.on_table_checking2_insert)
        # 吃药丸界面
        self.table_c13_checking_1.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.table_c13_checking_1.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单

    # 表格右键功能
    def onTableMenu(self,pos):
        row_num = -1
        indexs=self.table_c13_checking_1.selectionModel().selection().indexes()
        if indexs:
            for i in indexs:
                row_num = i.row()
            menu = QMenu()
            item1 = menu.addAction(Icon("取消"), "取消吃药")
            action = menu.exec_(self.table_c13_checking_1.mapToGlobal(pos))

            tjbh = self.table_c13_checking_1.getCurItemValueOfKey('tjbh')
            if action == item1:
                button = mes_warn(self,'您确定取消吃药丸？')
                if button == QMessageBox.Yes:
                    # 从当前位置删除
                    self.table_c13_checking_1.removeRow(self.table_c13_checking_1.currentRow())
                    self.gp_right_up.setTitle('2、吃药丸 计时中：总人数 %s' %self.table_c13_checking_1.rowCount())
                    # 回到待测位置
                    item = self.c13_items[tjbh]
                    item.setState(1)
                    self.table_c13_nocheck.insert4(item.getData())
                    self.gp_left.setTitle('1、待测：总人数 %s 人' % str(self.table_c13_nocheck.rowCount()))
                    try:
                        self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.tjbh == tjbh,MT_TJ_CZJLB.jllx == '0026').delete()
                        self.session.commit()
                    except Exception as e:
                        self.session.rollback()
                        mes_about(self,'MT_TJ_CZJLB 删除 记录失败！错误信息：%s' %e)


    # 刷新 获取待测数据
    def initDatas(self,up_time=None):
        # 初始化 所有组件
        if not up_time:
            ###################### 1、 显示完成列表 ######################
            results = self.session.execute(get_checked_sql()).fetchall()
            # 放入 对象容器
            tmp = []
            for result in results:
                # 已存在容器
                if result[0] not in list(self.c13_items.keys()):
                    self.c13_items[result[0]] = C13Item(result[0],data=list(result),state=4)
                    tmp.append(result)
            self.table_c13_checked.insertMany(tmp)
            self.gp_right_down_2.setTitle('4、完成吹气：总人数 %s' % self.table_c13_checked.rowCount())

            ###################### 2、 显示待吹气列表 ######################
            results = self.session.execute(get_checking2_sql()).fetchall()
            # 放入 对象容器
            tmp = []
            for result in results:
                # 已存在容器
                if result[0] not in list(self.c13_items.keys()):
                    self.c13_items[result[0]] = C13Item(result[0],data=list(result),state=3)
                    tmp.append(result)
            self.table_c13_checking_2.insertMany(tmp)
            self.gp_right_down_1.setTitle('3、计时完成待吹气：总人数 %s' % self.table_c13_checking_2.rowCount())

            ###################### 3、显示吃药丸列表 ######################
            results = self.session.execute(get_checking1_sql()).fetchall()
            for result in results:
                # 已存在容器
                print(str2(result[5]),self.login_area,str2(result[5]) in  self.login_area)
                if result[0] not in list(self.c13_items.keys()):
                    # 初始化 时 只显示本区域内的 吃药丸进度，避免影响其他区域
                    if str2(result[5]) in self.login_area:
                        self.c13_items[result[0]] = C13Item(result[0],data=list(result),state=2)
                        # 重启计时
                        tmp = []
                        tmp.extend(result)
                        tmp.append(0)
                        tmp.append(cur_time())
                        tmp.append(cur_time_15())
                        self.table_c13_checking_1.insert22([result[0],str2(result[1]),str2(result[2]),str(result[3]),str2(result[4]),str2(result[5]),0,cur_time(),cur_time_15()])
            self.gp_right_up.setTitle('2、吃药丸 计时中：总人数 %s' %self.table_c13_checking_1.rowCount())

            ###################### 4、 显示待测列表 ######################
            results = self.session.execute(get_nocheck_sql()).fetchall()
            # 放入 对象容器
            for result in results:
                self.c13_items[result[0]] = C13Item(result[0],data=list(result),state=1)
            self.table_c13_nocheck.load(results)
            self.gp_left.setTitle('1、待测：总人数 %s 人' % str(self.table_c13_nocheck.rowCount()))

        # 增量刷新 待测 组件
        else:
            results = self.session.execute(get_nocheck2_sql(up_time)).fetchall()
            if results:
                # 放入 对象容器
                tmp = []
                for result in results:
                    # 已存在容器
                    if result[0] not in list(self.c13_items.keys()):
                        self.c13_items[result[0]] = C13Item(result[0],data=list(result),state=1)
                        tmp.append(result)
                self.table_c13_nocheck.insertMany(tmp)
                self.gp_left.setTitle('1、待测：总人数 %s 人' % str(self.table_c13_nocheck.rowCount()))
                mes_about(self, '刷新 %s 条数据！' % str(len(tmp)))
            else:
                mes_about(self,'刷新 0 条数据！')
        # self.lb_update.setText('2018-08-21 09:00:00')   # 测试用
        self.lb_update.setText(cur_datetime())

    # 刷新待测列表
    def on_btn_update_click(self,up_time):
        self.initDatas(up_time)

    # 待测单击 显示体检编号
    def on_table_oncheck_show(self,tableWidget,QTableWidgetItem):
        if QTableWidgetItem:
            self.le_tjbh.setText(tableWidget.item(QTableWidgetItem.row(),0).text())

    # 体检编号 回车：1、吃药丸 2、完成吹气
    def on_le_tjbh_press(self):
        # 从状态容器中 获取 当前编号/状态 -> 效率更高
        tjbh = self.le_tjbh.text()
        if tjbh in list(self.c13_items.keys()):
            # 说明 在容器中 ，根据状态判断处于哪个table 中
            c13_item_obj = self.c13_items[tjbh]
            state = c13_item_obj.getState()
            print(tjbh,state)
            self.data_obj['tjbh'] = tjbh
            if state == 1:
                # 在待测列表中
                items = self.table_c13_nocheck.findItems(tjbh, Qt.MatchContains)
                if items:
                    item = items[0]
                    p_tjbh = self.table_c13_nocheck.item(item.row(), 0).text()
                    p_xm = self.table_c13_nocheck.item(item.row(), 1).text()
                    p_xb = self.table_c13_nocheck.item(item.row(), 2).text()
                    p_nl = self.table_c13_nocheck.item(item.row(), 3).text()
                    p_xmmc = self.table_c13_nocheck.item(item.row(), 4).text()
                    p_tjqy = self.table_c13_nocheck.item(item.row(), 5).text()
                    # 新表增加
                    self.table_c13_checking_1.insert2([p_tjbh,p_xm,p_xb,p_nl,p_xmmc,p_tjqy,0,cur_time(),cur_time_15()])
                    # 更新容器对象

                    # 旧表删除
                    self.table_c13_nocheck.removeRow(item.row())
                    # 更新新表 标题
                    self.gp_right_up.setTitle('2、吃药丸 计时中：总人数 %s' %self.table_c13_checking_1.rowCount())
                    # 更新旧表 标题
                    self.gp_left.setTitle('1、待测：总人数 %s 人' % str(self.table_c13_nocheck.rowCount()))
                    # C13项目状态变更
                    c13_item_obj.setData([p_tjbh,p_xm,p_xb,p_nl,p_xmmc,p_tjqy])
                    c13_item_obj.setState(2)
                    # 插入数据库
                    self.data_obj['bz'] = '吃药丸'
                    self.data_obj['sjfs'] = '2'
                    try:
                        self.session.bulk_insert_mappings(MT_TJ_CZJLB, [self.data_obj])
                        self.session.commit()
                    except Exception as e:
                        self.session.rollback()
                        mes_about(self, '插入 TJ_CZJLB,TJ_TJJLMXB 记录失败！错误代码：%s' % e)
                        self.log.info('插入 TJ_CZJLB,TJ_TJJLMXB 记录失败！错误代码：%s' % e)


            # 还处于 吃药丸中
            elif state == 2:
                items = self.table_c13_checking_1.findItems(tjbh, Qt.MatchContains)
                if items:
                    self.table_c13_checking_1.selectRow(items[0].row())
                mes_about(self,'该顾客正在吃药丸计时中，请计时结束后，再操作！')

            # 计时完成->吹气完成
            elif state == 3:
                items = self.table_c13_checking_2.findItems(tjbh, Qt.MatchContains)
                if items:
                    item = items[0]
                    p_tjbh = self.table_c13_checking_2.item(item.row(), 0).text()
                    p_sno = self.table_c13_checking_2.item(item.row(), 1).text()
                    p_xm = self.table_c13_checking_2.item(item.row(), 2).text()
                    p_xb = self.table_c13_checking_2.item(item.row(), 3).text()
                    p_nl = self.table_c13_checking_2.item(item.row(), 4).text()
                    p_xmmc = self.table_c13_checking_2.item(item.row(), 5).text()
                    p_tjqy = self.table_c13_checking_2.item(item.row(), 6).text()
                    # 删除原表中 行数据
                    self.table_c13_checking_2.removeRow(item.row())
                    # 更新项目状态
                    c13_item_obj.setState(4)
                    c13_item_obj.setData([p_tjbh,p_sno,p_xm,p_xb,p_nl,p_xmmc,p_tjqy])
                    # 新表增加
                    self.table_c13_checked.insert3([p_tjbh,p_sno,p_xm,p_xb,p_nl,p_xmmc,p_tjqy])
                    # 标题变更
                    self.gp_right_down_1.setTitle('3、计时完成待吹气：总人数 %s' % self.table_c13_checking_2.rowCount())
                    self.gp_right_down_2.setTitle('4、完成吹气：总人数 %s' %self.table_c13_checked.rowCount())
                    # 更新数据库 TJ_CZJLB  TJ_TJJLMXB
                    try:
                        self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.tjbh == tjbh,MT_TJ_CZJLB.mxbh == '5001').update({
                            MT_TJ_CZJLB.bz: '吹气完成',
                            MT_TJ_CZJLB.sjfs: '4'
                        },synchronize_session=False)
                        self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,MT_TJ_TJJLMXB.zhbh == '5001').update({MT_TJ_TJJLMXB.zxpb: '3'})
                        self.session.commit()
                    except Exception as e:
                        self.session.rollback()
                        mes_about(self, '插入 TJ_CZJLB,TJ_TJJLMXB 记录失败！错误代码：%s' % e)
                        self.log.info('插入 TJ_CZJLB,TJ_TJJLMXB 记录失败！错误代码：%s' % e)
            # 已完成吹气
            elif state == 4:
                items = self.table_c13_checked.findItems(tjbh, Qt.MatchContains)
                if items:
                    self.table_c13_checked.selectRow(items[0].row())
                    self.table_c13_checked.setStyleSheet("selection-background-color:qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #c0c0d0 stop:0.5 #054874 stop:1 #377277);")

                mes_about(self,'该顾客已完成吹气！')
        else:
            mes_about(self,'该顾客不存在，请尝试刷新或确认该顾客有C13项目！')

        # 清空体检编号
        self.le_tjbh.setText('')

    # 吹气列表
    def on_table_checking2_insert(self,data):
        if data[0] in list(self.c13_items.keys()):
            c13_item_obj = self.c13_items[data[0]]
            # data = c13_item_obj.getData()
            tjqy = data[5]
            # 更新项目状态
            c13_item_obj.setState(3)
            # 吹气完成，设置样本号
            if tjqy == '明州1楼':
                self.simpleno_1 = self.simpleno_1 + 1
                c13_item_obj.setSimpleNo(1000 + self.simpleno_1)
            elif tjqy == '明州2楼':
                self.simpleno_2 = self.simpleno_2 + 1
                c13_item_obj.setSimpleNo(2000 + self.simpleno_2)
            elif tjqy == '明州3楼':
                self.simpleno_3 = self.simpleno_3 + 1
                c13_item_obj.setSimpleNo(3000 + self.simpleno_3)
            elif tjqy == '江东':
                self.simpleno_4 = self.simpleno_4 + 1
                c13_item_obj.setSimpleNo(4000 + self.simpleno_4)
            elif tjqy == '明州贵宾':
                self.simpleno_5 = self.simpleno_5 + 1
                c13_item_obj.setSimpleNo(5000 + self.simpleno_5)
            # 添加样本号
            data.insert(1,str(c13_item_obj.getSimpleNo()))
            # 新表增加
            self.table_c13_checking_2.insert3(data)
            # 数量变更
            self.gp_right_up.setTitle('2、吃药丸 计时中：总人数 %s' % self.table_c13_checking_1.rowCount())
            self.gp_right_down_1.setTitle('3、计时完成待吹气：总人数 %s' % self.table_c13_checking_2.rowCount())
            # 更新数据库 TJ_CZJLB
            try:
                self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.tjbh == data[0], MT_TJ_CZJLB.mxbh == '5001').update({
                    MT_TJ_CZJLB.bz: '吹气中',
                    MT_TJ_CZJLB.sjfs: '3',
                    MT_TJ_CZJLB.jjxm: str(c13_item_obj.getSimpleNo())
                },synchronize_session=False)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                mes_about(self, '插入 TJ_CZJLB,TJ_TJJLMXB 记录失败！错误代码：%s' % e)
                self.log.info('插入 TJ_CZJLB,TJ_TJJLMXB 记录失败！错误代码：%s' % e)




if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = BreathCheck()
    ui.show()
    app.exec_()