from widgets.cwidget import *
from utils import gol

class Report_UI(DirTabWidget):

    def __init__(self,title):
        # '报告发布' '报告领取' '报告整理' '报告进度'
        self.nodes = ['报告追踪', '报告审阅', '报告打印','报告整理','设备报告','报告进度']
        super(Report_UI,self).__init__(title,self.nodes)
        default_menu_name = gol.get_value('menu_child_name','')
        if default_menu_name in self.nodes:
            self.addTab(default_menu_name)

    def addTab(self,title):
        super(Report_UI, self).addTab(title)
        if title=='报告追踪':
            from .report_track import ReportTrack
            widget=ReportTrack()
            self.rwidget.addPage(widget,Icon(title),title)
        elif title=='报告审阅':
            from .report_review import ReportReview
            widget=ReportReview()
            self.rwidget.addPage(widget,Icon(title),title)
        elif title=='报告打印':
            from .report_print import ReportPrint
            widget=ReportPrint()
            self.rwidget.addPage(widget,Icon(title),title)
        elif title=='设备报告':
            from .report_equip import ReportEquip
            widget=ReportEquip()
            self.rwidget.addPage(widget,Icon(title),title)
        elif title=='报告进度':
            from .report_progress import ReportProgress
            widget=ReportProgress()
            self.rwidget.addPage(widget,Icon(title),title)


