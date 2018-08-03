from widgets.cwidget import *

# 采集工作量统计
class CollectJobUI(Widget):

    def __init__(self):

        super(CollectJobUI,self).__init__()
        self.initUI()

    def initUI(self):
        lt_main = QHBoxLayout()
