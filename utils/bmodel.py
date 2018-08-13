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

    @property
    def item_state(self):
        if getattr(self, "qzjs", '') == '1':
            return '已拒检'
        else:
            if getattr(self, "jsbz", '') == '1':
                return '已小结'
            else:
                if getattr(self, "zxpb", '') == '0':
                    return '核实'
                elif getattr(self, "zxpb", '') == '1':
                    return '已回写'
                elif getattr(self, "zxpb", '') == '2':
                    return '已接收'
                elif getattr(self, "zxpb", '') == '3':
                    return '已检查'
                elif getattr(self, "zxpb", '') == '4':
                    return '已抽血'
                elif getattr(self, "zxpb", '') == '5':
                    return '已留样'
                else:
                    return '未知'

    @property
    def item_result(self):
        return {
            'xmmc':str2(getattr(self, "xmmc", '')),
            'xmbh': getattr(self, "xmbh", ''),
            'state': self.item_state,
            'ksbm':getattr(self, "ksbm", ''),
            'btn_dy':'',                                    # 打印
            'btn_jj':'',                                    # 拒检
            'btn_hs':''                                     # 核实
        }

    # @property
    # def ksbm(self):
    #     return getattr(self, "ksbm", ''),

class MT_TJ_PACS_PIC(BaseModel):

    __tablename__ = 'TJ_PACS_PIC'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    tjbh = Column(String(16),nullable=True)
    ksbm = Column(CHAR(6),nullable=True)
    picpath = Column(String(200),nullable=False)
    picname = Column(String(100),nullable=False)
    zhbh = Column(String(16), nullable=False)
    flag = Column(CHAR(1), nullable=False)
    path = Column(String(100), nullable=False)
    pk = Column(String(30), nullable=False)
    ftp_bz = Column(CHAR(1), nullable=False)

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
    jjxm = Column(VARCHAR(20), nullable=False)                              # 交接护士
    jjsj = Column(DateTime, nullable=False)                                 # 交接时间
    jsxm = Column(VARCHAR(20), nullable=False)                              # 签收人员
    jssj = Column(DateTime, nullable=False)                                 # 签收时间
    sjfs = Column(VARCHAR(20), nullable=False)                              # 送检人员


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
            'jjxm': str2(getattr(self, "jjxm")),
            'jjsj': self.jjsj_value,
            'jsxm': str2(getattr(self, "jsxm")),
            'jssj': self.jssj_value,
            'sjfs': str2(getattr(self, "sjfs")),
            'ck':'查看'
        }

    @property
    def jjsj_value(self):
        if getattr(self, "jjsj"):
            return str(getattr(self, "jjsj"))[0:19]
        else:
            return ''

    @property
    def jssj_value(self):
        if getattr(self, "jssj"):
            return str(getattr(self, "jssj"))[0:19]
        else:
            return ''

    @property
    def detail(self):
        return {
            'tjbh': getattr(self, "tjbh"),
            'mxbh': getattr(self, "mxbh"),
            'czxm': str2(getattr(self, "czxm")),
            'czqy': str2(getattr(self, "czqy")),
            'czsj': str(getattr(self, "czsj"))[0:19],
            'jlnr': str2(getattr(self, "jlnr"))
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

class MV_RYXX(BaseModel):

    __tablename__ = 'V_RYXX'

    tjbh = Column(VARCHAR(20), primary_key=True)
    xm = Column(VARCHAR(20),nullable=False)
    xb = Column(VARCHAR(20),nullable=False)
    nl = Column(Integer, nullable=False)
    sjhm = Column(VARCHAR(20), nullable=False)
    sfzh = Column(VARCHAR(20), nullable=False)
    depart = Column(VARCHAR(50), nullable=False)
    dwmc = Column(VARCHAR(100), nullable=False)
    djrq = Column(VARCHAR(20), nullable=False)
    qdrq = Column(VARCHAR(20), nullable=False)

    @property
    def to_dict(self):
        return {
            'tjbh':getattr(self, "tjbh"),
            'xm': str2(getattr(self, "xm")),
            'xb': str2(getattr(self, "xb")),
            'nl': '%s 岁' %str(getattr(self, "nl")),
            'sfzh': getattr(self, "sfzh"),
            'sjhm': getattr(self, "sjhm"),
            'depart': str2(getattr(self, "depart")),
            'dwmc': str2(getattr(self, "dwmc")),
            'djrq': getattr(self, "djrq"),
            'qdrq': getattr(self, "qdrq")
        }

class MT_TJ_PHOTO(BaseModel):

    __tablename__ = 'TJ_PHOTO'

    tjbh = Column(VARCHAR(16), primary_key=True)
    picture = Column(BLOB, nullable=False)


class MT_TJ_KSDM(BaseModel):

    __tablename__ = 'TJ_KSDM'

    ksbm = Column(CHAR(6), primary_key=True)
    ksmc = Column(VARCHAR(40), nullable=False)

class MT_TJ_XMDM(BaseModel):

    __tablename__ = 'TJ_XMDM'

    xmbh = Column(VARCHAR(10), primary_key=True)
    xmmc = Column(VARCHAR(40), nullable=False)
    sfzh = Column(CHAR(1), nullable=False)