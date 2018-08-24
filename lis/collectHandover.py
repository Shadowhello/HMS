from lis.collectHandover_ui import *
from lis.model import *

class CollectHandover(CollectHandover_UI):

    def __init__(self):

        super(CollectHandover,self).__init__()
        self.initParas()
        self.btn_query.clicked.connect(self.on_btn_query_click)
        # self.gp_quick_search.returnPressed.connect(self.on_quick_search)         # 快速检索
        self.table_handover_master.itemClicked.connect(self.on_table_handover_master_clicked)
        self.btn_handover.clicked.connect(self.on_collect_handover)
        self.btn_receive.clicked.connect(self.on_collect_receive)

    def initParas(self):
        pass

    def on_collect_handover(self):

        row = self.table_handover_master.currentRow()
        if row==-1:
            mes_about(self,'请选择需要交接的样本！')
        else:
            if self.table_handover_master.item(row,5).text():
                mes_about(self,'样本已交接，请勿重复进行样本交接！')
            else:
                for row in self.SelectedRows(self.table_handover_master.selectedItems()):
                    self.table_handover_master.item(row, 5).setText(self.login_name)
                    self.table_handover_master.item(row, 6).setText(cur_datetime())
                    self.table_handover_master.item(row, 7).setText(self.collect_user.currentText())
                    #### 查询条件值
                    t_start = self.table_handover_master.item(row, 0).text()
                    t_end = self.table_handover_master.item(row, 1).text()
                    czqy = self.table_handover_master.item(row, 2).text()
                    sgys = self.table_handover_master.item(row, 3).text()
                    try:
                        self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.jllx.in_(('0010', '0011')),
                                                                MT_TJ_CZJLB.czqy==czqy,
                                                                 MT_TJ_CZJLB.czsj.between(t_start, t_end),
                                                                 cast(MT_TJ_CZJLB.bz, VARCHAR) == sgys).update({
                            MT_TJ_CZJLB.jjxm:self.login_name,
                            MT_TJ_CZJLB.jjsj:cur_datetime(),
                            MT_TJ_CZJLB.sjfs:self.collect_user.currentText()
                        },synchronize_session=False)
                        self.session.commit()
                        mes_about(self,'样本交接成功！')
                    except Exception as e:
                        self.session.rollback()
                        self.log.info(e)
                        mes_about(self,'更新数据库TJ_CZJLB 出错！错误信息：%s' %e)

    def on_collect_receive(self):

        row = self.table_handover_master.currentRow()
        if row == -1:
            mes_about(self, '请选择需要签收的样本！')
        else:
            if self.table_handover_master.item(row, 8).text():
                mes_about(self, '样本已签收，请勿重复进行样本交接！')
            else:
                if not self.table_handover_master.item(row, 5).text():
                    mes_about(self, '样本还未送检，请先送检再签收！')
                else:
                    for row in self.SelectedRows(self.table_handover_master.selectedItems()):
                        self.table_handover_master.item(row, 8).setText(self.login_name)
                        self.table_handover_master.item(row, 9).setText(cur_datetime())
                        #### 查询条件值
                        t_start = self.table_handover_master.item(row, 0).text()
                        t_end = self.table_handover_master.item(row, 1).text()
                        czqy = self.table_handover_master.item(row, 2).text()
                        sgys = self.table_handover_master.item(row, 3).text()
                        try:
                            self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.jllx.in_(('0010', '0011')),
                                                                    MT_TJ_CZJLB.czqy==czqy,
                                                                     MT_TJ_CZJLB.czsj.between(t_start, t_end),
                                                                     cast(MT_TJ_CZJLB.bz, VARCHAR) == sgys).update({
                                MT_TJ_CZJLB.jsxm:self.login_name,
                                MT_TJ_CZJLB.jssj:cur_datetime()
                            },synchronize_session=False)
                            self.session.commit()
                            mes_about(self,'样本签收成功！')
                        except Exception as e:
                            self.session.rollback()
                            mes_about(self,'更新数据库TJ_CZJLB 出错！错误信息：%s' %e)

    # 判断是否选择了多行
    def SelectedRows(self,items):
        rows = []
        for item in items:
           if item.row() not in rows:
               rows.append(item.row())

        return rows

    # 条件查询
    def on_btn_query_click(self):
        collect_time = self.collect_time.get_where_text()
        if self.collect_user2.currentText() =='所有':
            where_collect_user2 = ' AND 1 = 1 '
        else:
            where_collect_user2 = "AND CZXM = '%s' " %self.collect_user2.currentText()
        # 检索条件
        if self.collect_area.get_area == '明州':
            results = self.session.execute(get_handover2_sql(collect_time[0], collect_time[1], self.collect_area.get_area,where_collect_user2)).fetchall()
        else:
            results = self.session.execute(get_handover_sql(collect_time[0],collect_time[1],self.collect_area.get_area,where_collect_user2)).fetchall()
        self.table_handover_master.load(results)
        rowcount = self.table_handover_master.rowCount()
        self.gp_bottom_left.setTitle('样本交接汇总 (%s)' %rowcount)
        mes_about(self, '共检索出 %s 条数据！' %rowcount)

    def on_table_handover_master_clicked(self,QTableWidgetItem):
        t_start = self.table_handover_master.item(QTableWidgetItem.row(),0).text()
        t_end = self.table_handover_master.item(QTableWidgetItem.row(), 1).text()
        czqy = self.table_handover_master.item(QTableWidgetItem.row(),2).text()
        sgys = self.table_handover_master.item(QTableWidgetItem.row(), 3).text()
        if czqy=='明州':
            results = self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.jllx.in_(('0010', '0011')),
                                                             MT_TJ_CZJLB.czqy.like('%s%%' % czqy),
                                                             MT_TJ_CZJLB.czsj.between(t_start,t_end),
                                                             cast(MT_TJ_CZJLB.bz,VARCHAR) == sgys).all()
        else:
            results = self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.jllx.in_(('0010', '0011')),
                                                             MT_TJ_CZJLB.czqy == czqy,
                                                             # MT_TJ_CZJLB.czqy.like('%s%%' % self.collect_area.get_area),
                                                             MT_TJ_CZJLB.czsj.between(t_start,t_end),
                                                             cast(MT_TJ_CZJLB.bz,VARCHAR) == sgys).all()

        self.table_handover_detail.load((result.detail for result in results))
        self.gp_bottom_right.setTitle('样本交接详细 (%s)' %self.table_handover_detail.rowCount())
