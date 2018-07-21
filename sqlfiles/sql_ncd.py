# 慢病查询SQL
'''
100033 血糖
100045 餐后二小时血糖
120031 糖化血红蛋白(HbALC)

100032 尿酸

100035 总胆固醇
100036 甘油三酯(TG)
100037 高密度脂蛋白(HDL)
100038 低密度脂蛋白(LDL)

010015 舒张压
010010 收缩压

050067 甲状腺彩超
甲状腺结节大于0.8cm

'''

SQL_NCD = '''
    SELECT a.TJBH,b.XM,(CASE b.XB WHEN 1 THEN '男' WHEN '2' THEN '女' ELSE '' END ) AS XB,
    a.NL,b.SJHM,b.SFZH,b.ADDR,a.DWBH,(select MC from TJ_DWDMB where DWBH=a.DWBH) AS DWMC,a.YSJE,
    substring(convert(char,a.DJRQ,120),1,10) AS DJRQ,
    substring(convert(char,a.QDRQ,120),1,10) AS QDRQ,
    substring(convert(char,a.TJRQ,120),1,10) AS TJRQ,
    substring(convert(char,a.ZJRQ,120),1,10) AS ZJRQ,
    substring(convert(char,a.SHRQ,120),1,10) AS SHRQ,
    (select YGXM from TJ_YGDM where yggh=a.ZJYS ) as ZJYS,
    (select YGXM from TJ_YGDM where yggh=a.SHYS ) as SHYS,
    c.xmmc,c.JG,c.ycbz,c.ycts,c.xmbh
    
    FROM

    TJ_TJDJB a 
    
    INNER JOIN TJ_TJDAB b ON a.DABH=b.DABH AND (a.del <> '1' or a.del is null) AND a.SUMOVER='1' AND (a.ZJRQ>='%s' AND a.ZJRQ<'%s')
    
    INNER JOIN TJ_TJJLMXB c ON a.TJBH=c.TJBH  
    
    AND XMBH IN ('010010','010015','100032','100033','100035','100036','100037','100038','100045','120031','050067')
    
    ORDER BY a.TJBH
'''