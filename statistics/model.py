from utils.bmodel import *


def get_nurse_sum_sql(start,end):
    return '''
    WITH T1 AS (
    SELECT CZGH,CZXM,JLLX,COUNT(*) AS RC,(SELECT JSGS FROM TJ_CZJLWHB WHERE CZBH = TJ_CZJLB.JLLX) AS JXXS
    FROM TJ_CZJLB 
    WHERE (CZSJ>='%s' AND CZSJ<'%s') 
        AND JLLX IN (SELECT CZBH FROM TJ_CZJLWHB WHERE YXBJ = 1)  
        GROUP BY CZGH,CZXM,JLLX 
    )
    SELECT CZGH,CZXM,SUM(T1.RC*JXXS) AS JXJJ,0 AS GWGZ,'' AS GZZH FROM T1 GROUP BY CZGH,CZXM ORDER BY SUM(T1.RC*JXXS) DESC ;
    ''' %(start,end)

def get_nurse_group_sql(start,end,yggh):
    return '''
    SELECT JLLX,JLMC,(SELECT JSGS FROM TJ_CZJLWHB WHERE CZBH = TJ_CZJLB.JLLX) as JXXS,COUNT(*) AS JXSL,COUNT(*)*(SELECT JSGS FROM TJ_CZJLWHB WHERE CZBH = TJ_CZJLB.JLLX) AS JXXJ 
    FROM TJ_CZJLB 
    WHERE (CZSJ>='%s' AND CZSJ<'%s') 
        AND CZGH = '%s'
        AND JLLX IN (SELECT CZBH FROM TJ_CZJLWHB WHERE YXBJ = 1) 
        GROUP BY JLLX,JLMC 
        ORDER BY COUNT(*) DESC
    ''' %(start,end,yggh)

def get_nurse_detail_sql(start,end,yggh,jllx):
    return '''
    SELECT TJBH,MXBH,CZSJ,CZQY,JLMC FROM TJ_CZJLB WHERE CZSJ>='%s' AND CZSJ<'%s'  AND CZGH='%s' AND JLLX='%s' 
    ''' %(start,end,yggh,jllx)