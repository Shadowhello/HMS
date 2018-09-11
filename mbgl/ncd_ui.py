from widgets.cwidget import *

class NCD_UI(DirTabWidget):

    def __init__(self,title):
        # 就诊预约
        nodes= ['疑似筛选']
        super(NCD_UI,self).__init__(title,nodes)


    def addTab(self,title):
        super(NCD_UI, self).addTab(title)
        if title=='疑似筛选':
            from .doubtful import Doubtful
            widget=Doubtful()
            self.rwidget.addPage(widget,Icon(title),title)

