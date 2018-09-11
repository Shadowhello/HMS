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

    @property
    def to_dict(self):
        return {
            "tjbh": getattr(self, "tjbh", ''),
            "xm": getattr(self, "xm", ''),
            "xb": getattr(self, "xb", ''),
            "nl": '%s 岁' % str(getattr(self, "nl", '')),
            "sfzh": getattr(self, "sfzh", ''),
            "sjhm": getattr(self, "sjhm", ''),
            "dwmc": getattr(self, "dwmc", ''),
            "ysje": str(getattr(self, "ysje", '')),
            "is_gxy": getattr(self, "is_gxy", ''),
            "is_gxz": getattr(self, "is_gxz", ''),
            "is_gxt": getattr(self, "is_gxt", ''),
            "is_gns": getattr(self, "is_gns", ''),
            "is_jzx": getattr(self, "is_jzx", ''),
            "glu": getattr(self, "glu", ''),
            "is_yc_glu": int(getattr(self, "is_yc_glu", '')),
            "glu2": getattr(self, "glu2", ''),
            "is_yc_glu2": int(getattr(self, "is_yc_glu2", '')),
            "hbalc": getattr(self, "hbalc", ''),
            "is_yc_hbalc": int(getattr(self, "is_yc_hbalc", '')),
            "ua": getattr(self, "ua", ''),
            "is_yc_ua": int(getattr(self, "is_yc_ua", '')),
            "tch": getattr(self, "tch", ''),
            "is_yc_tch": int(getattr(self, "is_yc_tch", '')),
            "tg": getattr(self, "tg", ''),
            "is_yc_tg": int(getattr(self, "is_yc_tg", '')),
            "hdl": getattr(self, "hdl", ''),
            "is_yc_hdl": int(getattr(self, "is_yc_hdl", '')),
            "ldl": getattr(self, "ldl", ''),
            "is_yc_ldl": int(getattr(self, "is_yc_ldl", '')),
            "hbp": getattr(self, "hbp", ''),
            "is_yc_hbp": int(getattr(self, "is_yc_hbp", '')),
            "lbp": getattr(self, "lbp", ''),
            "is_yc_lbp": int(getattr(self, "is_yc_lbp", ''))
        }

def get_mbgl_sql():
    return '''
    SELECT 
    tjbh,xm,xb,CAST(nl AS VARCHAR) AS nl,sfzh,sjhm,dwmc,CAST(ysje AS VARCHAR) AS ysje,is_gxy,is_gxz,is_gxt,is_gns,is_jzx,glu,is_yc_glu,glu2,is_yc_glu2,hbalc,is_yc_hbalc,ua,
    is_yc_ua,tch,is_yc_tch,tg,is_yc_tg,hdl,is_yc_hdl,ldl,is_yc_ldl,hbp,is_yc_hbp,lbp,is_yc_lbp
    FROM MB_YSKH WHERE 
    '''