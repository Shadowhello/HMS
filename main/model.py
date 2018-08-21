from utils.bmodel import *

#用户登录表
class MT_TJ_USER(BaseModel):

    __tablename__ = 'SS_OPERATE_USER'

    xtsb = Column(Integer, primary_key=True)
    yhdm = Column(VARCHAR(20),primary_key=True)
    yhzm = Column(VARCHAR(20),nullable=False)
    yhmc = Column(VARCHAR(20), nullable=False)
    yhkl = Column(VARCHAR(50), nullable=False)
    yhzt = Column(Integer, nullable=False)



