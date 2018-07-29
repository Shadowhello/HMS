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
    '''