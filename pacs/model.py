from utils.bmodel import *

class MV_RIS2HIS_ALL(BaseModel):

    __tablename__ = 'V_RIS2HIS_ALL'

    CBLKH = Column(VARCHAR(20), primary_key=True)        # 体检编号
    CNAME = Column(VARCHAR(20),nullable=False)
    CSEX = Column(VARCHAR(20),nullable=False)
    CAGE = Column(Integer, nullable=False)
    CBGZT = Column(VARCHAR(20), nullable=False)         # 报告状态
    CJCZT = Column(VARCHAR(20), nullable=False)         # 检查状态
    CBZ = Column(VARCHAR(50), nullable=False)

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