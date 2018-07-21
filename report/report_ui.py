from widgets.cwidget import *

class Report_UI(DirTabWidget):

    def __init__(self,title):
        self.nodes = ['报告追踪', '报告审阅', '报告打印', '报告整理', '报告领取', '报告进度', '报告发布', '设备报告']
        super(Report_UI,self).__init__(title,self.nodes)


    def addTab(self,title):
        super(Report_UI, self).addTab(title)
        if title=='报告追踪':
            from .report_track import ReportTrack
            widget=ReportTrack()
            self.rwidget.addPage(widget,Icon(title),title)


