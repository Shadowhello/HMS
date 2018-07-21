SQL_CDC = '''
    SELECT a.TJBH,b.XM,(CASE b.XB WHEN 1 THEN '男' WHEN '2' THEN '女' ELSE '' END ) AS XB,
    a.NL,b.SJHM,b.SFZH,b.ADDR,a.DWBH,(select MC from TJ_DWDMB where DWBH=a.DWBH) AS DWMC,a.YSJE,
    substring(convert(char,a.DJRQ,120),1,10) AS DJRQ,
    substring(convert(char,a.QDRQ,120),1,10) AS QDRQ,
    substring(convert(char,a.TJRQ,120),1,10) AS TJRQ,
    substring(convert(char,a.ZJRQ,120),1,10) AS ZJRQ,
    substring(convert(char,a.SHRQ,120),1,10) AS SHRQ,
    (select YGXM from TJ_YGDM where yggh=a.ZJYS ) as ZJYS,
    (select YGXM from TJ_YGDM where yggh=a.SHYS ) as SHYS,
    c.xmmc,c.JG,c.ZD,a.JY,c.xmbh
    
    FROM

    TJ_TJDJB a 
    
    INNER JOIN TJ_TJDAB b ON a.DABH=b.DABH AND (a.del <> '1' or a.del is null) AND a.SUMOVER='1' AND (a.ZJRQ>='%s' AND a.ZJRQ<'%s')
    
    INNER JOIN TJ_TJJLMXB c ON a.TJBH=c.TJBH  
    
    AND XMBH IN ('050060','050063','280029','280001','140049','120058')
    
    ORDER BY a.TJBH

'''