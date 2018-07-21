# 总检建议信息
sql_tj_zjsh = '''
  SELECT TJ_TJDJB.TJBH AS '体检编号',   
         TJ_TJDAB.XM AS '姓名',   
          (case TJ_TJDAB.XB when 1 then '男' when 2 then '女' else '' end) AS '性别',   
         TJ_TJDJB.NL AS '年龄',   
         TJ_TJDAB.SFZH AS '身份证号',  
		 TJ_TJDAB.SJHM AS '手机号码',   
         substring(convert(char,QDRQ,120),1,10) AS '体检日期', 
         (select MC from TJ_DWDMB where DWBH=TJ_TJDJB.DWBH) as '单位名称', 
         TJ_TJDJB.DEPART AS '部门',  
         (select ygxm from tj_ygdm where yggh=TJ_TJDJB.ZJYS ) as '总检医生',
         (select ygxm from tj_ygdm where yggh=TJ_TJDJB.SHYS ) as '审核医生'
    FROM TJ_TJDAB,   
         TJ_TJDJB  
   WHERE ( TJ_TJDAB.DABH = TJ_TJDJB.DABH ) 
    AND  ( TJ_TJDJB.SUMOVER = '1' ) 
    AND  ( TJ_TJDJB.QD = '1' )
    AND  ( TJ_TJDJB.DWBH = '%s' ) 
    AND  ( TJ_TJDJB.DEL = '' OR TJ_TJDJB.DEL IS NULL )  

    ORDER BY TJBH

'''
# 检验记录
sql_tj_jy = '''
SELECT TJ_TJDJB.TJBH AS '体检编号',   
         TJ_TJDAB.XM AS '姓名',   
          (case TJ_TJDAB.XB when 1 then '男' when 2 then '女' else '' end) AS '性别',   
         TJ_TJDJB.NL AS '年龄',   
         TJ_TJDAB.SFZH AS '身份证号',  
         TJ_TJDAB.SJHM AS '手机号码',   
         substring(convert(char,QDRQ,120),1,10) AS '体检日期', 
         (select MC from TJ_DWDMB where DWBH=TJ_TJDJB.DWBH) as '单位名称', 
         TJ_TJDJB.DEPART AS '部门',  
         (select ygxm from tj_ygdm where yggh=TJ_TJDJB.ZJYS ) as '总检医生',
         (select ygxm from tj_ygdm where yggh=TJ_TJDJB.SHYS ) as '审核医生',

TJ_TJJLMXB.XMMC AS '项目名称',

(CASE WHEN XMBH IN (SELECT XMBH FROM TJ_XMDM WHERE LBBM IN (SELECT LBBM FROM TJ_XMLB WHERE XMLX='1' AND SFZH='0')) THEN TJ_TJJLMXB.JG

  WHEN XMBH='700036' THEN TJ_TJJLMXB.JG ELSE TJ_TJJLMXB.ZD END ) AS '结果'


FROM TJ_TJDJB INNER JOIN TJ_TJDAB ON TJ_TJDJB.DABH=TJ_TJDAB.DABH 

AND ( TJ_TJDJB.SUMOVER = '1' ) AND  ( TJ_TJDJB.QD = '1' ) AND  ( TJ_TJDJB.DWBH = '%s' ) AND ( TJ_TJDJB.DEL = '' OR TJ_TJDJB.DEL IS NULL )

INNER JOIN TJ_TJJLMXB ON TJ_TJDJB.TJBH=TJ_TJJLMXB.TJBH

AND XMBH IN (SELECT XMBH FROM TJ_XMDM WHERE LBBM IN (SELECT LBBM FROM TJ_XMLB WHERE XMLX IN ('1','3')) AND SFZH='0')

AND TJ_TJDJB.TJBH='154080019' ORDER BY TJ_TJDJB.TJBH
'''