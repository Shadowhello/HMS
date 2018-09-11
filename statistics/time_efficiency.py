from widgets.cwidget import *

# 体检时效统计
class TimeEfficency(DirTabWidget):

    def __init__(self):
        self.nodes = ['满意度','项目结果出具','报告时效','报告打印率']
        super(TimeEfficency,self).__init__('体检时效',self.nodes,False)
        self.addTab('满意度')
        self.addTab('项目结果超期')
        self.addTab('报告时效')
        self.addTab('报告打印率')

    def addTab(self, title):
        super(TimeEfficency, self).addTab(title)
        if title == '满意度':
            from .custom_satisfaction import CustomSatisfaction
            self.custom_satisfaction = CustomSatisfaction()
            self.rwidget.addPage(self.custom_satisfaction, Icon(title), title)
        elif title == '项目结果超期':
            from .item_result_return import ItemResultReturn
            self.item_result = ItemResultReturn()
            self.rwidget.addPage(self.item_result, Icon(title), title)
        elif title == '报告时效':
            from report.report_time_efficiency import ReportTimeEfficiency
            self.report_time = ReportTimeEfficiency()
            self.rwidget.addPage(self.report_time, Icon(title), title)
        elif title == '报告打印率':
            from report.report_print_efficiency import ReportPrintTimeEffect
            self.report_print = ReportPrintTimeEffect()
            self.rwidget.addPage(self.report_print, Icon(title), title)



