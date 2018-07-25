from utils.bmodel import *

def get_report_track_sql(tstart,tend):
    return '''
    WITH T1 AS (
                SELECT 
                    (CASE TJZT
                        WHEN '0' THEN '取消登记'
                        WHEN '1' THEN '已登记'
                        WHEN '2' THEN '已预约'
                        WHEN '3' THEN '已签到'
                        WHEN '4' THEN '已收单'
                        WHEN '5' THEN '已追踪'
                        WHEN '6' THEN '已总检'
                        WHEN '7' THEN '已审核'
                        WHEN '8' THEN '已审阅'
                        ELSE '' END 
                    ) AS TJZT,
                    (CASE 
                        WHEN zhaogong='0' AND TJLX='1' THEN '普通'
                        WHEN zhaogong='1' AND TJLX='1' THEN '招工'
                        WHEN zhaogong='1' AND TJLX='2' THEN '从业'
                        WHEN zhaogong='1' AND TJLX IN ('3','4','5','6') THEN '职业病'
                        WHEN zhaogong='2' THEN '贵宾'
                        WHEN zhaogong='3' THEN '重点'
                        WHEN zhaogong='4' THEN '投诉'
                        ELSE '' END
                    ) AS TJLX,
                    (CASE tjqy
                        WHEN '1' THEN '明州1楼'
                        WHEN '2' THEN '明州2楼'
                        WHEN '3' THEN '明州3楼'
                        WHEN '4' THEN '江东'
                        WHEN '5' THEN '车管所'
                        WHEN '6' THEN '外出'
                        WHEN '7' THEN '其他'
                        WHEN '8' THEN '明州'
                        ELSE '' END
                    ) AS TJQY,
                    TJ_TJDJB.TJBH,XM,(CASE XB WHEN '1' THEN '男' ELSE '女' END) AS XB,
                    NL,TJ_TJDAB.SFZH,TJ_TJDAB.SJHM,
                    (select MC from TJ_DWDMB where DWBH=TJ_TJDJB.DWBH) AS DWMC,
                    DEPART,substring(convert(char,TJ_TJDJB.QDRQ,120),1,10) AS QDRQ
                FROM TJ_TJDJB INNER JOIN TJ_TJDAB ON TJ_TJDJB.DABH = TJ_TJDAB.DABH 

                AND (TJ_TJDJB.del <> '1' or TJ_TJDJB.del is null) 

                AND TJ_TJDJB.QD='1' AND SUMOVER = '0'

                AND (TJ_TJDJB.QDRQ>='%s' and TJ_TJDJB.QDRQ<'%s')
            )
             ,T2 AS (
                        SELECT T1.TJBH,XMMC FROM TJ_TJJLMXB INNER JOIN T1 ON TJ_TJJLMXB.TJBH = T1.TJBH AND TJ_TJJLMXB.SFZH='1' AND jsbz<>'1'
                    )

    SELECT T1.*,d.wjxm FROM T1 INNER JOIN 
    (
        SELECT T2.TJBH,(SELECT XMMC+' ; ' FROM T2 AS C WHERE C.TJBH=T2.TJBH  FOR XML PATH('')  ) AS wjxm from T2 GROUP BY T2.TJBH 
    ) AS d

    ON T1.TJBH=d.TJBH 

    ''' %(tstart,tend)

def get_quick_search_sql(tjbh):
    return '''
    WITH T1 AS (
                SELECT 
                    (CASE TJZT
                        WHEN '0' THEN '取消登记'
                        WHEN '1' THEN '已登记'
                        WHEN '2' THEN '已预约'
                        WHEN '3' THEN '已签到'
                        WHEN '4' THEN '已收单'
                        WHEN '5' THEN '已追踪'
                        WHEN '6' THEN '已总检'
                        WHEN '7' THEN '已审核'
                        WHEN '8' THEN '已审阅'
                        ELSE '' END 
                    ) AS TJZT,
                    (CASE 
                        WHEN zhaogong='0' AND TJLX='1' THEN '普通'
                        WHEN zhaogong='1' AND TJLX='1' THEN '招工'
                        WHEN zhaogong='1' AND TJLX='2' THEN '从业'
                        WHEN zhaogong='1' AND TJLX IN ('3','4','5','6') THEN '职业病'
                        WHEN zhaogong='2' THEN '贵宾'
                        WHEN zhaogong='3' THEN '重点'
                        WHEN zhaogong='4' THEN '投诉'
                        ELSE '' END
                    ) AS TJLX,
                    (CASE tjqy
                        WHEN '1' THEN '明州1楼'
                        WHEN '2' THEN '明州2楼'
                        WHEN '3' THEN '明州3楼'
                        WHEN '4' THEN '江东'
                        WHEN '5' THEN '车管所'
                        WHEN '6' THEN '外出'
                        WHEN '7' THEN '其他'
                        WHEN '8' THEN '明州'
                        ELSE '' END
                    ) AS TJQY,
                    TJ_TJDJB.TJBH,XM,(CASE XB WHEN '1' THEN '男' ELSE '女' END) AS XB,
                    NL,TJ_TJDAB.SFZH,TJ_TJDAB.SJHM,
                    (select MC from TJ_DWDMB where DWBH=TJ_TJDJB.DWBH) AS DWMC,
                    DEPART,substring(convert(char,TJ_TJDJB.QDRQ,120),1,10) AS QDRQ
                FROM TJ_TJDJB INNER JOIN TJ_TJDAB ON TJ_TJDJB.DABH = TJ_TJDAB.DABH 

                AND (TJ_TJDJB.del <> '1' or TJ_TJDJB.del is null) 

                AND TJ_TJDJB.QD='1' AND SUMOVER = '0'
                
                AND TJ_TJDJB.TJBH = '%s'

            )
             ,T2 AS (
                        SELECT T1.TJBH,XMMC FROM TJ_TJJLMXB INNER JOIN T1 ON TJ_TJJLMXB.TJBH = T1.TJBH AND TJ_TJJLMXB.SFZH='1' AND jsbz<>'1'
                    )

    SELECT T1.*,d.wjxm FROM T1 INNER JOIN 
    (
        SELECT T2.TJBH,(SELECT XMMC+' ; ' FROM T2 AS C WHERE C.TJBH=T2.TJBH  FOR XML PATH('')  ) AS wjxm from T2 GROUP BY T2.TJBH 
    ) AS d

    ON T1.TJBH=d.TJBH 

    ''' %tjbh

