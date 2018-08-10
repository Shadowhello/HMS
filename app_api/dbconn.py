from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import os

BaseModel = declarative_base()

# 获取外网数据库 连接
def get_oracle_session(conn_str):
    # 设置编码，否则：
    # 1. Oracle 查询出来的中文是乱码
    # 2. 插入数据时有中文，会导致
    # UnicodeEncodeError: 'ascii' codec can't encode characters in position 1-7: ordinal not in range(128)
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    #create_engine('oracle://scott:tiger@127.0.0.1:1521/sidname')   #SID方式
    engine = create_engine(conn_str, encoding='utf8', echo=False)        # TNS 方式

    session = sessionmaker(bind=engine)

    return session()

class MT_TJ_PDFRUL(BaseModel):

    __tablename__ = 'TJ_PDFRUL'

    ID = Column(VARCHAR(36), primary_key=True)
    TJBH = Column(VARCHAR(100), nullable=False)
    PDFURL = Column(VARCHAR(200),nullable=False)
    CREATETIME =Column(TIMESTAMP,nullable=False)