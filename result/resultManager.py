from widgets.cwidget import *

# 采集样本管理：尿液、粪便、血液
class ResultManager(DirTabWidget):

    def __init__(self):
        nodes= ['体格检查','特殊检查','历史查询','工作量']
        super(ResultManager,self).__init__('结果录入',nodes)
        # self.addTab('留样采集')

    def addTab(self,title):
        super(ResultManager, self).addTab(title)
        if title=='体格检查':
            from result.tj_result import TJResult
            widget = TJResult('体格检查')
            self.rwidget.addPage(widget,Icon(title),title)