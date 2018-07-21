from .report_track_ui import ReportTrackUI
from report.model import *
from widgets.cwidget import *

# 报告追踪

class ReportTrack(ReportTrackUI):

    def __init__(self):
        super(ReportTrack, self).__init__()
        self.initParas()
        #################### 信号槽  ############################
        # 右键菜单
        self.table_track.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.table_track.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单

        self.btn_export.clicked.connect(self.on_btn_export)

    def initParas(self):
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()

        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)

        self.lt_search.s_dwbh.setValues(self.dwmc_bh,self.dwmc_py)

    # 右键功能
    def onTableMenu(self,pos):
        row_num = -1
        indexs=self.table.selectionModel().selection().indexes()
        if indexs:
            for i in indexs:
                row_num = i.row()

            menu = QMenu()
            item1 = menu.addAction(Icon("短信"), "发送预约短信")
            item2 = menu.addAction(Icon("短信"), "编辑预约短信")
            item3 = menu.addAction(Icon("预约"), "设置预约客户")
            item4 = menu.addAction(Icon("预约"), "电话记录")
            item5 = menu.addAction(Icon("预约"), "本次体检结果")
            item6 = menu.addAction(Icon("预约"), "历年体检结果")
            item7 = menu.addAction(Icon("预约"), "浏览体检报告")
            item8 = menu.addAction(Icon("预约"), "下载电子报告")

            action = menu.exec_(self.table.mapToGlobal(pos))

    # 导出功能
    def on_btn_export(self):
        self.table_track.export()