from utils.bmodel import *
from string import Template
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

    tjbh = Column(String(16), primary_key=True)                         # 体检编号
    bgzt = Column(CHAR(1), nullable=True)                               # 报告状态 默认：追踪(0) 审核完成待审阅(1) 审阅完成待打印(2) 打印完成待整理(3) 4 整理  5 领取
    djrq = Column(DateTime, nullable=True)                              # 登记日期
    djgh = Column(String(16), nullable=False)                           # 登记工号
    djxm = Column(String(16), nullable=False)                           # 登记姓名
    qdrq = Column(DateTime, nullable=True)                              # 签到日期
    qdgh = Column(String(16), nullable=False)                           # 签到工号
    qdxm = Column(String(16), nullable=False)                           # 签到姓名
    sdrq = Column(DateTime, nullable=False)                             # 收单日期
    sdgh = Column(String(16), nullable=False)                           # 收单工号
    sdxm = Column(String(16), nullable=False)                           # 收单姓名
    zzrq = Column(DateTime, nullable=False,)                            # 追踪日期
    zzgh = Column(String(16), nullable=False)                           # 追踪工号
    zzxm = Column(String(16), nullable=False)                           # 追踪姓名
    zzbz = Column(Text, nullable=False)                                 # 追踪备注    记录电话等沟通信息，强制接收等信息
    zjrq = Column(DateTime, nullable=False)                             # 总检日期
    zjgh = Column(String(16), nullable=False)                           # 总检工号
    zjxm = Column(String(16), nullable=False)                           # 总检姓名
    zjbz = Column(Text, nullable=False)                                 # 总检备注
    shrq = Column(DateTime, nullable=False)                             # 审核日期
    shgh = Column(String(16), nullable=False)                           # 审核工号
    shxm = Column(String(16), nullable=False)                           # 审核姓名
    shbz = Column(Text, nullable=False)                                 # 审核备注    记录退回原因
    syrq = Column(DateTime, nullable=False)                             # 审阅日期
    sygh = Column(String(16), nullable=False)                           # 审阅工号
    syxm = Column(String(16), nullable=False)                           # 审阅姓名
    sybz = Column(Text, nullable=False)                                 # 审阅备注    记录退回原因
    sysc = Column(Integer, nullable=False, default=0)                   # 当次审阅时长 默认 0
    dyrq = Column(DateTime, nullable=False)                             # 打印日期
    dygh = Column(String(16), nullable=False)                           # 打印工号
    dyxm = Column(String(16), nullable=False)                           # 打印姓名
    dyfs = Column(CHAR(1), nullable=False)                              # 打印方式 默认 0 租赁打印  1 本地打印  2 自助打印
    dycs = Column(Integer, nullable=True, default=0)                    # 打印次数 默认 0
    zlrq = Column(DateTime, nullable=False)                             # 整理日期
    zlgh = Column(String(16), nullable=False)                           # 整理工号
    zlxm = Column(String(16), nullable=False)                           # 整理姓名
    zlhm = Column(String(16), nullable=False)                           # 整理货号
    lqrq = Column(DateTime, nullable=False)                             # 领取日期
    lqgh = Column(String(16), nullable=False)                           # 领取工号
    lqxm = Column(String(16), nullable=False)                           # 领取姓名
    lqfs = Column(String(16), nullable=False)                           # 领取方式
    lqbz = Column(Text, nullable=False)                                 # 领取备注    记录领取信息
    bgym = Column(Integer, nullable=True, default=0)                    # 报告页码，默认0页
    bglj = Column(String(250), nullable=False)                          # 报告路径 只存储对应PDF、HTML根路径
    bgms = Column(CHAR(1), nullable=False,default='0')                  # 报告模式 默认HTML 1 PDF
    last_item_done = Column(DateTime, nullable=False)                   # 最后一个项目完成时间
    jpdyrq = Column(DateTime, nullable=False)                           # 胶片打印日期
    jpdygh = Column(String(16), nullable=False)                         # 胶片打印工号
    jpdyxm = Column(String(16), nullable=False)                         # 胶片打印姓名
    jpsl = Column(String(16), nullable=False)                           # 胶片数量
    jpjjjl = Column(String(250), nullable=False)                        # 胶片交接记录

