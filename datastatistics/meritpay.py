from widgets.cwidget import *

# 医护绩效
class DN_MeritPay(DirTabWidget):

    def __init__(self):
        self.nodes = ['医生绩效','医生绩效(个人)','护理绩效','护理绩效(个人)','护理工作量','B超医生效率']
        super(DN_MeritPay,self).__init__('医生绩效',self.nodes)
