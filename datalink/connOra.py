from datalink.model import *
import os

if __name__=="__main__":
    # 设置编码，否则：
    # 1. Oracle 查询出来的中文是乱码
    # 2. 插入数据时有中文，会导致
    # UnicodeEncodeError: 'ascii' codec can't encode characters in position 1-7: ordinal not in range(128)
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    #create_engine('oracle://scott:tiger@127.0.0.1:1521/sidname')   #SID方式
    engine = create_engine('oracle+cx_oracle://RIS:RIS@RIS', encoding='utf8', echo=False)        # TNS 方式

    session = sessionmaker(bind=engine)()
    sql = 'SELECT * FROM ICNRIS_HISORDER WHERE ROWNUM<10'
    results = session.execute(sql).fetchall()
    for result in results:
        print(result)