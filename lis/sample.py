from widgets.cwidget import *

# 采集样本管理：尿液、粪便、血液
class SampleManager(DirTabWidget):

    def __init__(self):
        nodes= ['抽血采集','留样采集','样本交接','历史查询','工作量']
        super(SampleManager,self).__init__('采血台',nodes)
        self.addTab('样本交接')

    def addTab(self,title):
        super(SampleManager, self).addTab(title)
        if title=='抽血采集':
            from lis.collectblood import CollectBlood
            self.collectBlood = CollectBlood()
            self.rwidget.addPage(self.collectBlood,Icon(title),title)

        elif title=='留样采集':
            from lis.collecturine import CollectUrine
            widget=CollectUrine()
            self.rwidget.addPage(widget,Icon(title),title)

        elif title=='样本交接':
            from lis.collectHandover import CollectHandover
            widget=CollectHandover()
            self.rwidget.addPage(widget,Icon(title),title)

        elif title=='历史查询':
            from lis.collectHistory import CollectHistory
            widget=CollectHistory()
            self.rwidget.addPage(widget,Icon(title),title)

    def closeEvent(self, *args, **kwargs):
        super(SampleManager, self).closeEvent(*args, **kwargs)
        if hasattr(self, 'collectBlood'):
            getattr(self, 'collectBlood').close()