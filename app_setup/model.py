from utils.bmodel import *

class MT_Permissions(BaseModel):

    __tablename__ = 'sys_permissions'

    pid = Column(INTEGER, primary_key=True, nullable=False)
    pname = Column(VARCHAR(20), nullable=False)
    pcontent = Column(Text, nullable=False)
    mtime = Column(DateTime, nullable=False)
    muser = Column(VARCHAR(20), nullable=False)