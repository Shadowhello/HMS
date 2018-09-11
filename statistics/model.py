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

# 体检人数
def get_qd_sql(start,end):
    return '''
        SELECT COUNT(*) AS RS FROM TJ_TJDJB WHERE  (del <> '1' or del is null) and QD='1' AND (QDRQ>='%s' AND QDRQ<'%s')
    '''%(start,end)

# 收单人数
def get_sd_sql(start,end):
    return '''
        SELECT COUNT(*) AS RS FROM TJ_TJDJB WHERE  (del <> '1' or del is null) and QD='1' AND (QDRQ>='%s' AND QDRQ<'%s') AND TJZT IN ('4','5','6','7','8')
    '''%(start,end)

# 推送总数
def get_ts_sql(start,end):
    return '''
        SELECT count(DISTINCT TJBH) as RS FROM WX_QRSD_TS WHERE QDRQ>='%s' AND QDRQ<'%s'
    '''%(start,end)

# 关注总数
def get_gz_sql(start,end):
    return '''
        SELECT count(*) as RS FROM PENAIRERECORD WHERE 
    
        to_char(PENAIRERECORD.TESTDATE,'YYYY-MM-DD')>='%s' AND 
        to_char(PENAIRERECORD.TESTDATE,'YYYY-MM-DD')<'%s'
    '''%(start,end)

# 填写总数
def get_tx_sql(start,end):
    return '''
            SELECT count(STATUS) as RS FROM PENAIRERECORD WHERE 
                STATUS = 1 AND
                to_char(PENAIRERECORD.TESTDATE,'YYYY-MM-DD')>='%s' AND 
                to_char(PENAIRERECORD.TESTDATE,'YYYY-MM-DD')<'%s'
        ''' %(start,end)

# 填写总数
def get_tx_sql2(start,end):
    return '''
            SELECT STATUS,count(STATUS) as RS FROM PENAIRERECORD WHERE 
                to_char(PENAIRERECORD.TESTDATE,'YYYY-MM-DD')>='%s' AND 
                to_char(PENAIRERECORD.TESTDATE,'YYYY-MM-DD')<'%s'
            GROUP BY STATUS
        ''' %(start,end)

# 获取微信关注总数
def get_myd_sum_sql(start,end):
    return '''
            SELECT 
            (CASE STATUS WHEN 1 THEN '收到已作答' WHEN 0 THEN '收到未作答' ELSE '' END) AS STATE,
            ANSWER_ID AS TJBH,NAME,
            to_char(TESTDATE,'YYYY-MM-DD') AS ZDSJ,PHONE AS SJHM,to_char(b.SCORE,'999') AS SCORE,b.SUGGESTION
            
            from (
                SELECT * FROM PENAIRERECORD WHERE 
                to_char(PENAIRERECORD.TESTDATE,'YYYY-MM-DD')>='%s' AND 
                to_char(PENAIRERECORD.TESTDATE,'YYYY-MM-DD')<'%s'
             )  a
        
            LEFT  JOIN
        
            (SELECT ANSID,
                    sum(CASE WHEN QUESTION_ID IN (1,2,3,4,5) THEN To_number(CONTENT)*4 ELSE 0 END ) AS SCORE,
                    -- MAX(CASE QUESTION_ID WHEN 1 THEN CONTENT ELSE '' END) AS 预约排期,
                    -- MAX(CASE QUESTION_ID WHEN 2 THEN CONTENT ELSE '' END) AS 体检流程,
                    -- MAX(CASE QUESTION_ID WHEN 3 THEN CONTENT ELSE '' END) AS 专业水平,
                    -- MAX(CASE QUESTION_ID WHEN 4 THEN CONTENT ELSE '' END) AS 医护服务,
                    -- MAX(CASE QUESTION_ID WHEN 5 THEN CONTENT ELSE '' END) AS 早餐服务,
                    MAX(CASE QUESTION_ID WHEN 6 THEN CONTENT ELSE '' END) AS SUGGESTION
                    FROM PENAIREANS WHERE ANSID IN (SELECT ANSWER_ID FROM PENAIRERECORD WHERE 
                    
                    to_char(TESTDATE,'YYYY-MM-DD')>='%s' AND  
                    
                    to_char(TESTDATE,'YYYY-MM-DD')<'%s'  AND STATUS=1

                    ) GROUP BY  ANSID 
            ) b
        
        ON a.ANSWER_ID=b.ANSID 
        
        ORDER BY STATUS DESC,b.SCORE DESC,TESTDATE
    ''' %(start,end,start,end)


