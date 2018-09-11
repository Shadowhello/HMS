from app_interface.i_lis_result_ui import *
from app_interface.model import *
from app_interface.i_receive_result import *

class LisResult(LisResultUI):

    def __init__(self,parent=None):
        super(LisResult,self).__init__('检验系统',parent)
        # 绑定信号槽
        self.table_inspect_master.itemClicked.connect(self.on_table_show_detail)
        # 右侧详细结果 字典
        self.detail_datas = None
        self.btn_receive.clicked.connect(self.on_btn_receive_click)
        # 初始化项目字典
        self.item_match = {}
        results = self.session.execute(get_lis_match_pes_sql()).fetchall()
        for result in results:
            if ',' in result[0]:
                self.item_match[result[0].split(',')[0]] = result[1]
                self.item_match[result[0].split(',')[1]] = result[1]
            else:
                self.item_match[result[0]] = result[1]


    def setData(self,datas):
        # 清空数据
        self.bgys.setText('')
        self.bgsj.setText('')
        self.shys.setText('')
        self.shsj.setText('')
        #self.pacs_jg.setText('')
        #self.pacs_zd.setText('')
        self.table_inspect_master.load(datas['pes'])
        self.detail_datas = datas['lis']

    #单击主的 出来子的
    def on_table_show_detail(self,tableWidgetItem):
        row = tableWidgetItem.row()
        tjtm = self.table_inspect_master.item(row,7).text()+self.table_inspect_master.item(row,1).text()
        self.table_inspect_detail.load(self.detail_datas.get(tjtm,[]))
        bgys = self.table_inspect_master.item(row, 3).text()
        bgrq = self.table_inspect_master.item(row, 4).text()
        shys = self.table_inspect_master.item(row, 5).text()
        shrq = self.table_inspect_master.item(row, 6).text()
        self.bgys.setText(bgys)
        self.bgsj.setText(bgrq)
        self.shys.setText(shys)
        self.shsj.setText(shrq)

    # 强制接收
    def on_btn_receive_click(self):
        # 首先判断体检系统是否已拒检、已结束
        if self.table_inspect_master.currentRow()==-1:
            mes_about(self,'请选择行！')
        else:
            if self.table_inspect_master.item(self.table_inspect_master.currentRow(),0).text()=='已审核':
                mes_about(self,'结果已存在，不要重复接收！')
            else:
                if not self.table_inspect_detail.rowCount():
                    mes_about(self, '没有结果，无法接收！')
                else:
                    tjbh = self.table_inspect_master.getCurItemValueOfKey('tjbh')
                    tmbh = self.table_inspect_master.getCurItemValueOfKey('tmbh')
                    datas=[]
                    results = self.session_lis.query(MV_VI_TJ_RESULT).filter(MV_VI_TJ_RESULT.tjbh == tjbh,MV_VI_TJ_RESULT.tmh == tmbh).all()
                    for result in results:
                        datas.append(lis2pes(result.to_dict,self.item_match))
                        # print(lis2pes(result.to_dict,self.item_match))

                    mes_about(self,'接收成功！')






