from utils.bmodel import *

def get_report_detail_sql(sfzh):
    return '''
        SELECT 
            a.TJBH,
            b.XM,
            (CASE b.XB WHEN '1' THEN '男' WHEN '2' THEN '女' ELSE '' END) AS XB,
            a.NL,
            b.SFZH,
            b.SJHM,
            substring(convert(char,a.QDRQ,120),1,10) AS QDRQ,
            substring(convert(char,a.SHRQ,120),1,10) AS SHRQ
        FROM TJ_TJDJB a INNER JOIN TJ_TJDAB b ON a.DABH = b.DABH 
            AND (del <> '1' or del is null) 
            AND QD='1' 
            AND SUMOVER ='1' 
            AND b.sfzh='%s' 
        ORDER BY QDRQ DESC
    '''%sfzh