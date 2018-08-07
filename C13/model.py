from utils.bmodel import *
from utils.base import str2


def get_nocheck_sql():

    return '''
            SELECT  
            a.TJBH,
            b.XM,
            (CASE b.XB WHEN '1' THEN '男' WHEN '2'  THEN '女' ELSE '' END) AS XB,
            a.NL,
            c.XMMC,
            (CASE a.tjqy 
                WHEN '1'  THEN '明州1楼' 
                WHEN '2'  THEN '明州2楼' 
                WHEN '3'  THEN '明州3楼' 
                ELSE '江东' END 
            ) AS TJQY
            FROM TJ_TJDJB a INNER JOIN TJ_TJDAB b ON a.DABH=b.DABH AND  (a.del <> '1' or a.del is null) and a.QD='1' AND a.QDRQ>=substring(convert(char,getdate(),120),1,10) 
            INNER JOIN TJ_TJJLMXB c ON a.TJBH = c.TJBH AND c.XMBH='5001'
            AND a.TJBH NOT IN (SELECT TJBH FROM TJ_CZJLB WHERE MXBH='5001' AND CZSJ>=substring(convert(char,getdate(),120),1,10) )
    '''

def get_nocheck2_sql(up_time):

    return '''
            SELECT
            a.TJBH,
            b.XM,
            (CASE b.XB WHEN '1' THEN '男' WHEN '2'  THEN '女' ELSE '' END) AS XB,
            a.NL,
            c.XMMC,
            (CASE a.tjqy 
                WHEN '1'  THEN '明州1楼' 
                WHEN '2'  THEN '明州2楼' 
                WHEN '3'  THEN '明州3楼' 
                ELSE '江东' END 
            ) AS TJQY
            FROM TJ_TJDJB a 
				INNER JOIN TJ_TJDAB b ON a.DABH=b.DABH 
					AND  (a.del <> '1' or a.del is null) and a.QD='1' 
					AND a.QDRQ>='%s'  AND  a.QDRQ<substring(convert(char,dateadd(day,1,getdate()),120),1,10)
				INNER JOIN TJ_TJJLMXB c ON a.TJBH = c.TJBH AND c.XMBH='5001'
    ''' %up_time

# 吃药丸
def get_checking1_sql():

    return '''
            SELECT  
            a.TJBH,
            b.XM,
            (CASE b.XB WHEN '1' THEN '男' WHEN '2'  THEN '女' ELSE '' END) AS XB,
            a.NL,
            c.XMMC,
            (CASE a.tjqy 
                WHEN '1'  THEN '明州1楼' 
                WHEN '2'  THEN '明州2楼' 
                WHEN '3'  THEN '明州3楼' 
                ELSE '江东' END 
            ) AS TJQY
            FROM TJ_TJDJB a INNER JOIN TJ_TJDAB b ON a.DABH=b.DABH AND  (a.del <> '1' or a.del is null) and a.QD='1' AND a.QDRQ>=substring(convert(char,getdate(),120),1,10) 
            INNER JOIN TJ_TJJLMXB c ON a.TJBH = c.TJBH AND c.XMBH='5001'
            AND a.TJBH IN (SELECT TJBH FROM TJ_CZJLB WHERE MXBH='5001' AND SJFS='2' AND CZSJ>=substring(convert(char,getdate(),120),1,10) )
    '''
# 待吹气
def get_checking2_sql():

    return '''
            SELECT  
            a.TJBH,
			d.JJXM,
            b.XM,
            (CASE b.XB WHEN '1' THEN '男' WHEN '2'  THEN '女' ELSE '' END) AS XB,
            a.NL,
            c.XMMC,
            (CASE a.tjqy 
                WHEN '1'  THEN '明州1楼' 
                WHEN '2'  THEN '明州2楼' 
                WHEN '3'  THEN '明州3楼' 
                ELSE '江东' END 
            ) AS TJQY
            FROM TJ_TJDJB a INNER JOIN TJ_TJDAB b ON a.DABH=b.DABH AND  (a.del <> '1' or a.del is null) and a.QD='1' AND a.QDRQ>=substring(convert(char,getdate(),120),1,10) 
            INNER JOIN TJ_TJJLMXB c ON a.TJBH = c.TJBH AND c.XMBH='5001'
			INNER JOIN TJ_CZJLB d ON a.TJBH=d.TJBH AND d.SJFS='3';
    '''

# 完成
def get_checked_sql():

    return '''
            SELECT  
            a.TJBH,
			d.JJXM,
            b.XM,
            (CASE b.XB WHEN '1' THEN '男' WHEN '2'  THEN '女' ELSE '' END) AS XB,
            a.NL,
            c.XMMC,
            (CASE a.tjqy 
                WHEN '1'  THEN '明州1楼' 
                WHEN '2'  THEN '明州2楼' 
                WHEN '3'  THEN '明州3楼' 
                ELSE '江东' END 
            ) AS TJQY
            FROM TJ_TJDJB a INNER JOIN TJ_TJDAB b ON a.DABH=b.DABH AND  (a.del <> '1' or a.del is null) and a.QD='1' AND a.QDRQ>=substring(convert(char,getdate(),120),1,10) 
            INNER JOIN TJ_TJJLMXB c ON a.TJBH = c.TJBH AND c.XMBH='5001'
			INNER JOIN TJ_CZJLB d ON a.TJBH=d.TJBH AND d.SJFS='4';
    '''