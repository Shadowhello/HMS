from utils.bmodel import *

#用户表
class M_TJ_USER(BaseModel):

    __tablename__ = 'SS_OPERATE_USER'

    xtsb = Column(Integer, primary_key=True)
    yhdm = Column(VARCHAR(20),primary_key=True)
    yhzm = Column(VARCHAR(20),nullable=False)
    yhmc = Column(VARCHAR(20), nullable=False)
    yhkl = Column(VARCHAR(50), nullable=False)
    yhzt = Column(Integer, nullable=False)

#用户表
class M_TJ_YGQSKS(BaseModel):

    __tablename__ = 'TJ_YGQSKS'

    xh = Column(Integer, primary_key=True)
    yggh = Column(VARCHAR(10),primary_key=True)
    ksbm = Column(VARCHAR(10), primary_key=True)
    xssx = Column(Integer, nullable=False)