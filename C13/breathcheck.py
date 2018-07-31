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
        # 待插入的 数据对象
        self.data_obj = {'jllx':'0026','jlmc':'C13/14吹气','tjbh':'','mxbh':'5001',
                         'czgh':self.login_id,'czxm':self.login_name,'czqy':self.login_area,'jlnr':None,'bz':None}
        # 绑定信号
        self.btn_update.clicked.connect(partial(self.on_btn_update_click,self.lb_update.text()))
        self.le_tjbh.returnPressed.connect(self.on_le_tjbh_press)
        self.table_c13_nocheck.itemClicked.connect(partial(self.on_table_oncheck_show,self.table_c13_nocheck))
        self.table_c13_checking_2.itemClicked.connect(partial(self.on_table_oncheck_show,self.table_c13_checking_2))
        self.table_c13_checking_1.itemDroped.connect(self.on_table_checking2_insert)

    # 刷新 获取待测数据
    def initDatas(self,up_time=None):
        # 初始化
        if not up_time:
            results = self.session.execute(get_nocheck_sql()).fetchall()
            self.table_c13_nocheck.load(results)
        # 增量刷新
        else:
            results = self.session.execute(get_nocheck2_sql(up_time)).fetchall()
            self.table_c13_nocheck.insertMany(results)

        # 放入 对象容器
        for result in results:
            self.c13_items[result[0]] = C13Item(result[0])
        self.gp_left.setTitle('1、待测：总人数 %s 人' % str(self.table_c13_nocheck.rowCount()))
        self.lb_update.setText(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))))

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
            data = c13_item_obj.getData()
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
                    # 旧表删除
                    self.table_c13_nocheck.removeRow(item.row())
                    # 更新新表 标题
                    self.gp_right_up.setTitle('2、吃药丸 计时中：总人数 %s' %self.table_c13_checking_1.rowCount())
                    # 更新旧表 标题
                    self.gp_left.setTitle('1、待测：总人数 %s 人' % str(self.table_c13_nocheck.rowCount()))
                    # C13项目状态变更
                    c13_item_obj.setData([p_tjbh,p_xm,p_xb,p_nl,p_xmmc,p_tjqy])
                    c13_item_obj.setState(2)

            # 还处于 吃药丸中
            elif state == 2:
                items = self.table_c13_checking_1.findItems(tjbh, Qt.MatchContains)
                if items:
                    self.table_c13_checking_1.selectRow(items[0].row())
                mes_about(self,'该顾客正在吃药丸计时中，请计时结束后，再操作！')

            elif state == 3:
                items = self.table_c13_checking_2.findItems(tjbh, Qt.MatchContains)
                if items:
                    item = items[0]
                    p_tjqy = self.table_c13_checking_2.item(item.row(), 5).text()
                    # 删除原表中 行数据
                    self.table_c13_checking_2.removeRow(item.row())
                    # 更新项目状态
                    c13_item_obj.setState(4)
                    # 标题变更
                    self.gp_right_down_1.setTitle('3、计时完成待吹气：总人数 %s' % self.table_c13_checking_2.rowCount())
                    self.gp_right_down_2.setTitle('4、完成吹气：总人数 %s' %self.table_c13_checked.rowCount())
                    # 吹气完成，设置样本号
                    if p_tjqy == '明州1楼':
                        self.simpleno_1 = self.simpleno_1 + 1
                        c13_item_obj.setSimpleNo(1000+self.simpleno_1)
                    elif p_tjqy == '明州2楼':
                        self.simpleno_2 = self.simpleno_2 + 1
                        c13_item_obj.setSimpleNo(2000+self.simpleno_2)
                    elif p_tjqy == '明州3楼':
                        self.simpleno_3 = self.simpleno_3 + 1
                        c13_item_obj.setSimpleNo(3000+self.simpleno_3)
                    elif p_tjqy == '江东':
                        self.simpleno_4 = self.simpleno_4 + 1
                        c13_item_obj.setSimpleNo(4000+self.simpleno_4)

                    # 添加样本号
                    data.insert(0,str(c13_item_obj.getSimpleNo()))
                    # 新表增加
                    self.table_c13_checked.insert3(data)
                    # 更新数据库 TJ_CZJLB  TJ_TJJLMXB
                    self.data_obj['tjbh'] = tjbh
                    self.data_obj['bz'] = str(c13_item_obj.getSimpleNo())
                    try:
                        self.session.bulk_insert_mappings(MT_TJ_CZJLB, [self.data_obj])
                        self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,MT_TJ_TJJLMXB.zhbh == '5001').update({MT_TJ_TJJLMXB.zxpb: '3'})
                        self.session.commit()
                    except Exception as e:
                        mes_about(self, '插入 TJ_CZJLB,TJ_TJJLMXB 记录失败！错误代码：%s' % e)
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
    def on_table_checking2_insert(self,tjbh:str):
        if tjbh in list(self.c13_items.keys()):
            c13_item_obj = self.c13_items[tjbh]
            # 新表增加
            self.table_c13_checking_2.insert3(c13_item_obj.getData())
            # 新表 标题变更
            self.gp_right_down_1.setTitle('3、计时完成待吹气：总人数 %s' % self.table_c13_checking_2.rowCount())
            self.gp_right_up.setTitle('2、吃药丸 计时中：总人数 %s' % self.table_c13_checking_1.rowCount())
            # 更新项目状态
            c13_item_obj.setState(3)



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = BreathCheck()
    ui.show()
    app.exec_()