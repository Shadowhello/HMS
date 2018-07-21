# 检查所有结果导出

if __name__ =="__main__":
    from utils.bmodel import *
    from utils.base import sql_init
    from utils.envir import set_env
    set_env()
    engine = create_engine('mssql+pymssql://bsuser:admin2389@10.8.200.201:1433/tjxt', encoding='utf8', echo=False)
    session = sessionmaker(bind=engine)()
    sql = sql_init('sql_inspect_result',{'key_dwbh':'14719'})
    print(sql)
    #results = session.execute(sql).fetchall()