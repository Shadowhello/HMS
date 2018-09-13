from app_interface.i_pis_result_ui import *
from app_interface.model import *

class PisResult(PisResultUI):

    def __init__(self,parent=None):
        super(PisResult,self).__init__('病理系统',parent)

        # 绑定信号槽
        self.table_inspect.itemClicked.connect(self.on_table_refresh)
        self.btn_receive.clicked.connect(self.on_btn_receive_click)
        self.painter = None

    def on_table_refresh(self,tableWidgetItem):
        row = tableWidgetItem.row()
        bgys = self.table_inspect.getItemValueOfKey(row,'ReportDoc')
        bgrq = self.table_inspect.getItemValueOfKey(row,'ReportDate')
        shys = self.table_inspect.getItemValueOfKey(row,'AuditDoc')
        shrq = self.table_inspect.getItemValueOfKey(row,'AuditDate')
        xmjg = self.table_inspect.getItemValueOfKey(row,'TJSJ')
        xmzd = self.table_inspect.getItemValueOfKey(row,'TJZD')
        # bgys = self.table_inspect.item(row, 6).text()
        # bgrq = self.table_inspect.item(row, 7).text()
        # shys = self.table_inspect.item(row, 8).text()
        # shrq = self.table_inspect.item(row, 9).text()
        # xmjg = self.table_inspect.item(row, 10).text()
        # xmzd = self.table_inspect.item(row, 11).text()
        self.bgys.setText(bgys)
        self.bgsj.setText(bgrq)
        self.shys.setText(shys)
        self.shsj.setText(shrq)
        self.pis_jg.setText(xmjg)
        self.pis_zd.setText(xmzd)

    def setData(self,datas):
        # 清空数据
        self.bgys.setText('')
        self.bgsj.setText('')
        self.shys.setText('')
        self.shsj.setText('')
        self.pis_jg.setText('')
        self.pis_zd.setText('')
        self.table_inspect.load(datas)

    # 强制接收
    def on_btn_receive_click(self):
        # 首先判断体检系统是否已拒检、已结束
        if self.table_inspect.currentRow()==-1:
            mes_about(self,'请选择行！')
        else:
            content = self.table_inspect.getLastItemValue(self.table_inspect.currentRow())
            tjbh = content[0:9]
            xmbh = content[9:]
            path = self.table_inspect.getItemValueOfKey(self.table_inspect.currentRow(),'filename')
            # 未审核 不能接收
            if self.table_inspect.item(self.table_inspect.currentRow(),0).text()=='已审核':
                result = self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,MT_TJ_TJJLMXB.xmbh == xmbh).scalar()
                if result:
                    if result.item_state=='已拒检':
                        mes_about(self,'体检系统中该项目已被拒检！')
                    # -- 2018-09-13 zhufd 取消此代码 原因：适应于医生退回护士追踪，B超等结果重新接收一次
                    # elif result.item_state=='已小结':
                    #     mes_about(self,'体检系统中该项目已被小结，请勿重复接收！')
                    else:
                        try:
                            # 组合和子项 均写入 jcrq，jcys，zxpb，jsbz
                            self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,MT_TJ_TJJLMXB.zhbh == xmbh).update({
                                MT_TJ_TJJLMXB.jcys:self.shys.text(),
                                MT_TJ_TJJLMXB.jcrq:self.shsj.text(),
                                MT_TJ_TJJLMXB.zxpb: '1',
                                MT_TJ_TJJLMXB.jsbz: '1',
                                MT_TJ_TJJLMXB.ycbz: '1'
                            },synchronize_session=False)
                            # 子项目 写入结果、诊断
                            self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,MT_TJ_TJJLMXB.zhbh == xmbh,MT_TJ_TJJLMXB.sfzh=='1').update({
                                MT_TJ_TJJLMXB.jg: self.pis_jg.toPlainText(),
                                MT_TJ_TJJLMXB.zd:self.pis_zd.text()
                            },synchronize_session=False)
                            # 写入TJ_PACS_PIC
                            pic_obj = {
                                'tjbh':tjbh,'zhbh':xmbh,'picpath':path,'picname':path,'path':path,
                                'pk':content,'ftp_bz':'0','ksbm':'0026'
                            }
                            self.session.bulk_insert_mappings(MT_TJ_PACS_PIC, [pic_obj])
                            # 写入 TJ_CZJLB
                            jlnr = '''检查医生：%s；检查日期：%s；结果：%s；诊断：%s''' % (
                            self.shys.text(), self.shsj.text(), self.pis_jg.toPlainText(), self.pis_zd.text())
                            data_obj = {'jllx': '0102', 'jlmc': '结果强制接收', 'tjbh':tjbh, 'mxbh': xmbh,
                                             'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area,
                                             'jlnr': jlnr, 'bz': None}
                            self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                            self.session.commit()
                            mes_about(self,'结果接收成功！')

                        except Exception as e:
                            self.session.rollback()
                            mes_about(self,'更新数据库MT_TJ_TJJLMXB 出错！错误信息：%s' %e)
                else:
                    mes_about(self, '体检系统中不存在该项目')
            else:
                mes_about(self,'当前报告未审核，不能接收结果！')