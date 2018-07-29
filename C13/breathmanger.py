from widgets.cwidget import *

# C13 呼气试验管理
class BreathManager(TabWidget):

    def __init__(self,parent=None):
        super(BreathManager,self).__init__(parent)
        self.initPages()

    def initPages(self):
        nodes = ['吹气中', '结果录入', '历史查询', '工作量']
        from C13.breathcheck import BreathCheck
        self.breathCheck = BreathCheck()
        self.addPage(self.breathCheck,Icon('呼气室'),'呼气室')