# 获取微信填写率
def get_myd_tx_sql(start, end):
    return '''
            SELECT 
            (CASE STATUS WHEN 1 THEN '收到已作答' WHEN 0 THEN '收到未作答' ELSE '' END) AS STATE,
            ANSWER_ID AS TJBH,NAME,
            to_char(TESTDATE,'YYYY-MM-DD') AS ZDSJ,PHONE AS SJHM,
            b.yypq,b.tjlc,b.zysp,b.yhfw,b.zcfw,b.SUGGESTION

            from (
                SELECT * FROM PENAIRERECORD WHERE 
                STATUS = 1 AND 
                to_char(PENAIRERECORD.TESTDATE,'YYYY-MM-DD')>='%s' AND 
                to_char(PENAIRERECORD.TESTDATE,'YYYY-MM-DD')<'%s'

             )  a

            LEFT  JOIN

            (SELECT ANSID,
                    MAX(CASE QUESTION_ID WHEN 1 THEN CONTENT ELSE '' END) AS yypq,
                    MAX(CASE QUESTION_ID WHEN 2 THEN CONTENT ELSE '' END) AS tjlc,
                    MAX(CASE QUESTION_ID WHEN 3 THEN CONTENT ELSE '' END) AS zysp,
                    MAX(CASE QUESTION_ID WHEN 4 THEN CONTENT ELSE '' END) AS yhfw,
                    MAX(CASE QUESTION_ID WHEN 5 THEN CONTENT ELSE '' END) AS zcfw,
                    MAX(CASE QUESTION_ID WHEN 6 THEN CONTENT ELSE '' END) AS SUGGESTION

                    FROM PENAIREANS WHERE ANSID IN (SELECT ANSWER_ID FROM PENAIRERECORD WHERE 

                    to_char(TESTDATE,'YYYY-MM-DD')>='%s' AND  

                    to_char(TESTDATE,'YYYY-MM-DD')<'%s'   

                    AND STATUS=1

                    ) GROUP BY  ANSID 
            ) b

        ON a.ANSWER_ID=b.ANSID 

        ORDER BY STATUS DESC,TESTDATE
    ''' % (start, end, start, end)

# 获取微信好评率
def get_myd_hp_sql(start, end):
    return '''
            SELECT 
            (CASE STATUS WHEN 1 THEN '收到已作答' WHEN 0 THEN '收到未作答' ELSE '' END) AS STATE,
            ANSWER_ID AS TJBH,NAME,
            to_char(TESTDATE,'YYYY-MM-DD') AS ZDSJ,PHONE AS SJHM,to_char(b.SCORE,'999') AS SCORE

            from (

                SELECT * FROM PENAIRERECORD WHERE 
                STATUS = 1 AND 
                to_char(PENAIRERECORD.TESTDATE,'YYYY-MM-DD')>='%s' AND 
                to_char(PENAIRERECORD.TESTDATE,'YYYY-MM-DD')<'%s'

             )  a

            LEFT  JOIN

            (SELECT ANSID,
                    sum(CASE WHEN QUESTION_ID IN (1,2,3,4,5) THEN To_number(CONTENT)*4 ELSE 0 END ) AS SCORE
            FROM PENAIREANS WHERE ANSID IN (SELECT ANSWER_ID FROM PENAIRERECORD 
            WHERE to_char(TESTDATE,'YYYY-MM-DD')>='%s' 
                AND to_char(TESTDATE,'YYYY-MM-DD')<'%s'   
                AND STATUS=1
                    ) GROUP BY  ANSID 
            ) b

        ON a.ANSWER_ID=b.ANSID 

        ORDER BY STATUS DESC,b.SCORE DESC,TESTDATE
    ''' % (start, end, start, end)

