from .report_ui import *
from utils.readparas import GolParasMixin

class ReportManager(GolParasMixin,Report_UI):

    def __init__(self):
        super(ReportManager, self).__init__("报告中心")