from widgets.cwidget import *

# 医护绩效
class DN_MeritPay(DirTabWidget):

    def __init__(self):
        self.nodes = ['护理绩效']
        super(DN_MeritPay,self).__init__('医护绩效',self.nodes)
        self.addTab('护理绩效')

    def addTab(self, title):
        super(DN_MeritPay, self).addTab(title)
        if title == '护理绩效':
            from .achievements_nurse import AchievementsNurse
            self.achieve_nurse = AchievementsNurse()
            self.rwidget.addPage(self.achieve_nurse, Icon(title), title)