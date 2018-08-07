from widgets.bwidget import *

#定制表格

class TableWidget(QTableWidget):

    def __init__(self,heads=None,parent=None):
        super(TableWidget,self).__init__(parent)
        # 基本设置
        self.setShowGrid(True)
        self.setSortingEnabled(True)            # 字符串排序功能
        self.setFrameShape(QFrame.NoFrame)      # 设置无边框
        self.verticalHeader().setVisible(True)  # 列表头

    # 通用载入
    def load(self,heads,datas:list):
        '''
        :param heads:
        :param datas:
        :return:
        '''
        if isinstance(heads,dict):
            self.setHorizontalHeaderLabels(heads.values())  # 行表头
            for row_index, row_data in enumerate(datas):
                # row_data:dict
                for col_index, col_name in enumerate(heads.keys()):
                    item = QTableWidgetItem(str(row_data[col_name]))
                    self.setItem(row_index, col_index, item)

        elif isinstance(heads,list):
            self.setHorizontalHeaderLabels(heads)
            for row_index, row_data in enumerate(datas):
                # row_data:list
                for col_index, col_name in enumerate(heads):
                    item = QTableWidgetItem(str(row_data[col_index]))
                    self.setItem(row_index, col_index, item)
        else:
            pass

    #
    def load2(self,heads:list,datas:list):
        '''
        :param heads:
        :param datas:
        :return:
        '''
        self.setHorizontalHeaderLabels(heads)  # 行表头
        for row_index, row_data in enumerate(datas):
            # row_data:list
            for col_index, col_name in enumerate(heads):
                item = QTableWidgetItem(str(row_data[col_index]))
                self.setItem(row_index, col_index, item)

    #
    def load3(self,heads:dict,datas:list):
        '''
        :param heads:
        :param datas:
        :return:
        '''
        if isinstance(heads,dict):
            self.setHorizontalHeaderLabels(heads.values())  # 行表头
            for row_index, row_data in enumerate(datas):
                # row_data:dict
                for col_index, col_name in enumerate(heads.keys()):
                    item = QTableWidgetItem(str(row_data[col_name]))
                    self.setItem(row_index, col_index, item)

    def refresh(self,heads,datas:list):
        self.clear()
        self.load(heads,datas)

'''
# self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch) #第二列扩展
'''

class ReadOnlyTable(TableWidget):

    def __init__(self,heads=None,parent=None):
        super(ReadOnlyTable,self).__init__(heads,parent)




