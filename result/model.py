from utils.bmodel import *



class MT_TJ_XMJG(BaseModel):

    __tablename__ = 'TJ_XMJG'

    ID = Column(Integer, primary_key=True)
    xmbh = Column(String(12), primary_key=True)
    jg = Column(Text, nullable=False)
    ms = Column(String(200), nullable=False)
    sfxj = Column(CHAR(1), nullable=False)
    xssx = Column(Integer, nullable=False)