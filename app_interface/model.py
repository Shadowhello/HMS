from utils.bmodel import *

# 电话记录 实际应该同步 TJ_CZJLB 此表为过渡
class MT_TJ_DHGTJLB(BaseModel):

    __tablename__ = 'TJ_DHGTJLB'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    tjbh = Column(String(16), nullable=False)       # 体检编号
    jllx = Column(Integer, nullable=True)           # 记录类型
    jlnr = Column(DateTime, nullable=True)          # 记录内容
    jlr = Column(String(16), nullable=False)        # 记录人
    jlsj = Column(String(16), nullable=False)       # 记录时间

    @property
    def to_dict(self):
        return {
            'tjbh':getattr(self, "tjbh", ''),
            'jllx': self.jllx_v,
            'jlsj': str(getattr(self, "jlsj", ''))[0:19],
            'jlr':str2(getattr(self, "jlr", '')),
            'jlnr': str2(getattr(self, "jlnr", ''))
        }


    @property
    def jllx_v(self):
        if getattr(self, "jllx", '')== '1':
            return '项目追踪'
        elif getattr(self, "jllx", '')== '2':
            return '阳性沟通'
        elif getattr(self, "jllx", '')== '3':
            return '检后回访'
        elif getattr(self, "jllx", '')== '4':
            return '慢病回访'
        else:
            return ''

class MV_RIS2HIS_ALL(BaseModel):

    __tablename__ = 'V_RIS2HIS_ALL'

    CBLKH = Column(VARCHAR(20), primary_key=True)        # 体检编号
    CNAME = Column(VARCHAR(20),nullable=False)
    CSEX = Column(VARCHAR(20),nullable=False)
    CAGE = Column(Integer, nullable=False)
    CBGZT = Column(VARCHAR(20), nullable=False)         # 报告状态
    CJCZT = Column(VARCHAR(20), nullable=False)         # 检查状态
    CBZ = Column(VARCHAR(50), nullable=False)

class MT_TJ_SMS_POST(BaseModel):

    __tablename__ = 'TJ_SMS_POST'

    tjbh = Column(String(16), primary_key=True)       # 体检编号
    sendtime = Column(DateTime, nullable=False)       # 发送时间
    context = Column(Text, nullable=False)            # 短信内容
    state = Column(String(20), nullable=False)        # 状态
    sender = Column(String(20), nullable=False)       # 发送者
    xm = Column(String(20), nullable=False)           # 姓名
    sjhm = Column(String(20), nullable=False)         # 手机号码
    xb = Column(String(20), nullable=False)           # 性别

    @property
    def to_dict(self):
        return {
            'tjbh':getattr(self, "tjbh", ''),
            'sendtime': str(getattr(self, "sendtime", ''))[0:19],
            'context':str2(getattr(self, "context", ''))
        }


def get_inspect_result_sql():
    return '''
     SELECT 
        SYSTYPE,CMODALITY,CBZ AS XMMC,CACCNO,CBLKH,CNAME,CSEX,CAGE,
        CBGZT,RIS_BG_CSHYSXM AS SHYS,RIS_BG_DSHSJ AS SHSJ,
        RIS_BG_DBGSJ AS BGSJ,RIS_BG_CBGYSXM AS BGYS,CJCZT,
        DCHECKDATE,DDJSJ,IID,IJCH,RIS_BG_CBGSJ_HL7 AS XMJG,RIS_BG_CBGZD AS XMZD,
        RIS_BG_CBGYS,RIS_BG_CSHYS,HISORDER_IID,CBRLX,CROOM
     FROM V_RIS2HIS_ALL WHERE CBLKH = '%s'
    '''