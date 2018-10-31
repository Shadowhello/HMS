from widgets.cwidget import *
from utils import gol
# 报告追踪
from .report_track import ReportTrack
# 报告审阅
from .report_review import ReportReview
# 报告打印
from .report_print import ReportPrint
# 报告整理
from .report_order import ReportOrder
# 设备报告
from .report_equip import ReportEquip
# 报告进度
from .report_progress import ReportProgress


class Report_UI(DirTabWidget):

    def __init__(self,title):
        self.nodes = ['报告追踪', '报告审阅', '报告打印','报告整理','设备报告','报告进度']
        super(Report_UI,self).__init__(title,self.nodes)
        default_menu_name = gol.get_value('menu_child_name','')
        if default_menu_name in self.nodes:
            self.addTab(default_menu_name)

    def addTab(self,title):
        super(Report_UI, self).addTab(title)
        if title=='报告追踪':

            widget=ReportTrack()
        elif title=='报告审阅':

            widget=ReportReview()
        elif title=='报告打印':

            widget=ReportPrint()
        elif title=='设备报告':

            widget=ReportEquip()
        elif title=='报告进度':

            widget=ReportProgress()
        else:

            widget=ReportOrder()
        self.rwidget.addPage(widget,Icon(title),title)


