from utils.bmodel import *

# 主表 信息只记录最后一次，过程记录是 TJ_CZJLB
# 流程
# 正流程：体检登记 -> 体检预约 -> 体检签到(检查) -> 体检收单 -> (体检追踪) -> 总检 -> 审核 -> 审阅 -> 打印 -> 整理 -> 领取(下载)  取消登记(体检)0
# 正状态：  1           2           3              4            5           6      7      8
    # 正子流程：体检签到(检查) -> 体检收单 -> (体检追踪)
    # 签到未收单：即未咨询顾客项目拒检情况、报告领取方式、满意度调查等事宜；  增加收单、查看电子导检单功能
    #
# 反流程1：已审阅 发现报告问题：取消审阅 -> 取消审核 -> 取消总检
# 反流程2：已审阅 发现报告问题：取消审阅 -> 取消审核 -> 取消总检 -> 报告追踪
# 反流程3：未审阅 发现报告问题：取消审核 -> 取消总检
# 反流程4：未审阅 发现报告问题：取消审核 -> 取消总检 -> 报告追踪
#
class MT_TJ_BGGL(BaseModel):

    __tablename__ = 'TJ_BGGL'

    tjbh = Column(String(16), primary_key=True)     # 体检编号
    bgzt = Column(CHAR(1), nullable=True)           # 报告状态 默认：待追踪(0) 追踪完成，待总检审核(1) 审核完成待审阅(2) 审阅完成待打印(3)
    qdrq = Column(DateTime, nullable=True)          # 签到日期
    qdgh = Column(String(16), nullable=False)       # 签到工号
    qdxm = Column(String(16), nullable=False)       # 签到姓名
    sdrq = Column(DateTime, nullable=False)         # 收单日期
    sdgh = Column(String(16), nullable=False)       # 收单工号
    sdxm = Column(String(16), nullable=False)       # 收单姓名
    zzrq = Column(DateTime, nullable=False, default=datetime.now)         # 追踪日期
    zzgh = Column(String(16), nullable=False)       # 追踪工号
    zzxm = Column(String(16), nullable=False)       # 追踪姓名
    zzbz = Column(Text, nullable=False)             # 追踪备注    记录电话等沟通信息，强制接收等信息
    zjrq = Column(DateTime, nullable=False)         # 总检日期
    zjgh = Column(String(16), nullable=False)       # 总检工号
    zjxm = Column(String(16), nullable=False)       # 总检姓名
    zjbz = Column(Text, nullable=False)             # 总检备注
    shrq = Column(DateTime, nullable=False)         # 审核日期
    shgh = Column(String(16), nullable=False)       # 审核工号
    shxm = Column(String(16), nullable=False)       # 审核姓名
    shbz = Column(Text, nullable=False)             # 审核备注    记录退回原因
    syrq = Column(DateTime, nullable=False)         # 审阅日期
    sygh = Column(String(16), nullable=False)       # 审阅工号
    syxm = Column(String(16), nullable=False)       # 审阅姓名
    sybz = Column(Text, nullable=False)             # 审阅备注    记录退回原因
    dyrq = Column(DateTime, nullable=False)         # 打印日期
    dygh = Column(String(16), nullable=False)       # 打印工号
    dyxm = Column(String(16), nullable=False)       # 打印姓名
    dyfs = Column(CHAR(1), nullable=True, default='0')          # 打印方式 默认 0  自助打印 1
    dycs = Column(Integer, nullable=True, default=0)            # 打印次数 默认 0
    zlrq = Column(DateTime, nullable=False)         # 整理日期
    zlgh = Column(String(16), nullable=False)       # 整理工号
    zlxm = Column(String(16), nullable=False)       # 整理姓名
    zlhm = Column(String(16), nullable=False)       # 整理货号
    lqrq = Column(DateTime, nullable=False)         # 领取日期
    lqgh = Column(String(16), nullable=False)       # 领取工号
    lqxm = Column(String(16), nullable=False)       # 领取姓名
    lqbz = Column(Text, nullable=False)             # 领取备注    记录领取信息
    bgym = Column(Integer, nullable=True, default=0) # 报告页码，默认0页

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
                    (select MC from TJ_DWDMB where DWBH=TJ_TJDJB.DWBH) AS DWMC
                    ,substring(convert(char,TJ_TJDJB.QDRQ,120),1,10) AS QDRQ
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

def get_quick_search_sql(where_str):
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
                
                AND %s

                AND (TJ_TJDJB.del <> '1' or TJ_TJDJB.del is null) 
            )
             ,T2 AS (
                        SELECT T1.TJBH,XMMC FROM TJ_TJJLMXB INNER JOIN T1 ON TJ_TJJLMXB.TJBH = T1.TJBH AND TJ_TJJLMXB.SFZH='1' AND jsbz<>'1'
                    )

    SELECT T1.*,d.wjxm FROM T1 INNER JOIN 
    (
        SELECT T2.TJBH,(SELECT XMMC+' ; ' FROM T2 AS C WHERE C.TJBH=T2.TJBH  FOR XML PATH('')  ) AS wjxm from T2 GROUP BY T2.TJBH 
    ) AS d

    ON T1.TJBH=d.TJBH 

    ''' %where_str

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


# CREATE TABLE TJ_BGGL(
#     [TJBH] varchar(16) COLLATE Chinese_PRC_CI_AS NOT NULL ,
#     [BGZT] CHAR(1) COLLATE Chinese_PRC_CI_AS NOT NULL ,
#     [QDRQ] datetime NULL ,
#     [QDGH] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [QDXM] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [SDRQ] datetime NULL ,
#     [SDGH] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [SDXM] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [ZZRQ] datetime NULL ,
#     [ZZGH] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [ZZXM] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [ZZBZ] TEXT COLLATE Chinese_PRC_CI_AS NULL ,
#     [ZJRQ] datetime NULL ,
#     [ZJGH] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [ZJXM] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [ZJBZ] TEXT COLLATE Chinese_PRC_CI_AS NULL ,
#     [SHRQ] datetime  NULL ,
#     [SHGH] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [SHXM] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [SHBZ] TEXT COLLATE Chinese_PRC_CI_AS NULL ,
#     [SYRQ] datetime NULL ,
#     [SYGH] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [SYXM] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [SYBZ] TEXT COLLATE Chinese_PRC_CI_AS NULL ,
#     [DYRQ] datetime NULL ,
#     [DYGH] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [DYXM] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [DYFS] CHAR(1) COLLATE Chinese_PRC_CI_AS NOT NULL ,
#     [DYCS] INTEGER NOT NULL ,
#     [ZLRQ] datetime NULL ,
#     [ZLGH] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [ZLXM] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [ZLHM] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [LQRQ] datetime NULL ,
#     [LQGH] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [LQXM] varchar(16) COLLATE Chinese_PRC_CI_AS NULL ,
#     [LQBZ] TEXT COLLATE Chinese_PRC_CI_AS NULL ,
#     [BGYM] INTEGER NOT NULL ,
#     PRIMARY KEY (TJBH)
# );

