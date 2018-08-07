from result.tj_result_ui import *
from result.model import *

class TJResult(GolParasMixin,TJResultUI):

    def __init__(self,title):
        super(TJResult,self).__init__(title)
        self.init()
        self.initParas()
        # 绑定信号槽
        self.le_tjbh.returnPressed.connect(self.on_le_tjbh_f5)

    # 初始化参数
    def initParas(self):
        results = self.session.query(MT_TJ_KSDM).all()
        self.d_departs = dict([(result.ksbm,str2(result.ksmc)) for result in results])
        results = self.session.query(MT_TJ_XMDM).filter(MT_TJ_XMDM.sfzh == '1').all()
        self.d_items = dict([(result.xmbh, str2(result.xmmc)) for result in results])

    # 刷新页面
    def on_le_tjbh_f5(self):
        tjbh = self.le_tjbh.text()
        if len(tjbh)==9:
            user_result = self.session.query(MV_RYXX).filter(MV_RYXX.tjbh == tjbh).scalar()
            if user_result:
                # 人员信息
                self.gp_user.setData(user_result.to_dict)
                # 照片信息
                # photo_result = self.session.query(MT_TJ_PHOTO).filter(MT_TJ_PHOTO.tjbh == tjbh).scalar()
                # 科室信息
                ksxx = {}
                results = self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,MT_TJ_TJJLMXB.sfzh == '1').all()
                for result in results:
                    if result.ksbm not in list(ksxx.keys()):
                        ksxx[result.ksbm] = []
                    ksxx[result.ksbm].append(result.xmmc)
                # 项目信息
            else:
                mes_about(self,'该体检顾客未签到或者不存在！')
        else:
            mes_about(self,'请输入正确的体检编号！')
        self.le_tjbh.setText('')