from .bmodel import *

def get_tjxt_session(hostname,dbname,user,passwd,port=1433,encoding='utf-8',echo=False):
    '''
    :param hostname: 主机
    :param dbname: 数据库
    :param user: 用户
    :param passwd: 密码
    :param port: 端口
    :return:
    '''
    engine_str = 'mssql+pymssql://%s:%s@%s:%s/%s' %(user,passwd,hostname,port,dbname)
    engine = create_engine(engine_str,echo=False)
    session = sessionmaker(bind=engine)
    return session()



# oracle
#engine = create_engine('oracle://scott:tiger@127.0.0.1:1521/sidname')
#engine = create_engine('oracle+cx_oracle://scott:tiger@tnsname')