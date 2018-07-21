from .report_ui import *
from utils.readparas import GolParasMixin

class ReportCenter(GolParasMixin,Report_UI):

    def __init__(self):
        super(ReportCenter, self).__init__("报告中心")