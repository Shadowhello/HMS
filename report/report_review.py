from report.report_review_ui import *
import webbrowser

# 报告追踪
class ReportReview(ReportReviewUI):

    def __init__(self):
        super(ReportReview, self).__init__()
        self.gp_quick_search.returnPressed.connect(self.on_quick_search)    # 快速检索
        # 右键、双击、单击
        self.table_report_review.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.table_report_review.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单
        self.btn_query.clicked.connect(self.on_btn_query_click)
        # 表格双击
        self.table_report_review.doubleClicked.connect(self.on_table_double_click)
        # 审阅
        self.gp_review_user.btnClick.connect(self.on_btn_review_click)
        self.btn_review_mode.clicked.connect(self.on_btn_review_mode_click)
        # 设置快速获取的变量
        self.cur_tjbh = None
        self.cur_row = None

    def on_btn_review_mode_click(self):
        if self.table_report_review.rowCount():
            ui = ReportReviewFullScreen(self)
            ui.opened.emit(self.table_report_review.cur_data_set)
            ui.showFullScreen()
        else:
            mes_about(self,"请先筛选需要审阅的报告，再全屏操作！")

    def on_btn_query_click(self):
        # 日期范围 必选
        tstart,tend = self.gp_where_search.date_range
        sql = get_report_review_sql(tstart,tend)
        # 报告状态
        if self.cb_report_state.where_state:
            sql = sql + self.cb_report_state.where_state
        # 报告审阅者
        if self.cb_user.where_user:
            sql = sql + " AND SYXM ='%s' " %self.cb_user.where_user
        # 附加 关联SQL 必须
        sql = sql + " INNER JOIN TJ_TJDAB b ON a.DABH=b.DABH "
        # 是否选择单位
        if self.gp_where_search.where_dwbh:
            sql = sql + " AND a.DWBH = '%s' " %self.gp_where_search.where_dwbh
        # 是否选择 区域
        if self.cb_area.where_tjqy2:
            sql = sql + self.cb_area.where_tjqy2
        # 是否选择 报告类型
        if self.cb_report_type.where_tjlx2:
            sql = sql + self.cb_report_type.where_tjlx2
        try:
            results = self.session.execute(sql).fetchall()
        except Exception as e:
            results = []
            mes_about(self,'执行SQL：%s 出错，错误信息：%s' %(sql,e))
        self.table_report_review.load(results)
        self.gp_table.setTitle('审阅列表（%s）' %self.table_report_review.rowCount())
        mes_about(self, '检索出数据%s条' % self.table_report_review.rowCount())
        #results = self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.shrq>=tstart,MT_TJ_BGGL.shrq<tend).all()

    def on_table_double_click(self,QModelIndex):
        # 获取变量
        bgzt = self.table_report_review.getItemValueOfKey(QModelIndex.row(), 'bgzt')
        tjbh = self.table_report_review.getItemValueOfKey(QModelIndex.row(), 'tjbh')
        xm = self.table_report_review.getItemValueOfKey(QModelIndex.row(), 'xm')
        xb = self.table_report_review.getItemValueOfKey(QModelIndex.row(), 'xb')
        nl = self.table_report_review.getItemValueOfKey(QModelIndex.row(), 'nl')
        syrq = self.table_report_review.getItemValueOfKey(QModelIndex.row(), 'syrq')
        syxm = self.table_report_review.getItemValueOfKey(QModelIndex.row(), 'syxm')
        sybz = self.table_report_review.getItemValueOfKey(QModelIndex.row(), 'sybz')
        #
        self.cur_tjbh = tjbh
        self.cur_row = QModelIndex.row()
        # 更新title
        self.gp_right.setTitle('报告预览   体检编号：%s  姓名：%s 性别：%s  年龄：%s' %(tjbh,xm,xb,nl))
        self.gp_right.setStyleSheet('''font: 75 12pt '微软雅黑';color: rgb(0,128,0);''')
        # 未审阅则打开HTML 页面
        url = gol.get_value('api_report_preview') %('html',tjbh)
        self.wv_report_equip.load(url)
        # 已审阅则 打开PDF 页面 PDF在窗口中加载奇慢无比，取消此功能
        # 先下载
        # url = gol.get_value('api_report_down') %tjbh
        # filename = os.path.join(gol.get_value('path_tmp'),'%s.pdf' %tjbh)
        # if request_get(url,filename):
        #     # 下载成功
        #     url = gol.get_value('api_pdf_show') %filename
        #     print(url)
        #     self.wv_report_equip.load(url)
        # 刷新界面
        self.gp_review_user.setData({'sybz':sybz,'syrq':syrq,'syxm':syxm,'syzt':bgzt})

    # 右键功能
    def onTableMenu(self,pos):
        row_num = -1
        indexs=self.table_report_review.selectionModel().selection().indexes()
        if indexs:
            for i in indexs:
                row_num = i.row()
            menu = QMenu()
            item1 = menu.addAction(Icon("报告中心"), "浏览器中打开HTML报告")
            item2 = menu.addAction(Icon("报告中心"), "浏览器中打开PDF报告")
            action = menu.exec_(self.table_report_review.mapToGlobal(pos))
            tjbh = self.table_report_review.getCurItemValueOfKey('tjbh')
            bgzt = self.table_report_review.getCurItemValueOfKey('bgzt')
            if tjbh:
                if action == item1:
                    try:
                        webbrowser.open(gol.get_value('api_report_preview') % ('html', tjbh))
                    except Exception as e:
                        mes_about(self, '打开出错，错误信息：%s' % e)
                        return
                elif action == item2:
                    if bgzt=='已审核':
                        mes_about(self,'该报告还未审阅，不能查看PDF报告！')
                    else:
                        # 优先打开 新系统生成的
                        result = self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).scalar()
                        if result:
                            filename = os.path.join(result.bglj,'%s.pdf' %tjbh).replace('D:/activefile/','')
                            url = gol.get_value('api_pdf_new_show') % filename
                            webbrowser.open(url)
                        else:
                            try:
                                self.cxk_session = gol.get_value('cxk_session')
                                result = self.cxk_session.query(MT_TJ_PDFRUL).filter(MT_TJ_PDFRUL.TJBH == tjbh).scalar()
                                if result:
                                    url = gol.get_value('api_pdf_old_show') % result.PDFURL
                                    webbrowser.open(url)
                                else:
                                    mes_about(self, '未找到该顾客体检报告！')
                            except Exception as e:
                                mes_about(self, '查询出错，错误信息：%s' % e)
                                return
            else:
                mes_about(self, '未找到该顾客体检报告！')


    #快速检索
    def on_quick_search(self,p1_str,p2_str):
        if p1_str == 'tjbh':
            where_str = " a.TJBH = '%s' " % p2_str
        else:
            where_str = " b.XM = '%s' " % p2_str
        results = self.session.execute(get_report_review_sql2(where_str)).fetchall()
        self.table_report_review.load(results)
        mes_about(self,'共检索出 %s 条数据！' %self.table_report_review.rowCount())

    # 审阅/取消审阅
    def on_btn_review_click(self,syzt:bool,num:int):
        # 未双击过查看过报告 不允许审核
        if not self.cur_tjbh:
            mes_about(self,'您还未打开报告，不允许审阅')
            return
        # 完成审阅
        if syzt:
            # 更新数据库 TJ_CZJLB TJ_BGGL
            data_obj = {'jllx':'0031','jlmc':'报告审阅','tjbh':self.cur_tjbh,'mxbh':'',
                         'czgh':self.login_id,'czxm':self.login_name,'czqy':self.login_area,'jlnr':str(num),'bz':self.gp_review_user.get_sybz()}
            try:
                self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == self.cur_tjbh).update(
                    {
                        MT_TJ_BGGL.syxm: self.login_name,
                        MT_TJ_BGGL.sygh: self.login_id,
                        MT_TJ_BGGL.syrq: cur_datetime(),
                        MT_TJ_BGGL.sybz: self.gp_review_user.get_sybz(),
                        MT_TJ_BGGL.sysc: num,
                        MT_TJ_BGGL.bgzt: 2,
                    }
                )
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                mes_about(self,'更新数据库失败！错误信息：%s' %e)
                return
            # 刷新控件 表格 和按钮
            self.table_report_review.setItemValueOfKey(self.cur_row, 'bgzt', '已审阅', QColor("#f0e68c"))           # 审阅状态
            self.table_report_review.setItemValueOfKey(self.cur_row, 'syxm', self.login_name)                  # 审阅者
            self.table_report_review.setItemValueOfKey(self.cur_row, 'syrq', cur_datetime())                   # 审阅日期
            self.table_report_review.setItemValueOfKey(self.cur_row, 'sybz', self.gp_review_user.get_sybz())   # 审阅备注
            self.gp_review_user.statechange()
            self.gp_review_user.setData({'sybz':self.gp_review_user.get_sybz(),'syrq':cur_datetime(),'syxm':self.login_name,'syzt':2})
            # 向服务端 发送请求
            # HTML 报告需要重新生成
            request_create_report(self.cur_tjbh, 'html')
            # 生成PDF 报告请求
            request_create_report(self.cur_tjbh, 'pdf')

        # 取消审阅
        else:
            if not self.gp_review_user.get_sybz():
                mes_about(self,'请您输入取消审阅原因！')
                return
            # 更新数据库 TJ_CZJLB TJ_BGGL
            data_obj = {'jllx':'0032','jlmc':'取消审阅','tjbh':self.cur_tjbh,'mxbh':'',
                         'czgh':self.login_id,'czxm':self.login_name,'czqy':self.login_area,'bz':self.gp_review_user.get_sybz()}
            try:
                self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                self.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == self.cur_tjbh).update(
                    {
                        MT_TJ_BGGL.syxm: None,
                        MT_TJ_BGGL.sygh: None,
                        MT_TJ_BGGL.syrq: None,
                        MT_TJ_BGGL.sybz: None,
                        MT_TJ_BGGL.sysc: 0,
                        MT_TJ_BGGL.bgzt: 1,
                    }
                )
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                mes_about(self,'更新数据库失败！错误信息：%s' %e)
                return
            # 更新表
            self.table_report_review.setItemValueOfKey(self.cur_row, 'bgzt', '已审核',QColor("#FF0000"))    # 审阅状态
            self.table_report_review.setItemValueOfKey(self.cur_row, 'syxm', '')                           # 审阅者
            self.table_report_review.setItemValueOfKey(self.cur_row, 'syrq', '')                           # 审阅日期
            self.table_report_review.setItemValueOfKey(self.cur_row, 'sybz','')                            # 审阅备注
            self.gp_review_user.clearData()                                                                 # 清空数据

    # 自动缩放 无效
    # def resizeEvent(self, event):#由于没有使用布局，这里当父窗口大小改变时自动改变webview的大小
    #     super(ReportReview, self).resizeEvent(event)
    #     self.wv_report_equip.resize(self.size())