from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# MT 表示 表 MV 表示视图
class MT_TJ_FILE_ACTIVE(db.Model):

    __tablename__ = "TJ_FILE_ACTIVE"

    rid = db.Column(db.BigInteger, primary_key=True)
    tjbh = db.Column(db.String(16))
    dwbh = db.Column(db.CHAR(5))
    ryear = db.Column(db.CHAR(4))
    rmonth = db.Column(db.CHAR(7))
    rday = db.Column(db.CHAR(10))
    localfile = db.Column(db.String(250))
    ftpfile = db.Column(db.String(100))
    filename = db.Column(db.String(20))
    filetype = db.Column(db.CHAR(2))
    filetypename = db.Column(db.String(20))
    filesize = db.Column(db.Float)
    filemtime = db.Column(db.BigInteger)
    createtime = db.Column(db.DateTime)


# 自动更新表
class MT_TJ_UPDATE(db.Model):

    __tablename__ = "TJ_UPDATE"

    upid = db.Column(db.BigInteger, primary_key=True)
    version = db.Column(db.Float)
    ufile = db.Column(db.Text)
    describe = db.Column(db.Text)
    uptime = db.Column(db.DateTime)

class MT_TJ_BGGL(db.Model):

    __tablename__ = 'TJ_BGGL'

    tjbh = db.Column(db.String(16), primary_key=True)                         # 体检编号
    bgzt = db.Column(db.CHAR(1), nullable=True)                               # 报告状态 默认：追踪(0) 审核完成待审阅(1) 审阅完成待打印(2) 打印完成待整理(3)
    djrq = db.Column(db.DateTime, nullable=True)                              # 登记日期
    djgh = db.Column(db.String(16), nullable=False)                           # 登记工号
    djxm = db.Column(db.String(16), nullable=False)                           # 登记姓名
    qdrq = db.Column(db.DateTime, nullable=True)                              # 签到日期
    qdgh = db.Column(db.String(16), nullable=False)                           # 签到工号
    qdxm = db.Column(db.String(16), nullable=False)                           # 签到姓名
    sdrq = db.Column(db.DateTime, nullable=False)                             # 收单日期
    sdgh = db.Column(db.String(16), nullable=False)                           # 收单工号
    sdxm = db.Column(db.String(16), nullable=False)                           # 收单姓名
    zzrq = db.Column(db.DateTime, nullable=False,)                            # 追踪日期
    zzgh = db.Column(db.String(16), nullable=False)                           # 追踪工号
    zzxm = db.Column(db.String(16), nullable=False)                           # 追踪姓名
    zzbz = db.Column(db.Text, nullable=False)                                 # 追踪备注    记录电话等沟通信息，强制接收等信息
    zjrq = db.Column(db.DateTime, nullable=False)                             # 总检日期
    zjgh = db.Column(db.String(16), nullable=False)                           # 总检工号
    zjxm = db.Column(db.String(16), nullable=False)                           # 总检姓名
    zjbz = db.Column(db.Text, nullable=False)                                 # 总检备注
    shrq = db.Column(db.DateTime, nullable=False)                             # 审核日期
    shgh = db.Column(db.String(16), nullable=False)                           # 审核工号
    shxm = db.Column(db.String(16), nullable=False)                           # 审核姓名
    shbz = db.Column(db.Text, nullable=False)                                 # 审核备注    记录退回原因
    syrq = db.Column(db.DateTime, nullable=False)                             # 审阅日期
    sygh = db.Column(db.String(16), nullable=False)                           # 审阅工号
    syxm = db.Column(db.String(16), nullable=False)                           # 审阅姓名
    sybz = db.Column(db.Text, nullable=False)                                 # 审阅备注    记录退回原因
    dyrq = db.Column(db.DateTime, nullable=False)                             # 打印日期
    dygh = db.Column(db.String(16), nullable=False)                           # 打印工号
    dyxm = db.Column(db.String(16), nullable=False)                           # 打印姓名
    dyfs = db.Column(db.CHAR(1), nullable=True, default='0')                  # 打印方式 默认 0  自助打印 1
    dycs = db.Column(db.Integer, nullable=True, default=0)                    # 打印次数 默认 0
    zlrq = db.Column(db.DateTime, nullable=False)                             # 整理日期
    zlgh = db.Column(db.String(16), nullable=False)                           # 整理工号
    zlxm = db.Column(db.String(16), nullable=False)                           # 整理姓名
    zlhm = db.Column(db.String(16), nullable=False)                           # 整理货号
    lqrq = db.Column(db.DateTime, nullable=False)                             # 领取日期
    lqgh = db.Column(db.String(16), nullable=False)                           # 领取工号
    lqxm = db.Column(db.String(16), nullable=False)                           # 领取姓名
    lqbz = db.Column(db.Text, nullable=False)                                 # 领取备注    记录领取信息
    bgym = db.Column(db.Integer, nullable=True, default=0)                    # 报告页码，默认0页
    bglj = db.Column(db.String(250), nullable=False)                          # 报告路径 只存储对应PDF、HTML根路径
    bgms = db.Column(db.CHAR(1), nullable=False,default='0')                  # 报告模式 默认HTML 1 PDF