def get_report_track_sql(tstart,tend):
    sql= '''
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

                AND (TJ_TJDJB.QDRQ>= '$tstart' and TJ_TJDJB.QDRQ< '$tend')
            )
             ,T2 AS (
                        SELECT T1.TJBH,XMMC,(SELECT BGCJZQ FROM TJ_XMDM WHERE XMBH = TJ_TJJLMXB.XMBH) AS XMZQ 
                        FROM TJ_TJJLMXB INNER JOIN T1 ON TJ_TJJLMXB.TJBH = T1.TJBH AND TJ_TJJLMXB.SFZH='1' AND jsbz<>'1'
                    )

    SELECT d.XMZQ,(d.XMZQ-DATEDIFF(DAY, T1.QDRQ, GETDATE())) AS zzjd,(CASE WHEN TJ_CZJLB.CZXM IS NOT NULL THEN '追踪中' ELSE '' END) AS zzzt,TJ_CZJLB.CZXM AS lqry,T1.*,d.wjxm FROM T1 

	LEFT  JOIN TJ_CZJLB ON T1.TJBH = TJ_CZJLB.TJBH AND TJ_CZJLB.JLLX='0030' AND CZSJ>= '$tstart'
    INNER JOIN 
    (
        SELECT T2.TJBH,MAX(T2.XMZQ) AS XMZQ,(SELECT XMMC+' ; ' FROM T2 AS C WHERE C.TJBH=T2.TJBH  FOR XML PATH('')  ) AS wjxm from T2 GROUP BY T2.TJBH 
    ) AS d

    ON T1.TJBH=d.TJBH 
    
    '''

    return Template(sql).safe_substitute({'tstart':tstart,'tend':tend})

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
                        SELECT T1.TJBH,XMMC,(SELECT BGCJZQ FROM TJ_XMDM WHERE XMBH = TJ_TJJLMXB.XMBH) AS XMZQ  
                        FROM TJ_TJJLMXB INNER JOIN T1 ON TJ_TJJLMXB.TJBH = T1.TJBH AND TJ_TJJLMXB.SFZH='1' AND jsbz<>'1'
                    )

    SELECT d.XMZQ,(d.XMZQ-DATEDIFF(DAY, T1.QDRQ, GETDATE())) AS zzjd, (CASE WHEN TJ_CZJLB.CZXM IS NOT NULL THEN '追踪中' ELSE '' END) AS zzzt,TJ_CZJLB.CZXM AS lqry,T1.*,d.wjxm FROM T1 

	LEFT  JOIN TJ_CZJLB ON T1.TJBH = TJ_CZJLB.TJBH AND TJ_CZJLB.JLLX='0030'
    INNER JOIN 
    (
        SELECT T2.TJBH,MAX(T2.XMZQ) AS XMZQ,(SELECT XMMC+' ; ' FROM T2 AS C WHERE C.TJBH=T2.TJBH  FOR XML PATH('')  ) AS wjxm from T2 GROUP BY T2.TJBH 
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

def get_equip_sql():
    return '''
    
    '''
# 根据签到日期检索 历史的
def get_report_print_sql(t_start,t_end):
    return '''
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
                    c.BGZT,
                    (CASE WHEN c.DYRQ IS NOT NULL THEN 1 WHEN c.DYRQ IS NULL AND a.dybj='1' THEN 1 ELSE 0 END) AS dyzt,
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
                    A.TJBH,
                    B.XM,
                    (CASE XB WHEN '1' THEN '男' ELSE '女' END) AS XB,
                    A.NL,
                    B.SFZH,
                    B.SJHM,
                    substring(convert(char,a.QDRQ,120),1,10) as QDRQ,
                    substring(convert(char,(CASE WHEN c.DYRQ IS NULL THEN a.BGRQ ELSE c.DYRQ END ),120),1,10) AS DYRQ,
                    (CASE WHEN c.DYXM IS NULL THEN (select ygxm from tj_ygdm where yggh=a.CPAINTER ) ELSE c.DYXM END) AS DYXM,
                    (CASE WHEN c.DYCS IS NULL AND dybj='1' THEN 1 WHEN c.DYCS IS NULL AND (dybj='0' OR dybj IS NULL) THEN 0 ELSE c.DYCS END) AS DYCS,
                    (CASE WHEN c.DYFS IS NULL AND dybj='1' THEN '报告室' WHEN c.DYCS IS NULL AND (dybj='0' OR dybj IS NULL) THEN '' ELSE c.DYFS END) AS DYFS,
                    (select MC from TJ_DWDMB where DWBH=a.DWBH) AS DWMC
                FROM TJ_TJDJB a INNER JOIN TJ_TJDAB b ON a.DABH=b.DABH AND (a.del <> '1' or a.del is null) and a.QD='1' AND SUMOVER='1' and (a.QDRQ>='%s' and a.QDRQ<'%s')
                LEFT JOIN TJ_BGGL c ON a.TJBH=c.TJBH 
            ''' %(t_start,t_end)

# 根据审阅日期检索
def get_report_print2_sql():
    return '''
                SELECT
                    (CASE TJ_TJDJB.TJZT
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
                    (CASE TJ_BGGL.BGZT
                            WHEN '0' THEN '追踪中'
                            WHEN '1' THEN '已审核'
                            WHEN '2' THEN '已审阅'
                            WHEN '3' THEN '已打印'
                            WHEN '4' THEN '已整理'
                            WHEN '5' THEN '已领取'
                            ELSE '' END 
                    ) AS BGZT,
                    (CASE WHEN TJ_BGGL.DYRQ IS NOT NULL THEN 1 WHEN TJ_BGGL.DYRQ IS NULL AND TJ_TJDJB.dybj='1' THEN 1 ELSE 0 END) AS dyzt,
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
                    TJ_TJDJB.TJBH,
                    TJ_TJDAB.XM,
                    (CASE XB WHEN '1' THEN '男' ELSE '女' END) AS XB,
                    TJ_TJDJB.NL,
                    TJ_TJDAB.SFZH,
                    TJ_TJDAB.SJHM,
                    substring(convert(char,TJ_TJDJB.QDRQ,120),1,10) as QDRQ,
                    substring(convert(char,(CASE WHEN TJ_BGGL.DYRQ IS NULL THEN TJ_TJDJB.BGRQ ELSE TJ_BGGL.DYRQ END ),120),1,10) AS DYRQ,
                    (CASE 
                        WHEN TJ_BGGL.DYXM IS NULL THEN (select ygxm from tj_ygdm where yggh=TJ_TJDJB.CPAINTER ) 
                        ELSE TJ_BGGL.DYXM END
                    ) AS DYXM,
                    (CASE 
                        WHEN TJ_BGGL.DYCS IS NULL AND dybj='1' THEN '1' 
                        WHEN TJ_BGGL.DYCS IS NULL AND (dybj='0' OR dybj IS NULL) THEN '' 
                        WHEN TJ_BGGL.DYCS = 0 THEN ''
                        ELSE CAST(TJ_BGGL.DYCS AS VARCHAR) END
                    ) AS DYCS,
                    (CASE 
                        WHEN TJ_BGGL.DYFS IS NULL AND dybj='1' THEN '租赁打印' 
                        WHEN TJ_BGGL.DYCS IS NULL AND (dybj='0' OR dybj IS NULL) THEN '' 
                        WHEN TJ_BGGL.DYCS = 0 THEN '租赁打印'
                        WHEN TJ_BGGL.DYCS = 1 THEN '本地打印'
                        WHEN TJ_BGGL.DYCS = 2 THEN '自助打印'
                        ELSE '' END
                    ) AS DYFS,
                    TJ_BGGL.ZLXM,
                    TJ_BGGL.ZLRQ,
                    TJ_BGGL.ZLHM,
                    TJ_BGGL.LQXM,
                    TJ_BGGL.LQRQ,
                    TJ_BGGL.LQFS,
                    '' AS JPDY,
                    TJ_TJDJB.DWBH,
                    (select MC from TJ_DWDMB where DWBH=TJ_TJDJB.DWBH) AS DWMC
                FROM 
                TJ_BGGL INNER JOIN TJ_TJDJB ON TJ_TJDJB.TJBH=TJ_BGGL.TJBH  
                    AND (TJ_TJDJB.del <> '1' or TJ_TJDJB.del is null) 
                    AND TJ_TJDJB.QD='1' 
                    AND TJ_TJDJB.SUMOVER='1' 
        '''

# 根据审阅日期检索
def get_report_review_sql(t_start,t_end):
    return '''
            SELECT
                (CASE C.BGZT
                        WHEN '0' THEN '待追踪'
                        WHEN '1' THEN '已审核'
                        WHEN '2' THEN '已审阅'
                        WHEN '3' THEN '已打印'
                        ELSE '' END 
                ) AS BGZT,                  
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
                A.TJBH,
                B.XM,
                (CASE XB WHEN '1' THEN '男' ELSE '女' END) AS XB,
                A.NL,
                C.SYRQ,
                C.SYXM,
                (select MC from TJ_DWDMB where DWBH=a.DWBH) as DWMC,
                C.SYBZ
            FROM 
            TJ_BGGL c INNER JOIN TJ_TJDJB a ON a.TJBH=c.TJBH  AND (a.del <> '1' or a.del is null) and a.QD='1' AND SUMOVER='1' AND (c.shrq>='%s' AND c.shrq<'%s')
        '''%(t_start,t_end)

# 根据审阅日期检索
def get_report_review_sql2(where_str):
    return '''
            SELECT
                (CASE C.BGZT
                        WHEN '0' THEN '待追踪'
                        WHEN '1' THEN '已审核'
                        WHEN '2' THEN '已审阅'
                        WHEN '3' THEN '已打印'
                        ELSE '' END 
                ) AS BGZT,                  
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
                A.TJBH,
                B.XM,
                (CASE XB WHEN '1' THEN '男' ELSE '女' END) AS XB,
                A.NL,
                C.SYRQ,
                C.SYXM,
                (select MC from TJ_DWDMB where DWBH=a.DWBH) as DWMC,
                C.SYBZ
            FROM 
            TJ_BGGL c INNER JOIN TJ_TJDJB a ON a.TJBH=c.TJBH  AND (a.del <> '1' or a.del is null) and a.QD='1' AND SUMOVER='1' 
            INNER JOIN TJ_TJDAB b ON a.DABH=b.DABH  AND %s
        '''%where_str

def get_item_state_sql(tjbh):
    return '''
            SELECT 
            
                (CASE 
                    WHEN qzjs ='1' THEN '已拒检'
                    WHEN qzjs IS NULL AND jsbz ='1' THEN '已小结'
                    WHEN qzjs IS NULL AND jsbz <>'1' AND ZXPB='0' THEN '核实'
                    WHEN qzjs IS NULL AND jsbz <>'1' AND ZXPB='1' THEN '已回写'
                    WHEN qzjs IS NULL AND jsbz <>'1' AND ZXPB='2' THEN '已登记'
                    WHEN qzjs IS NULL AND jsbz <>'1' AND ZXPB='3' THEN '已检查'
                    WHEN qzjs IS NULL AND jsbz <>'1' AND ZXPB='4' THEN '已抽血'
                    WHEN qzjs IS NULL AND jsbz <>'1' AND ZXPB='5' THEN '已留样'
                    ELSE '未定义' END
                ) AS STATE,
                XMBH,
                XMMC,
                (SELECT KSMC FROM TJ_KSDM WHERE KSBM=TJ_TJJLMXB.KSBM) AS KSMC,
                substring(convert(char,JCRQ,120),1,10) AS JCRQ,
                (SELECT YGXM FROM TJ_YGDM WHERE YGGH=TJ_TJJLMXB.JCYS) AS JCYS,
                substring(convert(char,shrq,120),1,10) AS SHRQ,
                (SELECT YGXM FROM TJ_YGDM WHERE YGGH=TJ_TJJLMXB.shys) AS SHYS,
                TMBH1,'' AS btn_name
            FROM TJ_TJJLMXB 
                WHERE TJBH='%s' AND SFZH='1' 
                AND XMBH NOT IN (SELECT XMBH FROM TJ_KSKZXM  WHERE KSBM='0028')
            ORDER BY qzjs DESC,jsbz,ZXPB DESC,KSBM,ZHBH,XSSX;
    ''' %tjbh


def get_report_efficiency_sql(start,end):
    return '''
            SELECT 
                TJBH,
                DATEDIFF ( Hour , QDRQ , SDRQ ) AS SDSC,
                DATEDIFF ( Hour , QDRQ , ZZRQ ) AS ZZSC,
                DATEDIFF ( Hour , Last_Item_Done , ZJRQ) AS ZJSC,
                DATEDIFF ( Hour , ZJRQ , SHRQ) AS SHSC,
                DATEDIFF ( Hour , SHRQ , SYRQ) AS SYSC,
                DATEDIFF ( Hour , SYRQ , DYRQ) AS DYSC
            FROM TJ_BGGL WHERE QDRQ>='%s' AND QDRQ<'%s'
    ''' %(start,end)

# 获取打印时长
def get_report_dy_sql(start,end):
    return '''
    SELECT  
        TJBH,substring(convert(char,QDRQ,120),1,10) AS QDRQ,
        substring(convert(char,SDRQ,120),1,10) AS SDRQ,
        SDXM,
        substring(convert(char,ZZRQ,120),1,10) AS ZZRQ,
        ZZXM,
        substring(convert(char,ZJRQ,120),1,10) AS ZJRQ,
        ZJXM,
        substring(convert(char,SHRQ,120),1,10) AS SHRQ,
        SHXM,
        substring(convert(char,SYRQ,120),1,10) AS SYRQ,
        SYXM,
        substring(convert(char,DYRQ,120),1,10) AS DYRQ,
        DYXM 
    FROM TJ_BGGL 
    WHERE (QDRQ>='%s' AND QDRQ<'%s') 
    AND (DATEDIFF ( Hour , SYRQ , DYRQ) IS NULL OR DATEDIFF ( Hour , SYRQ , DYRQ)>24)
    ORDER BY QDRQ
    '''%(start,end)

# 获取审阅时长
def get_report_sy_sql(start,end):
    return '''
    SELECT
        TJBH,substring(convert(char,QDRQ,120),1,10) AS QDRQ,
        substring(convert(char,SDRQ,120),1,10) AS SDRQ,
        SDXM,
        substring(convert(char,ZZRQ,120),1,10) AS ZZRQ,
        ZZXM,
        substring(convert(char,ZJRQ,120),1,10) AS ZJRQ,
        ZJXM,
        substring(convert(char,SHRQ,120),1,10) AS SHRQ,
        SHXM,
        substring(convert(char,SYRQ,120),1,10) AS SYRQ,
        SYXM,
        substring(convert(char,DYRQ,120),1,10) AS DYRQ,
        DYXM
    FROM TJ_BGGL 
    WHERE (QDRQ>='%s' AND QDRQ<'%s') 
    AND (DATEDIFF ( Hour , SHRQ , SYRQ) IS NULL OR DATEDIFF (Hour , SHRQ , SYRQ)>24)
    ORDER BY QDRQ
    '''%(start,end)

# 获取审核时长
def get_report_sh_sql(start,end):
    return '''
    SELECT
        TJBH,substring(convert(char,QDRQ,120),1,10) AS QDRQ,
        substring(convert(char,SDRQ,120),1,10) AS SDRQ,
        SDXM,
        substring(convert(char,ZZRQ,120),1,10) AS ZZRQ,
        ZZXM,
        substring(convert(char,ZJRQ,120),1,10) AS ZJRQ,
        ZJXM,
        substring(convert(char,SHRQ,120),1,10) AS SHRQ,
        SHXM,
        substring(convert(char,SYRQ,120),1,10) AS SYRQ,
        SYXM,
        substring(convert(char,DYRQ,120),1,10) AS DYRQ,
        DYXM
    FROM TJ_BGGL 
    WHERE (QDRQ>='%s' AND QDRQ<'%s') 
    AND (DATEDIFF ( Hour , ZJRQ , SHRQ) IS NULL OR DATEDIFF (Hour , ZJRQ , SHRQ)>24)
    ORDER BY QDRQ
    '''%(start,end)

# 获取总检时长
def get_report_zj_sql(start,end):
    return '''
    SELECT
        TJBH,substring(convert(char,QDRQ,120),1,10) AS QDRQ,
        substring(convert(char,SDRQ,120),1,10) AS SDRQ,
        SDXM,
        substring(convert(char,ZZRQ,120),1,10) AS ZZRQ,
        ZZXM,
        substring(convert(char,ZJRQ,120),1,10) AS ZJRQ,
        ZJXM,
        substring(convert(char,SHRQ,120),1,10) AS SHRQ,
        SHXM,
        substring(convert(char,SYRQ,120),1,10) AS SYRQ,
        SYXM,
        substring(convert(char,DYRQ,120),1,10) AS DYRQ,
        DYXM
    FROM TJ_BGGL 
    WHERE (QDRQ>='%s' AND QDRQ<'%s') 
    AND (DATEDIFF ( Hour , Last_Item_Done , ZJRQ) IS NULL OR DATEDIFF (Hour , Last_Item_Done , ZJRQ)>24)
    ORDER BY QDRQ
    '''%(start,end)

# 获取追踪时长
def get_report_zz_sql(start,end):
    return '''
    SELECT
        TJBH,substring(convert(char,QDRQ,120),1,10) AS QDRQ,
        substring(convert(char,SDRQ,120),1,10) AS SDRQ,
        SDXM,
        substring(convert(char,ZZRQ,120),1,10) AS ZZRQ,
        ZZXM,
        substring(convert(char,ZJRQ,120),1,10) AS ZJRQ,
        ZJXM,
        substring(convert(char,SHRQ,120),1,10) AS SHRQ,
        SHXM,
        substring(convert(char,SYRQ,120),1,10) AS SYRQ,
        SYXM,
        substring(convert(char,DYRQ,120),1,10) AS DYRQ,
        DYXM
    FROM TJ_BGGL 
    WHERE (QDRQ>='%s' AND QDRQ<'%s') 
    AND (DATEDIFF ( Hour , QDRQ , ZZRQ) IS NULL OR DATEDIFF (Hour , QDRQ , ZZRQ)>72)
    ORDER BY QDRQ
    '''%(start,end)

# 获取追踪时长
def get_report_sd_sql(start,end):
    return '''
    SELECT
        TJBH,substring(convert(char,QDRQ,120),1,10) AS QDRQ,
        substring(convert(char,SDRQ,120),1,10) AS SDRQ,
        SDXM,
        substring(convert(char,ZZRQ,120),1,10) AS ZZRQ,
        ZZXM,
        substring(convert(char,ZJRQ,120),1,10) AS ZJRQ,
        ZJXM,
        substring(convert(char,SHRQ,120),1,10) AS SHRQ,
        SHXM,
        substring(convert(char,SYRQ,120),1,10) AS SYRQ,
        SYXM,
        substring(convert(char,DYRQ,120),1,10) AS DYRQ,
        DYXM
    FROM TJ_BGGL 
    WHERE (QDRQ>='%s' AND QDRQ<'%s') 
    AND (DATEDIFF ( Hour , QDRQ , SDRQ) IS NULL OR DATEDIFF (Hour , QDRQ , ZZRQ)>8)
    ORDER BY QDRQ
    '''%(start,end)

# ORACLE PDF 路径 属于历史的
class MT_TJ_PDFRUL(BaseModel):

    __tablename__ = 'TJ_PDFRUL'

    ID = Column(VARCHAR(36), primary_key=True)
    TJBH = Column(VARCHAR(100), nullable=False)
    PDFURL = Column(VARCHAR(200),nullable=False)
    CREATETIME =Column(TIMESTAMP,nullable=False)

# ORACLE PDF 路径 属于历史的
class MT_TJ_DWBH(BaseModel):

    __tablename__ = 'TJ_DWBH'

    dwbh = Column(VARCHAR(5), nullable=True,primary_key=True)
    zlhm = Column(Integer, nullable=True,default=0)

class MT_TJ_PHOTO_ZYD(BaseModel):

    __tablename__ = 'TJ_PHOTO_ZYD'

    tjbh = Column(String(16), primary_key=True)                         # 体检编号
    picture_zyd = Column(BLOB, nullable=True)

# 所有的报告
def get_report_all_sql(start,end):
    return '''
        SELECT TJBH,
        substring(convert(char,QDRQ,120),1,10) AS QDRQ,
        substring(convert(char,DYRQ,120),1,10) AS DYRQ,
        (CASE DYFS 
            WHEN 0 THEN '租赁机打印'
            WHEN 1 THEN '本地打印'
            WHEN 2 THEN '自助机打印'
            ELSE '' END
        ) AS DYFS,
        DYCS FROM TJ_BGGL  WHERE QDRQ>='%s' AND QDRQ<='%s'
    '''%(start,end)

# 租赁打印报告
def get_report_zl_sql(start,end):
    return '''
        SELECT TJBH,
        substring(convert(char,QDRQ,120),1,10) AS QDRQ,
        substring(convert(char,DYRQ,120),1,10) AS DYRQ,
        DYXM,
        (CASE DYFS 
            WHEN 0 THEN '租赁机打印'
            WHEN 1 THEN '本地打印'
            WHEN 2 THEN '自助机打印'
            ELSE '' END
        ) AS DYFS,
        DYCS FROM TJ_BGGL  WHERE QDRQ>='%s' AND QDRQ<='%s' AND BGZT IN ('3','4','5') AND DYFS='0'
    '''%(start,end)

# 本地打印报告
def get_report_bd_sql(start,end):
    return '''
        SELECT TJBH,
        substring(convert(char,QDRQ,120),1,10) AS QDRQ,
        substring(convert(char,DYRQ,120),1,10) AS DYRQ,
        DYXM,
        (CASE DYFS 
            WHEN 0 THEN '租赁机打印'
            WHEN 1 THEN '本地打印'
            WHEN 2 THEN '自助机打印'
            ELSE '' END
        ) AS DYFS,
        DYCS FROM TJ_BGGL  WHERE QDRQ>='%s' AND QDRQ<='%s' AND BGZT IN ('3','4','5') AND DYFS='1'
    '''%(start,end)

# 自助打印报告
def get_report_zzj_sql(start,end):
    return '''
        SELECT TJBH,
        substring(convert(char,QDRQ,120),1,10) AS QDRQ,
        substring(convert(char,DYRQ,120),1,10) AS DYRQ,
        DYXM,
        (CASE DYFS 
            WHEN 0 THEN '租赁机打印'
            WHEN 1 THEN '本地打印'
            WHEN 2 THEN '自助机打印'
            ELSE '' END
        ) AS DYFS,
        DYCS FROM TJ_BGGL  WHERE QDRQ>='%s' AND QDRQ<='%s' AND BGZT IN ('3','4','5') AND DYFS='2'
    '''%(start,end)