def get_myd_score_sql(start, end):
    return '''
         SELECT AVG(SCORE) AS SCORE_AVG  FROM    
						(SELECT ANSID,
                    sum(CASE WHEN QUESTION_ID IN (1,2,3,4,5) THEN To_number(CONTENT)*4 ELSE 0 END ) AS SCORE
                    FROM PENAIREANS WHERE ANSID IN (SELECT ANSWER_ID FROM PENAIRERECORD 
										
										WHERE STATUS=1 AND
                    
                    to_char(TESTDATE,'YYYY-MM-DD')>='%s' AND  
                    
                    to_char(TESTDATE,'YYYY-MM-DD')<'%s'  

                    ) GROUP BY  ANSID ) a
    ''' % (start, end)

# 获取报告项目超期
def get_report_item_cq_sql(xmlx,start,end):
    return '''
    SELECT TJBH,XMBH,XMMC,
        (CASE XMLX 
            WHEN '1' THEN '功能项目'
            WHEN '2' THEN '检验项目'
            WHEN '3' THEN '检查项目'
            ELSE '' END
        ) AS LXMC,
        substring(convert(char,QDRQ,120),1,10) AS QDRQ,
        substring(convert(char,JCRQ,120),1,10) AS JCRQ,
        XMZQ,DATEDIFF(day,QDRQ,JCRQ) AS SJZQ,(XMZQ-DATEDIFF(day,QDRQ,JCRQ)) AS XMCQ  
    FROM
    (SELECT 
        a.TJBH,b.QDRQ,a.XMBH,a.XMMC,
        (CASE WHEN a.shrq IS NULL THEN a.JCRQ ELSE a.shrq END) AS JCRQ,
        (SELECT BGCJZQ FROM TJ_XMDM WHERE XMBH = a.XMBH) AS XMZQ,
        (SELECT TJ_XMLB.XMLX FROM TJ_XMLB INNER JOIN TJ_XMDM ON TJ_XMLB.LBBM = TJ_XMDM.LBBM AND TJ_XMDM.XMBH =a.XMBH) AS XMLX
        FROM 
        TJ_TJJLMXB a INNER JOIN TJ_TJDJB b
        ON a.TJBH= b.TJBH AND (del <> '1' or del is null) AND QD='1' AND SUMOVER='1' AND QDRQ>='%s' AND QDRQ<'%s' 
        AND SFZH='1' AND qzjs IS NULL 
    ) AS tmp
    WHERE XMLX='%s' AND XMZQ-DATEDIFF(day,QDRQ,JCRQ)<0
    ORDER BY XMBH,QDRQ,(XMZQ-DATEDIFF(day,QDRQ,JCRQ))
    ''' %(start,end,xmlx)

def get_report_item_sql(start,end):
    return '''
    SELECT XMLX,COUNT(*) AS RS,
        ( CASE 
            WHEN XMZQ-DATEDIFF(day,QDRQ,JCRQ)>=0 THEN 0
            ELSE 1 END
        ) AS SFCQ
 
    FROM
    (SELECT 
        b.QDRQ,a.XMBH,
        (CASE WHEN a.shrq IS NULL THEN a.JCRQ ELSE a.shrq END) AS JCRQ,
        (SELECT BGCJZQ FROM TJ_XMDM WHERE XMBH = a.XMBH) AS XMZQ,
        (SELECT TJ_XMLB.XMLX FROM TJ_XMLB INNER JOIN TJ_XMDM ON TJ_XMLB.LBBM = TJ_XMDM.LBBM AND TJ_XMDM.XMBH =a.XMBH) AS XMLX
        FROM 
        TJ_TJJLMXB a INNER JOIN TJ_TJDJB b
        ON a.TJBH= b.TJBH AND (del <> '1' or del is null) AND QD='1' AND SUMOVER='1' AND QDRQ>='%s' AND QDRQ<'%s' 
        AND SFZH='1' AND qzjs IS NULL 
    ) AS tmp
    
    GROUP BY XMLX,(CASE WHEN XMZQ-DATEDIFF(day,QDRQ,JCRQ)>=0 THEN 0 ELSE 1 END)

    '''%(start,end)