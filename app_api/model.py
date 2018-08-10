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