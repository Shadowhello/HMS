from .report_equip_ui import *
from .model import *
from collections import OrderedDict

# 设备报告
class ReportEquip(ReportEquipUI):

    def __init__(self):
        super(ReportEquip, self).__init__()
        # 初始化必要数据
        self.initParas()
        # 绑定信号槽
        self.btn_query.clicked.connect(self.on_btn_query_click)
        self.table_report_equip.doubleClicked.connect(self.on_table_report_equip_click)
        # 按钮栏
        self.gp_quick_search.returnPressed.connect(self.on_quick_search)    # 快速检索

    def initParas(self):
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()
        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)

        self.gp_where_search.s_dwbh.setValues(self.dwmc_bh,self.dwmc_py)

    def on_btn_query_click(self):
        t_start,t_end = self.gp_where_search.date_range     # 日期范围
        dwbh = self.gp_where_search.where_dwbh              # 单位编号
        equip_type = self.cb_equip_type.get_equip_type()    #设备编号
        # 执行查询
        if equip_type:
            if dwbh:
                if self.cb_user.currentText()=='所有':
                    results=self.session.query(MT_TJ_EQUIP).filter(
                                MT_TJ_EQUIP.equip_type==equip_type,
                                MT_TJ_EQUIP.operate_time.between(t_start,t_end),
                                MT_TJ_EQUIP.tjbh.like('%s%%' % dwbh)
                            ).all()
                else:
                    results=self.session.query(MT_TJ_EQUIP).filter(
                                MT_TJ_EQUIP.equip_type==equip_type,
                                MT_TJ_EQUIP.operate_time.between(t_start,t_end),
                                MT_TJ_EQUIP.operator2 == self.cb_user.currentText(),
                                MT_TJ_EQUIP.tjbh.like('%s%%' % dwbh)
                            ).all()
            else:
                if self.cb_user.currentText() == '所有':
                    results =self.session.query(MT_TJ_EQUIP).filter(
                                MT_TJ_EQUIP.equip_type==equip_type,
                                MT_TJ_EQUIP.operate_time.between(t_start,t_end)
                            ).all()
                else:
                    results =self.session.query(MT_TJ_EQUIP).filter(
                                MT_TJ_EQUIP.equip_type==equip_type,
                                MT_TJ_EQUIP.operate_time.between(t_start,t_end),
                                MT_TJ_EQUIP.operator2 == self.cb_user.currentText()
                            ).all()
        else:
            if dwbh:
                if self.cb_user.currentText() == '所有':
                    results =self.session.query(MT_TJ_EQUIP).filter(
                                MT_TJ_EQUIP.operate_time.between(t_start,t_end),
                                MT_TJ_EQUIP.tjbh.like('%s%%' % dwbh)
                            ).all()
                else:
                    results =self.session.query(MT_TJ_EQUIP).filter(
                                MT_TJ_EQUIP.operate_time.between(t_start,t_end),
                                MT_TJ_EQUIP.operator2 == self.cb_user.currentText(),
                                MT_TJ_EQUIP.tjbh.like('%s%%' % dwbh)
                            ).all()
            else:
                if self.cb_user.currentText() == '所有':
                    results =self.session.query(MT_TJ_EQUIP).filter(
                                MT_TJ_EQUIP.operate_time.between(t_start,t_end)
                            ).all()
                else:
                    results =self.session.query(MT_TJ_EQUIP).filter(
                                MT_TJ_EQUIP.operate_time.between(t_start,t_end),
                                MT_TJ_EQUIP.operator2 == self.cb_user.currentText(),
                            ).all()
        # 载入数据
        self.table_report_equip.load((result.to_dict for result in results))
        self.gp_table.setTitle('检查完成列表（%s）' %self.table_report_equip.rowCount())

    # 预览报告
    # http://localhost:4001/web/viewer.html?file=\equip\2018\2018-08\2018-08-15\172960088_08.pdf
    def on_table_report_equip_click(self,QModelIndex):
        fpath = self.table_report_equip.item(QModelIndex.row(),6).text()
        url = gol.get_value('api_equip_show','')
        print(url %fpath)
        if url:
            self.wv_report_equip.load(url %fpath)

            # self.wv_report_equip.show()

        else:
            mes_about(self,'未配置：api_equip_show 参数！')

    # 快速检索
    def on_quick_search(self, p1_str, p2_str):
        if p1_str == 'tjbh':
            results = self.session.query(MT_TJ_EQUIP).filter(MT_TJ_EQUIP.tjbh==p2_str).all()
        elif p1_str == 'xm':
            results = self.session.query(MT_TJ_EQUIP).filter(MT_TJ_EQUIP.patient == p2_str).all()
        else:
            results =[]
        if results:
            # 载入数据
            self.table_report_equip.load((result.to_dict for result in results))
        self.gp_table.setTitle('检查完成列表（%s）' % self.table_report_equip.rowCount())


