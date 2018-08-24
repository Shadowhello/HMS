from lis import CollectBlood,CollectHandover,CollectHistory
from C13 import BreathCheck
from widgets.cwidget import DirTabWidget,Icon

# 采集样本管理：尿液、粪便、血液
class VipManager(DirTabWidget):

    def __init__(self):
        nodes= ['呼气室','抽血采集','样本交接','采集历史']
        super(VipManager,self).__init__('采血台',nodes,False)
        self.addTab('呼气室')
        self.addTab('样本交接')
        self.addTab('抽血采集')

    def addTab(self,title):
        super(VipManager, self).addTab(title)
        if title=='抽血采集':
            self.collectBlood = CollectBlood()
            self.rwidget.addPage(self.collectBlood,Icon(title),title)

        elif title=='样本交接':
            widget=CollectHandover()
            self.rwidget.addPage(widget,Icon(title),title)

        elif title=='采集历史':
            widget=CollectHistory()
            self.rwidget.addPage(widget,Icon(title),title)

        elif title == '呼气室':
            widget = BreathCheck()
            self.rwidget.addPage(widget, Icon('呼气室'), '呼气室')

    def closeEvent(self, *args, **kwargs):
        super(VipManager, self).closeEvent(*args, **kwargs)
        if hasattr(self, 'collectBlood'):
            getattr(self, 'collectBlood').close()