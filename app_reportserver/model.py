from utils.bmodel import *

#医生排班
class MT_TJ_YSPB(BaseModel):

    __tablename__ = 'TJ_YSPB'

    PBID = Column(Numeric(18), primary_key=True)
    PBXQ = Column(Numeric(1),nullable=False)
    PBSXW = Column(Numeric(1),nullable=False)
    PBKSSJ = Column(VARCHAR(6), nullable=False)
    PBJSSJ = Column(VARCHAR(6), nullable=False)
    YSXX = Column(VARCHAR(60), nullable=False)
    ZFBZ = Column(Numeric(1), nullable=False)
    ZHXGR = Column(VARCHAR(30), nullable=False)
    ZHXGSJ = Column(Date, nullable=False)

#疾病情况
class MT_TJ_JBQK(BaseModel):

    __tablename__ = 'TJ_JBQK'

    jlxh = Column(Numeric(), primary_key=True)
    tjbh = Column(String(16),nullable=False)
    jbbm = Column(String(20),nullable=False)
    jbmc = Column(String(100),nullable=False)
    ksbm = Column(String(12),nullable=True)
    sfjb = Column(CHAR(1), nullable=True)
    jynr = Column(String(2000), nullable=True)
    jblx = Column(CHAR(2), nullable=True)
    jbpx = Column(Integer, nullable=True)

# 项目记录
class MV_TJJLMXB(BaseModel):

    __tablename__ = 'V_TJJLMXB'

    tjbh = Column(String(16), primary_key=True)
    xmbh = Column(String(12), primary_key=True)
    zhbh = Column(String(12), nullable=True)
    xmmc = Column(String(60), nullable=False)
    jg = Column(Text, nullable=False)
    xmdw = Column(String(20), nullable=False)
    ckfw = Column(String(100), nullable=False)
    ycbz = Column(CHAR(1), nullable=False)
    ycts = Column(String(20), nullable=False)
    sfzh = Column(CHAR(1), nullable=False)
    kslx = Column(CHAR(1), nullable=False)
    xmlx = Column(CHAR(1), nullable=False)
    xssx = Column(Integer, nullable=False)
    ksbm = Column(CHAR(6), nullable=False)
    jcrq = Column(DateTime, nullable=False)
    jcys = Column(String(20), nullable=False)
    zd = Column(Text, nullable=False)
    shys = Column(String(20), nullable=False)
    shrq = Column(DateTime, nullable=False)


    def zhxm(self):
        pass

    def mxxm(self):

        # 特殊处理项目
        if getattr(self, "xmbh", '')=='190016':
            jg = str2(getattr(self, "jg", '')).replace('\r\n','<br />')
            zd = str2(getattr(self, "zd", ''))
        elif getattr(self, "xmbh", '')=='700036':
            zd = str2(getattr(self, "jg", ''))
            jg = '检查已做，详见心电图报告。'
        else:
            zd = str2(getattr(self, "zd", ''))
            jg = str2(getattr(self, "jg", ''))

        return {
                "xmbh": getattr(self, "xmbh", ''),
                "xmmc": str2(getattr(self, "xmmc", '')),
                "jg": jg,
                "ckfw": str2(getattr(self, "ckfw", '')),
                "xmdw": str2(getattr(self, "xmdw", '')),
                "ycbz": getattr(self, "ycbz", ''),
                "ycts": str2(getattr(self, "ycts", '')),
                "kslx": getattr(self, "kslx", ''),
                "ksbm": getattr(self, "ksbm", ''),
                "zd": zd
                }



# 保健处方标题
class MT_TJ_BJCF_TITLE(BaseModel):

    __tablename__ = 'tj_bjcf_title'

    ID = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=True)
    stitle = Column(String(500), nullable=True)
    ltitle1 = Column(String(500), nullable=True)
    body1 = Column(Text, nullable=True)
    ltitle2 = Column(String(500), nullable=True)
    body2 = Column(Text, nullable=True)
    inuser = Column(CHAR(1),nullable=True)

    def to_dict(self):
        return {
                "title": str2(getattr(self, "title", '')),
                "stitle": str2(getattr(self, "stitle", '')),
                "ltitle1": str2(getattr(self, "ltitle1", '')),
                "body1": str2(getattr(self, "body1", '')),
                "ltitle2": str2(getattr(self, "ltitle2", '')),
                "body2": str2(getattr(self, "body2", ''))
        }

def get_bjcf_detail(tjbh):
    return '''
            SELECT
                a.title AS bjcf_title,
                a.body AS bjcf_body
            FROM
                tj_bjcf_body a
            WHERE
                a.id IN (
                    SELECT DISTINCT (b.bodyid) FROM tj_bjcf_rel b
                    WHERE
                        b.illid IN (
                            SELECT DISTINCT (c.bh) FROM
                                tj_suggestion c,
                                tj_jbqk d
                            WHERE
                                c.jbbh = d.jbbm
                            AND d.tjbh = '%s'
                        )
                )
            ORDER BY a.id
    ''' %tjbh