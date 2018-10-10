from widgets.cwidget import *
from report.model import *
import zeep,json,base64,os

# 查看项目状态
class ItemsStateUI(Dialog):

    # 自定义 信号，封装对外使用
    returnPressed = pyqtSignal(str)

    def __init__(self,parent=None):
        super(ItemsStateUI,self).__init__(parent)
        self.setWindowTitle('项目查看')
        self.setMinimumHeight(500)
        self.setMinimumWidth(880)
        self.initUI()
        # 绑定信号槽
        self.returnPressed.connect(self.setDatas)
        self.le_tjbh.returnPressed.connect(self.on_le_tjbh_press)
        self.btn_query.clicked.connect(self.on_le_tjbh_press)
        self.table_item.itemClicked.connect(self.on_table_item_click)
        # 右键
        self.table_item.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.table_item.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单
        self.tmp_path = gol.get_value('path_tmp')

    # 右键功能
    def onTableMenu(self,pos):
        row_num = -1
        indexs=self.table_item.selectionModel().selection().indexes()
        if indexs:
            for i in indexs:
                row_num = i.row()
            menu = QMenu()
            item1 = menu.addAction(Icon(""), "手工小结")
            action = menu.exec_(self.table_item.mapToGlobal(pos))
            xmbh = self.table_item.getCurItemValueOfKey('xmbh')
            tjbh = self.gp_user.get_tjbh
            if action == item1:
                if xmbh in ['1122','1931','0903','501732','501933','501934']:
                    pass
                else:
                    mes_about(self,'该项目不是手工单项目，不允许手工小结！')

    def initUI(self):
        self.item_cols = OrderedDict(
            [
                ("state","状态"),
                ("xmbh", "项目编号"),
                ("xmmc", "项目名称"),
                ("ksmc", "科室名称"),
                ("jcrq", "检查日期"),
                ("jcys", "检查医生"),
                ("shrq", "审核日期"),
                ("shys", "审核医生"),
                ("tmbh", "条码号"),
                ("btn_name", "")
             ])
        lt_main = QVBoxLayout()
        # 搜索
        lt_top = QHBoxLayout()
        self.le_tjbh = QTJBH()
        self.btn_query = QPushButton(Icon('query'),'查询')
        gp_top = QGroupBox('检索条件')
        lt_top.addWidget(QLabel('体检编号：'))
        lt_top.addWidget(self.le_tjbh)
        lt_top.addWidget(self.btn_query)
        lt_top.addStretch()
        gp_top.setLayout(lt_top)
        lt_middle = QHBoxLayout()
        self.gp_middle = QGroupBox('项目信息')
        # 用户基本信息
        self.gp_user = UserBaseGroup()
        self.table_item = ItemsStateTable(self.item_cols)
        self.table_item.setAlternatingRowColors(False)                       # 使用行交替颜色
        self.table_item.verticalHeader().setVisible(False)
        lt_middle.addWidget(self.table_item)
        self.gp_middle.setLayout(lt_middle)

        lt_main.addWidget(gp_top)
        lt_main.addLayout(self.gp_user)
        lt_main.addWidget(self.gp_middle)
        self.setLayout(lt_main)

    # 变更项目状态
    def on_table_item_click(self,QTableWidgetItem):
        row = QTableWidgetItem.row()
        col = QTableWidgetItem.column()
        if col != self.table_item.getLastCol():
            return
        tjbh = self.le_tjbh.text()
        btn_name = self.table_item.getItemValueOfKey(row, "btn_name")
        xmbh = self.table_item.getItemValueOfKey(row, "xmbh")
        xmmc = self.table_item.getItemValueOfKey(row, "xmmc")
        if btn_name:
            if btn_name=='核实':
                button = mes_warn(self, '您是否继续？')
                if button != QMessageBox.Yes:
                    return
                try:
                    data_obj = {'jllx': '0121', 'jlmc': '项目核实', 'tjbh':tjbh , 'mxbh': '',
                                'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area, 'jlnr': xmmc,
                                'bz': None}
                    self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh==tjbh,MT_TJ_TJJLMXB.zhbh==xmbh).update({
                        MT_TJ_TJJLMXB.zxpb: '0',
                        MT_TJ_TJJLMXB.jsbz: '0',
                        MT_TJ_TJJLMXB.qzjs: None
                    })
                    self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                    mes_about(self,'执行出错，错误信息：%s' %e)
                    return
                # 刷新界面
                self.table_item.setItemValueOfKey(row,'state','核实',QColor("#FF0000"))
            elif btn_name=='拒检':
                button = mes_warn(self, '您是否继续？')
                if button != QMessageBox.Yes:
                    return
                try:
                    data_obj = {'jllx': '0012', 'jlmc': '项目拒检', 'tjbh':tjbh , 'mxbh': '',
                                'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area, 'jlnr': xmmc,
                                'bz': None}
                    self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh==tjbh,MT_TJ_TJJLMXB.zhbh==xmbh).update({
                        MT_TJ_TJJLMXB.zxpb: '1',
                        MT_TJ_TJJLMXB.jsbz: '1',
                        MT_TJ_TJJLMXB.qzjs: '1'
                    })
                    self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                    mes_about(self,'执行出错，错误信息：%s' %e)
                    return
                # 刷新界面
                self.table_item.setItemValueOfKey(row,'state','已拒检',QColor("#008000"))

            elif btn_name == '图像接收':
                results = self.session.query(MT_TJ_PACS_PIC).filter(MT_TJ_PACS_PIC.tjbh==tjbh,MT_TJ_PACS_PIC.zhbh==xmbh).all()
                if results:
                    button = mes_warn(self,"您是否确认从检查系统接收图像？")
                    if button != QMessageBox.Yes:
                        return
                # 读取
                filenames = get_pacs_pic(tjbh,xmbh,self.tmp_path)
                if filenames:
                    # 上传 http请求替代smb协议
                    pass
                else:
                    mes_about(self,'检查系统中未发现顾客(%s)%s项目的图像！' %(tjbh,xmmc))
                # 上传
                # 更新或者删除
            else:
                mes_about(self,'功能未定义，请联系管理员！')

    # 初始化数据
    def setDatas(self,p_str):
        self.le_tjbh.setText(p_str)
        self.on_le_tjbh_press()

    # 查询
    def on_le_tjbh_press(self):
        if not self.le_tjbh.text():
            mes_about(self,'请输入体检编号！')
            return
        # 人员信息
        result = self.session.query(MV_RYXX).filter(MV_RYXX.tjbh == self.le_tjbh.text()).scalar()
        if result:
            self.gp_user.setData(result.to_dict)
        else:
            mes_about(self,'不存在，请确认后重新输入！')
            self.gp_user.clearData()
        # 项目结果
        #results = self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == self.le_tjbh.text(),MT_TJ_TJJLMXB.sfzh=='1').all()
        #self.table_item.load([result.item_result for result in results])
        results = self.session.execute(get_item_state_sql(tjbh=self.le_tjbh.text())).fetchall()
        self.table_item.load(results)
        self.gp_middle.setTitle('项目状态 (%s)' %self.table_item.rowCount())


# 胶片打印服务
def get_pacs_pic(tjbh, xmbh, path):
    url = "http://10.8.200.220:7059/WebGetFileView.asmx?WSDL"
    client = zeep.Client(url)
    try:
        result = json.loads(client.service.f_GetUISFilesByTJ_IID(tjbh + xmbh))
        filenames = []
        if result['IsSuccess'] == 'true':
            pic_datas = result['Datas']
            count = 0
            for pic_data in pic_datas:
                count = count + 1
                filename = os.path.join(path, '%s_%s_%s.jpg' % (tjbh, xmbh, count))
                with open(filename, "wb") as f:
                    f.write(base64.b64decode(pic_data))
                filenames.append(filename)
        return filenames

    except Exception as e:
        print(e)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = ItemsStateUI()
    ui.show()
    app.exec_()

