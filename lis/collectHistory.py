from lis.collectHistory_ui import *
from lis.model import *

class CollectHistory(CollectHistory_UI):

    def __init__(self):

        super(CollectHistory,self).__init__()
        self.initParas()
        self.btn_query.clicked.connect(self.on_btn_query_click)

    def initParas(self):
        pass

    # 查询
    def on_btn_query_click(self):
        collect_time = self.collect_time.get_where_text()
        results = self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.jllx.in_(('0010', '0011')),MT_TJ_CZJLB.czsj.between(collect_time[0],collect_time[1])).all()
        self.table_history.load((result.to_dict for result in results))