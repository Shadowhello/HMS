from lis.collectHistory_ui import *
from lis.model import *

class CollectHistory(CollectHistory_UI):

    def __init__(self):

        super(CollectHistory,self).__init__()
        self.initParas()
        self.btn_query.clicked.connect(self.on_btn_query_click)
        self.gp_quick_search.returnPressed.connect(self.on_quick_search)         # 快速检索

    def initParas(self):
        pass

    # 查询
    def on_btn_query_click(self):
        collect_time = self.collect_time.get_where_text()
        # 检索条件
        if self.collect_user.currentText()== '所有':
            if self.collect_area.get_area == '所有':
                results = self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.jllx.in_(('0010', '0011')),MT_TJ_CZJLB.czsj.between(collect_time[0],collect_time[1])).all()
            else:
                results = self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.jllx.in_(('0010', '0011')),
                                                                 MT_TJ_CZJLB.czqy.like('%s%%' %self.collect_area.get_area),
                                                                 MT_TJ_CZJLB.czsj.between(collect_time[0],
                                                                                          collect_time[1])).all()
        else:
            results = self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.jllx.in_(('0010', '0011')),
                                                             MT_TJ_CZJLB.czqy.like('%s%%' % self.collect_area.get_area),
                                                             MT_TJ_CZJLB.czxm==self.collect_user.currentText(),
                                                             MT_TJ_CZJLB.czsj.between(collect_time[0],
                                                                                      collect_time[1])).all()

        self.table_history.load((result.to_dict for result in results))
        mes_about(self, '共检索出 %s 条数据！' % self.table_history.rowCount())

    def on_quick_search(self,p1_str,p2_str):
        if p1_str == 'tjbh':
            results = self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.jllx.in_(('0010', '0011')), MT_TJ_CZJLB.tjbh==p2_str).all()
            self.table_history.load((result.to_dict for result in results))
        # elif p1_str == 'sjhm':
        #     where_str = " TJ_TJDAB.SJHM = '%s' " % p2_str
        # elif p1_str == 'sfzh':
        #     where_str = " TJ_TJDAB.SFZH = '%s' " % p2_str
        # else:
        #     where_str = " TJ_TJDAB.XM ='%s' " % p2_str

        mes_about(self,'共检索出 %s 条数据！' %self.table_history.rowCount())