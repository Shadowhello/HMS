import pandas as pd

if __name__ =="__main__":
    # 检查所有结果导出

    if __name__ == "__main__":
        from utils.bmodel import *
        from utils.base import sql_init
        from utils.envir import set_env

        set_env()
        engine = create_engine('mssql+pymssql://bsuser:admin2389@10.8.200.201:1433/tjxt', encoding='utf8', echo=False)
        session = sessionmaker(bind=engine)()
        sql = sql_init('sql_inspect_result', {'key_dwbh': '14719'})
        #print(sqlparse.format(sql, reindent=True, keyword_case='upper', indent_width=4, output_format="python"))
        results = session.execute(sql).fetchall()
        datas =[]
        ryxx = {'tjbh': ''}
        cols = ['tjbh','xm','xb','nl','sjhm','sfzh','qdrq','dwmc','depart','zjys']
        for result in results:
            if ryxx['tjbh'] == result[0]:
                if str2(result[-2]) not in cols:
                    cols.append(str2(result[-2]))
                ryxx[str2(result[-2])] = str2(result[-1])
            else:
                # 先加入后清空
                if ryxx['tjbh']:
                    datas.append(ryxx)
                ryxx = {'tjbh': ''}
                ryxx['tjbh'] = result[0]
                ryxx['xm'] = str2(result[1])
                ryxx['xb'] = str2(result[2])
                ryxx['nl'] = result[3]
                ryxx['sjhm'] = result[4]
                ryxx['sfzh'] = result[5]
                ryxx['qdrq'] = result[6]
                ryxx['dwmc'] = str2(result[7])
                ryxx['depart'] = str2(result[8])
                ryxx['zjys'] = str2(result[9])


        filename = 'C:/Users/Administrator/Desktop/三门核电/2016三门核电检查结果.xlsx'
        df = pd.DataFrame(data=datas)
        df.to_excel(filename,sheet_name='2016三门核电检查结果', columns=cols, index=False)