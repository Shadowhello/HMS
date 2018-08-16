from .report_print_ui import *
from .model import *

# 报告追踪
class ReportPrint(ReportPrintUI):

    def __init__(self):
        super(ReportPrint, self).__init__()
        self.initParas()

    def initParas(self):
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()
        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)

        self.lt_where_search.s_dwbh.setValues(self.dwmc_bh,self.dwmc_py)