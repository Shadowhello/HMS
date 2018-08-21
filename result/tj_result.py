from result.tj_result_ui import *
from result.model import *

class TJResult(GolParasMixin,TJResultUI):

    def __init__(self,title):
        super(TJResult,self).__init__(title)
        self.init()
        self.initParas()
        # 绑定信号槽
        self.gp_search.returnPressed.connect(self.on_le_tjbh_f5)
        self.cb_ksmc.currentIndexChanged.connect(self.on_cb_ksmc_change)
        self.cb_zhmc.currentTextChanged.connect(self.on_cb_zhmc_change)
        self.table_result_item.cellPressed.connect(self.on_table_default_result)
        # 双击设置结果
        self.table_result_item_default.itemDoubleClicked.connect(self.on_table_set_result)
        # 保存结果
        self.btn_finish.clicked.connect(self.on_btn_finish_save)

    # 初始化参数
    def initParas(self):
        # 获取用户 权限科室
        self.user_default_ksbm = gol.get_value('login_user_ksbms')
        # 基础科室代码
        results = self.session.query(MT_TJ_KSDM).all()
        self.base_ksmc = dict([(result.ksbm.rstrip(),str2(result.ksmc)) for result in results])
        results = self.session.query(MT_TJ_YGDM).all()
        self.base_user = dict([(result.yggh,str2(result.ygxm)) for result in results])
        results = self.session.query(MT_TJ_XMDM).filter(MT_TJ_XMDM.sfzh == '1').all()
        self.base_items = dict([(str2(result.xmmc),result.xmbh) for result in results])
        # 用于快速获取
        self.cur_tjbh = None  # 当前体检编号
        self.cur_zhbh = None  # 当前组合编号
        self.cur_ksbm = None  # 当前科室编号
        self.all_ksmc = None  # 当前所有科室名称
        self.ksxx = OrderedDict()        # 科室信息 示例如下：
        # OrderedDict([('0001', ['一般检查(身高体重血压)']),
        #              ('0002', ['内科']),
        #              ('0003', ['外科']),
        #              ('0007', ['耳鼻喉科']),
        #              ('0018', ['常规心电图']),
        #              ('0004', ['眼科']),
        #              ('0010', ['血糖', '肾功能', '肝功能常规', '甘油三酯', '总胆固醇']),
        #              ('0008', ['血常规']),
        #              ('0009', ['尿常规(自动化分析)']),
        #              ('0019', ['胸部正位(不出片)']),
        #              ('0028', ['凑整费', '一楼餐厅'])
        #           ])
        self.zhxx = OrderedDict()        # 组合信息 示例如下：
        # OrderedDict([('0101', ['韩雨', '2018-08-18 08:24:24', '已小结']),
        #              ('0102', ['宋新江', '2018-08-18 08:29:39', '已小结']),
        #              ('0202', ['姚兰', '2018-08-18 08:34:13', '已小结']),
        #              ('0302', ['胡雪琼', '2018-08-18 08:30:13', '已小结']),
        #              ('0806', ['周少华', '2018-08-18 00:00:00', '已小结']),
        #              ('0901', ['胡雪琼', '2018-08-18 08:30:16', '已小结']),
        #              ('1006', ['沈佳宜', '2018-08-18 11:18:37', '已小结']),
        #              ('1073', ['沈佳宜', '2018-08-18 11:18:37', '已小结']),
        #              ('1074', ['沈佳宜', '2018-08-18 11:18:37', '已小结']),
        #              ('1079', ['沈佳宜', '2018-08-18 11:18:37', '已小结']),
        #              ('1082', ['沈佳宜', '2018-08-18 11:18:37', '已小结']),
        #              ('1202', ['周挺', '2018-08-18 10:03:46', '已小结']),
        #              ('1308', ['张建伟', '2018-08-18 10:22:37', '已小结']),
        #              ('501716', ['李振宇', '2018-08-18 16:58:48', '已小结']),
        #              ('888888', ['', '', '已小结']),
        #              ('999999', ['', '', '已小结'])
        #              ])

    # 清空基础数据
    def clearData(self):
        # 用于快速获取
        self.cur_tjbh = None  # 当前体检编号
        self.cur_zhbh = None  # 当前组合编号
        self.cur_ksbm = None  # 当前科室编号
        self.all_ksmc = None  # 当前所有科室名称
        self.ksxx = OrderedDict()        # 科室信息
        self.zhxx = OrderedDict()        # 组合项目

    # 刷新页面
    def on_le_tjbh_f5(self):
        # 清空
        self.clearData()
        self.cur_tjbh = self.gp_search.text()
        if len(self.cur_tjbh)==9:
            # 获取人员信息
            user_result = self.session.query(MV_RYXX).filter(MV_RYXX.tjbh == self.cur_tjbh).scalar()
            if user_result:
                # 设置人员信息
                self.gp_user.setData(user_result.to_dict)
                # 照片信息
                # photo_result = self.session.query(MT_TJ_PHOTO).filter(MT_TJ_PHOTO.tjbh == tjbh).scalar()
                # 获取科室信息
                results = self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == self.cur_tjbh,MT_TJ_TJJLMXB.sfzh == '1').all()
                # 分拆装包
                for result in results:
                    # 用户有权限的科室 才展示
                    # result.ksbm.rstrip() 数据库存储的是CHAR 类型 需要删除空格 设计的不好！
                    print(self.user_default_ksbm,result.ksbm)
                    if result.ksbm.rstrip() in self.user_default_ksbm:
                        # 科室 组合项目信息 打包一起
                        if result.ksbm.rstrip() not in list(self.ksxx.keys()):
                            # 不存在则添加
                            self.ksxx[result.ksbm.rstrip()] = []
                        self.ksxx[result.ksbm.rstrip()].append(str2(result.xmmc))
                        # 组合项目 、检查日期、检查时间、检查状态 打包一起
                        if result.zhbh not in list(self.zhxx.keys()):
                            self.zhxx[result.zhbh] = []
                        # 此时需要获取 日期和医生
                        self.zhxx[result.zhbh].append(self.base_user.get(result.get_shys,''))
                        self.zhxx[result.zhbh].append(result.get_shrq)
                        self.zhxx[result.zhbh].append(result.item_state)

                # 设置科室信息
                self.cb_ksmc.addItems([self.base_ksmc[key] for key in self.ksxx.keys()])


                # 项目信息
                from pprint import pprint
                pprint(self.ksxx)
                pprint(self.zhxx)
            else:
                mes_about(self,'该体检顾客未签到或者不存在！')
        else:
            mes_about(self,'请输入正确的体检编号！')
        self.gp_search.setText('')

    # 科室项目变化信号-> 处理组合项目
    def on_cb_ksmc_change(self,p_index:int):
        # 先清空上次
        self.cb_zhmc.clear()
        # 更新变量
        self.cur_ksbm = list(self.ksxx.keys())[p_index]
        # 重新赋值
        zhxms = self.ksxx[self.cur_ksbm]
        self.cb_zhmc.addItems(zhxms)


    # 组合项目变化信号 -> 处理子项 及基本信息
    def on_cb_zhmc_change(self,p_str:str):
        if p_str:
            self.cur_zhbh = self.base_items.get(p_str,'')
            if self.cur_zhbh:
                info = self.zhxx[self.cur_zhbh]
                self.lb_jcys.setText(info[0])
                self.lb_jcrq.setText(info[1])
                self.lb_state.setText(info[2])
            else:
                print('不存在key：%s' % p_str)
        else:
            print('不存在下拉内容：%s' %p_str)

        # 更新子项目
        results = self.session.query(MT_TJ_TJJLMXB).filter(
                                                            MT_TJ_TJJLMXB.tjbh == self.cur_tjbh,
                                                            MT_TJ_TJJLMXB.zhbh == self.cur_zhbh,
                                                            MT_TJ_TJJLMXB.sfzh == '0'
                                                        ).order_by(MT_TJ_TJJLMXB.xssx).all()

        self.table_result_item.load([result.get_edit_items for result in results])
        # 显示状态图片、更新按钮名称
        if self.lb_state.text()=='已小结':
            self.lb_state_pic.show2()
            self.btn_finish.setText('取消保存')
        else:
            self.lb_state_pic.show2(False)
            self.btn_finish.setText('保存')

    # 单击获取默认结果
    def on_table_default_result(self,row,col):
        results = self.session.query(MT_TJ_XMJG).filter(MT_TJ_XMJG.xmbh == self.table_result_item.item(row,0).text(), cast(MT_TJ_XMJG.jg,VARCHAR)!='').all()
        self.table_result_item_default.clear()
        for result in results:
            self.table_result_item_default.addItem(QListWidgetItem(str2(result.jg)))

    # 双击设置结果
    def on_table_set_result(self):
        currentitem=self.table_result_item.currentItem()
        if currentitem:
            if self.table_result_item_default.is_left:
                currentitem.setText(self.table_result_item_default.currentText())
            else:
                new_text="%s,%s" %(currentitem.text(),self.table_result_item_default.currentText())
                currentitem.setText(new_text)
        else:
            mes_about(self,'请先选择项目！')

    # 保存结果
    def on_btn_finish_save(self):
        if self.btn_finish.text()=='取消保存':
            dialog = mes_warn(self,"体检顾客(%s)，当前(%s)科室:(%s)项目已完成。\n\n您确定取消结果，重新录入？" %(self.cur_tjbh,self.cb_ksmc.currentText(),self.cb_zhmc.currentText()))
            if dialog != QMessageBox.Yes:
                return
            else:
                self.btn_finish.setText('保存')
                self.lb_jcys.setText('')
                self.lb_jcrq.setText('')
                self.lb_state.setText('')
                self.lb_state_pic.show2(False)
        else:
            self.btn_finish.setText('取消保存')
            self.lb_jcys.setText(self.login_name)
            self.lb_jcrq.setText(cur_datetime())
            self.lb_state.setText('已小结')
            self.lb_state_pic.show2(True)
            mes_about(self,'保存成功！')

def cur_datetime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))