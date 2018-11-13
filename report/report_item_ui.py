from widgets.cwidget import *
from report.model import *
import zeep,json,base64,os
from utils import trans_pacs_pic,request_get,print_pdf_gsprint
from widgets import QBrowser

# 查看项目状态
class ItemsStateUI(Dialog):

    # 自定义 信号，封装对外使用
    returnPressed = pyqtSignal(str)

    def __init__(self,parent=None):
        super(ItemsStateUI,self).__init__(parent)
        self.setWindowTitle('项目查看')
        self.setMinimumHeight(600)
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
        self.table_item.itemDoubleClicked.connect(self.on_table_item_doubleclick)
        # 功能区
        self.btn_report_suggest.clicked.connect(self.on_btn_report_suggest_click)
        self.btn_report_zdbl.clicked.connect(self.on_btn_report_zdbl_click)
        self.btn_report_browse.clicked.connect(self.on_btn_report_browse_click)
        self.btn_report_print.clicked.connect(self.on_btn_report_print_click)
        self.btn_report_down.clicked.connect(self.on_btn_report_down_click)
        self.tmp_path = gol.get_value('path_tmp')
        # 特殊变量
        self.browser = None

    def on_btn_report_suggest_click(self):
        pass

    def on_btn_report_zdbl_click(self):
        pass

    def on_btn_report_browse_click(self):
        tjbh = self.gp_user.get_tjbh
        # 优先打开 新系统生成的
        result = self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).scalar()
        if result:
            filename = os.path.join(result.bglj, '%s.pdf' % tjbh).replace('D:/activefile/', '')
            url = gol.get_value('api_pdf_new_show') % filename
            url_title = "体检编号：%s" % tjbh
            self.open_url(url, url_title)
        else:
            try:
                self.cxk_session = gol.get_value('cxk_session')
                result = self.cxk_session.query(MT_TJ_PDFRUL).filter(MT_TJ_PDFRUL.TJBH == tjbh).scalar()
                if result:
                    url = gol.get_value('api_pdf_old_show') % result.PDFURL
                    url_title = "体检编号：%s" % tjbh
                    self.open_url(url, url_title)
                    # webbrowser.open(url)
                else:
                    mes_about(self, '未找到该顾客体检报告！')
            except Exception as e:
                mes_about(self, '查询出错，错误信息：%s' % e)
                return

    # 在窗口中打开报告，取消在浏览器中打开，主要用于外部查询中使用，避免地址外泄
    def open_url(self,url,title):
        if not self.browser:
            self.browser = QBrowser(self)
        self.browser.open_url.emit(title,url)
        self.browser.show()

    def on_btn_report_print_click(self):
        printerInfo = QPrinterInfo()
        default_printer = printerInfo.defaultPrinterName()
        button = mes_warn(self, "您确认用打印机：%s，打印当前选择的体检报告？" %default_printer)
        if button != QMessageBox.Yes:
            return
        tjbh = self.gp_user.get_tjbh
        # 本地打印 需要下载
        url = gol.get_value('api_report_down') % tjbh
        filename = os.path.join(gol.get_value('path_tmp'), '%s.pdf' % tjbh)
        if request_get(url, filename):
            # 打印成功
            if print_pdf_gsprint(filename) == 0:
                # 打印成功
                mes_about(self, '打印成功！')
            else:
                # 打印失败
                mes_about(self, '打印失败！')
        else:
            mes_about(self,'未找到可打印的报告！')

    def on_btn_report_down_click(self):
        filepath = QFileDialog.getExistingDirectory(self, "下载保存路径",desktop(),QFileDialog.ShowDirsOnly|QFileDialog.DontResolveSymlinks)
        if not filepath:
            return
        button = mes_warn(self, "您确认下载当前选择的体检报告到路径：%s？" %filepath)
        if button != QMessageBox.Yes:
            return
        tjbh = self.gp_user.get_tjbh
        url = gol.get_value('api_report_down') %tjbh
        filename = os.path.join(filepath, '%s.pdf' % tjbh)
        if request_get(url,filename):
            # 下载成功
            mes_about(self,'下载成功！')
        else:
            mes_about(self,'未找到报告，无法下载！')


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
        self.btn_receive= QPushButton(Icon('接收'), '结果接收')
        gp_top = QGroupBox('检索条件')
        lt_top.addWidget(QLabel('体检编号：'))
        lt_top.addWidget(self.le_tjbh)
        lt_top.addWidget(self.btn_query)
        lt_top.addWidget(self.btn_receive)
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
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox()
        self.btn_report_suggest = QPushButton(Icon('小结建议'),'小结建议')
        self.btn_report_zdbl = QPushButton(Icon('病历'), '重点病历')
        self.btn_report_browse = QPushButton(Icon('报告'),'报告浏览')          # 查看
        self.btn_report_print = QPushButton(Icon('报告'), '报告打印')         # 打印
        self.btn_report_down = QPushButton(Icon('报告'),'报告下载')          # 下载
        lt_bottom.addWidget(self.btn_report_suggest)
        lt_bottom.addWidget(self.btn_report_zdbl)
        lt_bottom.addWidget(self.btn_report_browse)
        lt_bottom.addWidget(self.btn_report_print)
        lt_bottom.addWidget(self.btn_report_down)
        gp_bottom.setLayout(lt_bottom)
        # 添加布局
        lt_main.addWidget(gp_top)
        lt_main.addLayout(self.gp_user)
        lt_main.addWidget(self.gp_middle)
        lt_main.addWidget(gp_bottom)
        self.setLayout(lt_main)

    # 双击查看明细结果
    def on_table_item_doubleclick(self):
        pass

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
        ksmc = self.table_item.getItemValueOfKey(row, "ksmc")
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
                button = mes_warn(self,"您是否确认从检查系统重新接收图像？")
                if button != QMessageBox.Yes:
                        return
                if '彩超' in ksmc:
                    ksbm = '0020'
                elif '病理' in ksmc:
                    ksbm = '0026'
                else:
                    ksbm = '0024'
                if trans_pacs_pic(tjbh,ksbm,xmbh):
                    mes_about(self,'传输成功！')
                else:
                    mes_about(self,'传输失败！')
            #     results = self.session.query(MT_TJ_PACS_PIC).filter(MT_TJ_PACS_PIC.tjbh==tjbh,MT_TJ_PACS_PIC.zhbh==xmbh).all()
            #     if results:
            #         button = mes_warn(self,"您是否确认从检查系统接收图像？")
            #         if button != QMessageBox.Yes:
            #             return
            #     # 读取
            #     filenames = get_pacs_pic(tjbh,xmbh,self.tmp_path)
            #     if filenames:
            #         # 上传 http请求替代smb协议
            #         pass
            #     else:
            #         mes_about(self,'检查系统中未发现顾客(%s)%s项目的图像！' %(tjbh,xmmc))
            #     # 上传
            #     # 更新或者删除
            # else:
            #     mes_about(self,'功能未定义，请联系管理员！')

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
        self.gp_middle.setTitle('项目信息 (%s)' %self.table_item.rowCount())


