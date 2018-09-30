from widgets.cwidget import *
from utils import gol

# 采集样本管理：尿液、粪便、血液
class RegisterManager(DirTabWidget):

    def __init__(self):
        nodes= ['导检收单']
        super(RegisterManager,self).__init__('登记管理',nodes)
        default_menu_name = gol.get_value('menu_child_name','')
        if default_menu_name in nodes:
            self.addTab(default_menu_name)
        self.addTab('导检收单')

    def addTab(self,title):
        super(RegisterManager, self).addTab(title)
        if title=='导检收单':
            from .tjsd import TJSD
            self.tjsd = TJSD()
            self.rwidget.addPage(self.tjsd,Icon(title),title)


    # def closeEvent(self, *args, **kwargs):
    #     super(SampleManager, self).closeEvent(*args, **kwargs)
    #     if hasattr(self, 'collectBlood'):
    #         getattr(self, 'collectBlood').close()