from utils.bmodel import *

# 慢病记录表 宽表

class MT_MB_YSKH(BaseModel):

    __tablename__ = 'MB_YSKH'

    mbid = Column(Integer, primary_key=True, autoincrement=True)
    tjbh = Column(String(16),nullable=True,unique=True)
    xm = Column(String(10),nullable=True)
    xb = Column(String(5),nullable=False)
    nl = Column(Integer, nullable=False)
    sjhm = Column(String(20),nullable=False)
    sfzh = Column(String(20), nullable=False)
    addr = Column(String(100),nullable=False)
    dwbh = Column(String(5), nullable=False)
    dwmc = Column(String(200), nullable=False)
    ysje = Column(FLOAT, nullable=False)
    djrq = Column(String(10), nullable=False)
    qdrq = Column(String(10), nullable=False)
    tjrq = Column(String(10), nullable=False)
    zjrq = Column(String(10), nullable=False)
    shrq = Column(String(10), nullable=False)
    zjys = Column(String(10), nullable=False)
    shys = Column(String(10), nullable=False)
    is_gxy = Column(CHAR(1), nullable=True,default='0')
    is_gxz = Column(CHAR(1), nullable=True,default='0')
    is_gns = Column(CHAR(1), nullable=True,default='0')
    is_gxt = Column(CHAR(1), nullable=True,default='0')
    is_jzx = Column(CHAR(1), nullable=True,default='0')
    glu = Column(FLOAT, nullable=False)         # 血糖
    is_yc_glu = Column(CHAR(1), nullable=True, default='0')
    glu2 = Column(FLOAT, nullable=False)        # 二小时血糖
    is_yc_glu2 = Column(CHAR(1), nullable=True, default='0')
    hbalc = Column(FLOAT, nullable=False)       # 糖化血红蛋白
    is_yc_hbalc = Column(CHAR(1), nullable=True, default='0')
    ua = Column(FLOAT, nullable=False)          # 尿酸
    is_yc_ua = Column(CHAR(1), nullable=True, default='0')
    tch = Column(FLOAT, nullable=False)         # 总胆固醇
    is_yc_tch = Column(CHAR(1), nullable=True, default='0')
    tg = Column(FLOAT, nullable=False)          # 甘油三酯
    is_yc_tg = Column(CHAR(1), nullable=True, default='0')
    hdl = Column(FLOAT, nullable=False)         # 高密度脂蛋白
    is_yc_hdl = Column(CHAR(1), nullable=True, default='0')
    ldl = Column(FLOAT, nullable=False)         # 低密度脂蛋白
    is_yc_ldl = Column(CHAR(1), nullable=True, default='0')
    hbp = Column(FLOAT, nullable=False)         # 高血压
    is_yc_hbp = Column(CHAR(1), nullable=True, default='0')
    lbp = Column(FLOAT, nullable=False)         # 低血压
    is_yc_lbp = Column(CHAR(1), nullable=True, default='0')
    jzxcs = Column(Text, nullable=False)        # 甲状腺彩超
    is_hf = Column(CHAR(1), nullable=True, default='0') # 是否回访