# 获取彩超、内镜图像
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

# 查看操作记录
class OperateUI(Dialog):

    # 自定义 信号，封装对外使用
    returnPressed = pyqtSignal(str)

    def __init__(self,parent=None):
        super(OperateUI,self).__init__(parent)
        self.setWindowTitle('操作记录查询')
        self.setMinimumHeight(500)
        self.setMinimumWidth(700)
        self.initUI()
        # 信号槽
        self.returnPressed.connect(self.setQuery)
        self.btn_query.clicked.connect(self.on_btn_query_click)
        self.le_tjbh.returnPressed.connect(self.on_le_tjbh_return)


    def setQuery(self, tjbh):
        self.le_tjbh.setText(tjbh)
        self.on_le_tjbh_return()

    def on_le_tjbh_return(self):
        tjbh = self.le_tjbh.text()
        if not tjbh:
            mes_about(self, '请您输入体检编号')
            return
        else:
            sql = get_operate_sql(tjbh)
            results = self.session.execute(sql)
            self.table_operate.load(results)
            self.gp_middle.setTitle('操作记录(%s)' % self.table_operate.rowCount())
            # mes_about(self, '共检索出数据 %s 条' % self.table_operate.rowCount())

        self.le_tjbh.setText('')

    def on_btn_query_click(self):
        if self.le_tjbh.text():
            self.on_le_tjbh_return()

    def initUI(self):
        self.operate_cols = OrderedDict(
            [
                ("jlmc", "记录名称"),
                ("czsj", "操作时间"),
                ("czxm", "操作人员"),
                ("czqy", "操作区域"),
                ("jnlr", "记录内容"),
                ("bz", "备注")
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
        self.gp_middle = QGroupBox('操作记录(0)')
        # 用户基本信息
        # self.gp_user = UserBaseGroup()
        self.table_operate = OperateTable(self.operate_cols)
        self.table_operate.setAlternatingRowColors(False)                       # 使用行交替颜色
        self.table_operate.verticalHeader().setVisible(False)
        lt_middle.addWidget(self.table_operate)
        self.gp_middle.setLayout(lt_middle)

        lt_main.addWidget(gp_top)
        # lt_main.addLayout(self.gp_user)
        lt_main.addWidget(self.gp_middle)
        self.setLayout(lt_main)

# 报告审阅列表
class OperateTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(OperateTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # 字典载入
        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)  # 插入一行
            for col_index, col_value in enumerate(row_data):
                if col_index==1:
                    item = QTableWidgetItem(str2(col_value))
                    item.setTextAlignment(Qt.AlignCenter)
                else:
                    item = QTableWidgetItem(str2(col_value))
                self.setItem(row_index, col_index, item)
        # 布局
        self.setColumnWidth(0, 75)      # 记录名称
        self.setColumnWidth(1, 80)      # 操作时间
        self.setColumnWidth(2, 60)      # 操作人员
        self.setColumnWidth(3, 80)      # 操作区域
        self.setColumnWidth(4, 200)  # 操作区域
        self.horizontalHeader().setStretchLastSection(True)

# 获取操作记录SQL
def get_operate_sql(tjbh):
    return '''
    (SELECT 
        '信息修改' AS JLMC,substring(convert(char,zhxgsj,120),1,19) AS CZSJ,
        (SELECT YGXM FROM TJ_YGDM WHERE YGGH=log_jbxx.zhxgr ) AS CZXM,
        '' AS CZQY,
        xgnr AS JLNR,
        '' AS BZ 
    FROM log_jbxx WHERE tjbh='%s')
    
    UNION ALL
    
    (SELECT JLMC,substring(convert(char,CZSJ,120),1,19) AS CZSJ,CZXM,CZQY,JLNR,BZ FROM TJ_CZJLB WHERE tjbh='%s')
    
    ORDER BY czsj 
    ''' %(tjbh,tjbh)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = ItemsStateUI()
    ui.show()
    app.exec_()

