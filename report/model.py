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
                (CASE WHEN OrderState>=3030 THEN '已审核' ELSE '未审核' END ) AS BGZT,
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