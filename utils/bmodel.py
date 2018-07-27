from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from utils.base import str2
from datetime import datetime
import os
BaseModel = declarative_base()


'''
模型类名：
1）MT_ 表示表     其中 M表示model  T表示table
2）MV_ 表示视图   其中 M表示model  V表示view
'''

# 公共模型
class MT_TJ_TJJLMXB(BaseModel):

    __tablename__ = 'TJ_TJJLMXB'

    tjbh = Column(String(16), primary_key=True)      #体检编号 自动生成
    xmbh = Column(String(12), primary_key=True)      # 体检编号 自动生成
    zhbh = Column(String(12), nullable=False)        # 组合编号
    xmmc = Column(String(60), nullable=True)
    jg = Column(Text, nullable=True)
    xmdw = Column(String(20), nullable=True)
    ckfw = Column(String(100), nullable=True)
    ycbz = Column(CHAR(1), nullable=True)
    ycts = Column(String(20), nullable=True)
    sfzh = Column(CHAR(1), nullable=True)
    xssx = Column(Integer(), nullable=True)
    ksbm = Column(CHAR(6), nullable=True)
    jcrq = Column(DateTime, nullable=True)
    jcys = Column(String(20), nullable=True)
    zhsx = Column(Integer(), nullable=True)
    zd = Column(Text, nullable=True)
    zxpb = Column(CHAR(1), nullable=True)
    jsbz = Column(CHAR(1), nullable=True)
    qzjs = Column(CHAR(1), nullable=True)
    shrq = Column(DateTime, nullable=True)
    shys = Column(String(20), nullable=True)
    tmxh = Column(String(20), nullable=True)
    tmbh1 = Column(String(20), nullable=False)

class MT_TJ_DW(BaseModel):

    __tablename__ = 'TJ_DWDMB'

    dwbh = Column(String(30), primary_key=True)
    mc = Column(String(100),nullable=True)
    pyjm = Column(String(50),nullable=True)

    @property
    def to_dict_bh(self):
        return {
            getattr(self, "dwbh", ''):str2(getattr(self, "mc", ''))
        }

    @property
    def to_dict_py(self):
        return {
            getattr(self, "pyjm", ''):str2(getattr(self, "mc", ''))
        }


# 公共模型
class MT_TJ_FILE_ACTIVE(BaseModel):

    __tablename__ = 'TJ_FILE_ACTIVE'

    tjbh = Column(String(16), primary_key=True)      #体检编号 自动生成
    dwbh = Column(CHAR(5), nullable=True)
    ryear = Column(CHAR(4), nullable=True)
    rmonth = Column(CHAR(7), nullable=True)
    rday = Column(CHAR(10), nullable=True)
    localfile = Column(String(250), nullable=True)
    ftpfile = Column(String(100), nullable=False)
    filename = Column(String(20), nullable=False)
    filetypename = Column(String(20), nullable=False)
    filesize = Column(Float, nullable=False)
    filemtime = Column(BIGINT, nullable=False)
    createtime = Column(DateTime, nullable=True)

class MT_TJ_CZJLB(BaseModel):

    __tablename__ = 'TJ_CZJLB'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    jllx = Column(CHAR(4), nullable=True)
    jlmc = Column(VARCHAR(30), nullable=True)
    tjbh = Column(VARCHAR(16), nullable=False)
    mxbh = Column(VARCHAR(20), nullable=True)
    czgh = Column(VARCHAR(20), nullable=True)
    czxm = Column(VARCHAR(20), nullable=True)
    czsj = Column(DateTime, nullable=True, default=datetime.now)
    czqy = Column(VARCHAR(2), nullable=True)
    jlnr = Column(Text, nullable=False)
    bz = Column(Text, nullable=False)

    @property
    def to_dict(self):

        return {
            'zt': '√',
            'jllx': str2(getattr(self, "jlmc")),
            'tjbh': getattr(self, "tjbh"),
            'tmbh': getattr(self, "mxbh"),
            'czxm': str2(getattr(self, "czxm")),
            'czqy': str2(getattr(self, "czqy")),
            'czsj': str(getattr(self, "czsj"))[0:19],
            'jlnr': str2(getattr(self, "jlnr")),
            'ck':'查看'
        }

# 设备表
class MT_TJ_EQUIP(BaseModel):

    __tablename__ = 'TJ_EQUIP'

    tjbh = Column(String(16), primary_key=True)  #体检编号
    equip_type = Column(CHAR(1), primary_key=True)  # 设备类型
    equip_name = Column(String(16), nullable=True)
    create_time = Column(DateTime, nullable=False)
    modify_time = Column(DateTime, nullable=False)
    patient = Column(String(20), nullable=False)
    file_path = Column(String(50), nullable=False)
    operator = Column(String(20), nullable=False)
    operate_time = Column(DateTime, nullable=False)
    equip_jg1 = Column(String(250), nullable=False)
    equip_jg2 = Column(String(50), nullable=False)
    xmbh = Column(String(12), nullable=False)
    hostname = Column(String(50), nullable=False)
    hostip = Column(String(25), nullable=False)
    operator2 = Column(String(20), nullable=False)
    operate_area = Column(String(50), nullable=False)

# 心电图
class MT_DCP_files(BaseModel):

    __tablename__ = 'DCP_files'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    cusn = Column(String(32), nullable=False)                       #体检编号
    department = Column(String(16), nullable=False)
    filename = Column(String(128), nullable=False)
    filecontent = Column(BLOB, nullable=False)
    uploadtime = Column(DateTime, nullable=False)
    flag = Column(CHAR(1), nullable=True)