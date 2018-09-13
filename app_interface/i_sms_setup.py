from widgets.cwidget import *
# 短信设置
# 1、短信模板设置
# 2、自动发送短信单位设置

class SmsManager(DirTabWidget):

    def __init__(self):
        nodes= ['自动发送','短信模板']
        super(SmsManager,self).__init__('采血台',nodes)
        self.addTab('抽血采集')

    def addTab(self,title):
        super(SmsManager, self).addTab(title)
        if title=='抽血采集':
            from lis.collectblood import CollectBlood
            self.collectBlood = CollectBlood()
            self.rwidget.addPage(self.collectBlood,Icon(title),title)