def get_pis_sql(tjbh):
    return '''
            SELECT  
                (CASE 
                    WHEN OrderState=1020 THEN '未报告'
                    WHEN OrderState=3010 THEN '未审核'
                    WHEN OrderState=3030 THEN '已审核'
                    ELSE '未审核' END 
                ) AS BGZT,
                ExamitemName,
                PName AS Name,
                (CAST(PAge AS VARCHAR)+AgeUnit) AS AGE,
                ServiceDoc,
                Doccol,
                ReportDoc,
                ReportDate,
                AuditDoc,
                AuditDate,
                TJSJ,
                TJZD,
                filename,
                ModalityNO,  
                MedrecNO,     
                HIS_KeyNO
            FROM V_PS_Report_TJ WHERE  LEFT(HIS_keyCode,9)='%s' ;
    ''' %tjbh

def has_pis_sql(tjbh):
    return '''
    SELECT 1 FROM TJ_TJJLMXB WHERE TJBH ='%s' AND KSBM='0026' AND SFZH='1';
    ''' %tjbh

def get_pacs_sql(tjbh):
    return '''
     SELECT 
        CBGZT,SYSTYPE,CMODALITY,CBZ AS XMMC,CNAME,CSEX,CAGE,
				RIS_BG_CBGYSXM AS BGYS,RIS_BG_DBGSJ AS BGSJ,
        RIS_BG_CSHYSXM AS SHYS,RIS_BG_DSHSJ AS SHSJ
				,RIS_BG_CBGSJ_HL7 AS XMJG,RIS_BG_CBGZD AS XMZD,CJCZT,
        DDJSJ,DCHECKDATE,RIS_BG_CBGYS AS BGYSGH,
				RIS_BG_CSHYS AS SHYSGH,CACCNO,CBLKH,HISORDER_IID
     FROM V_RIS2HIS_ALL WHERE CBLKH = '%s'
    ''' %tjbh

def has_pacs_sql(tjbh):
    return '''
    SELECT 1 FROM TJ_TJJLMXB WHERE TJBH ='%s' AND KSBM in ('0020','0022','0023','0024','0027','0019','') AND SFZH='1';
    ''' %tjbh

# 获取体检端条码明细：项目
def get_pes_sql(tjbh):
    return '''
        WITH 
        T1 AS (
            SELECT TJBH,XMMC,TMBH1 AS TMBH,jsbz,shys,shrq,JCRQ,JCYS
            FROM TJ_TJJLMXB WHERE TJBH='%s' AND SFZH='1' 
            AND (
                       (XMBH IN (SELECT XMBH FROM TJ_XMDM WHERE LBBM IN (SELECT LBBM FROM TJ_XMLB WHERE XMLX='2' )) AND TMBH1 IS NOT NULL) 
                    OR (XMBH='1931')
                 )
        ),
        T2 AS (
            SELECT T1.jsbz,T1.TJBH,T1.TMBH,(SELECT XMMC+'  ' FROM T1 AS C WHERE C.TJBH = T1.TJBH AND C.TMBH = T1.TMBH  FOR XML PATH('')  ) AS XMHZ,
						T1.shys,T1.shrq,T1.JCRQ,T1.JCYS from T1 
            GROUP BY T1.TJBH,T1.TMBH,T1.jsbz,T1.shys,T1.shrq,T1.JCRQ,T1.JCYS
        )
        SELECT T2.jsbz,T2.TMBH,T2.XMHZ,
            (select ygxm from tj_ygdm where yggh=T2.JCYS ) AS jcys,T2.JCRQ,
            (select ygxm from tj_ygdm where yggh=T2.shys ) AS shys,T2.shrq,
            T2.TJBH 
        FROM T2 WHERE TJBH='%s' AND T2.TMBH IS NOT NULL;
    ''' %(tjbh,tjbh)

def get_lis_sql(tjbh):
    return '''
        SELECT (TJBH+tmh) AS TJTM,XMXH,XMMC,XMJG,GDBJ,CKFW,XMDW FROM VI_TJ_RESULT WHERE TJBH='%s';
    ''' %tjbh

def get_lis_sql2(tjbh):
    return '''
    SELECT TJBH,tmh AS TMBH,BGRQ,SHYS,JYYS,JYRQ FROM VI_TJ_RESULT WHERE TJBH='%s' GROUP BY TJBH,tmh,BGRQ,SHYS,JYYS,JYRQ;
    ''' %tjbh

