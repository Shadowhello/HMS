from .bmodel import *
import _mssql,pymssql


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
def get_pacs_session():
    # 设置编码，否则：
    # 1. Oracle 查询出来的中文是乱码
    # 2. 插入数据时有中文，会导致
    # UnicodeEncodeError: 'ascii' codec can't encode characters in position 1-7: ordinal not in range(128)
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    #create_engine('oracle://scott:tiger@127.0.0.1:1521/sidname')   #SID方式
    engine = create_engine('oracle+cx_oracle://RIS:RIS@RIS', encoding='utf8', echo=False)        # TNS 方式

    session = sessionmaker(bind=engine)

    return session()

def get_cxk_session():
    # 设置编码，否则：
    # 1. Oracle 查询出来的中文是乱码
    # 2. 插入数据时有中文，会导致
    # UnicodeEncodeError: 'ascii' codec can't encode characters in position 1-7: ordinal not in range(128)
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    #create_engine('oracle://scott:tiger@127.0.0.1:1521/sidname')   #SID方式
    engine = create_engine('oracle://TJ_CXK:TJ_CXK@10.7.200.101:1521/orcl', encoding='utf8', echo=False)        # TNS 方式

    session = sessionmaker(bind=engine)

    return session()

def get_pis_session(hostname='10.8.200.79',dbname='eWorldPIS',user='sa',passwd='eWorldPACS',port=1433,encoding='utf-8',echo=False):
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

def get_lis_session(hostname='10.8.200.231',dbname='digitlab',user='sa',passwd='abc@123',port=1433,encoding='utf-8',echo=False):
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