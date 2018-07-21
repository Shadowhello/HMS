from utils.bmodel import *
from utils.base import str2

#用户表
class MV_EQUIP_JCMX(BaseModel):

    __tablename__ = 'V_EQUIP_JCMX'

    tjbh = Column(VARCHAR(20), primary_key=True)
    xm = Column(VARCHAR(20),nullable=False)
    xb = Column(VARCHAR(20),nullable=False)
    nl = Column(Integer, nullable=False)
    xmmc = Column(VARCHAR(50), nullable=False)
    zxpb = Column(CHAR(1), nullable=False)
    jsbz = Column(CHAR(1), nullable=False)
    qzjs = Column(CHAR(1), nullable=False)
    xmbh = Column(VARCHAR(20), nullable=False)
    ysgh = Column(VARCHAR(20), nullable=False)
    ysxm = Column(VARCHAR(20), nullable=False)

    @property
    def inspect_state(self):
        if getattr(self, "qzjs")=='1':
            return '已拒检'
        else:
            if getattr(self, "jsbz") == '1':
                return '已小结'
            else:
                if getattr(self, "zxpb") == '0':
                    return '核实'
                elif getattr(self, "zxpb") == '1':
                    return '已回写'
                elif getattr(self, "zxpb") == '2':
                    return '已登记'
                elif getattr(self, "zxpb") == '3':
                    return '已检查'
                elif getattr(self, "zxpb") == '4':
                    return '已抽血'
                elif getattr(self, "zxpb") == '5':
                    return '已留样'
                else:
                    return '未结束'

    @property
    def to_dict(self):
        tmp={}
        tmp["tjbh"] = getattr(self, "tjbh")
        tmp["xm"] = str2(getattr(self, "xm"))
        tmp["xb"] = str2(getattr(self, "xb"))
        tmp["nl"] = str(getattr(self, "nl"))
        tmp["xmmc"] = str2(getattr(self, "xmmc"))
        tmp["state"] = self.inspect_state
        return tmp


get_equip_inspect_sql = '''

SELECT 
a.TJBH,
b.XM,
(CASE b.XB WHEN '1' THEN '男' WHEN '2'  THEN '女' ELSE '' END) AS XB,
a.NL,
c.XMMC,
c.ZXPB,
c.jsbz,
c.qzjs,
c.XMBH,
c.JCYS AS ysgh,
(SELECT YGXM FROM TJ_YGDM WHERE YGGH=c.JCYS) AS ysxm


FROM TJ_TJDJB a INNER JOIN TJ_TJDAB b ON a.DABH=b.DABH AND  (a.del <> '1' or a.del is null) and a.QD='1' AND a.QDRQ>=substring(convert(char,getdate(),120),1,10) 

INNER JOIN TJ_TJJLMXB c ON a.TJBH = c.TJBH AND c.SFZH='1'
'''