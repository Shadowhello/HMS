# 获取胶片数数量
def get_film_num(tjbh):
    return '''
        SELECT 

        (CASE 
        WHEN LBBM IN ('51','61') THEN 'MRI'
        WHEN LBBM = '28' THEN 'CT'
        WHEN LBBM = '49' THEN 'DR'
        WHEN LBBM = '18' THEN 'RX'
        ELSE '' END) AS JPMC,
        (CASE 
        WHEN LBBM IN ('51','61') THEN JPSL
        WHEN LBBM = '28' THEN JPSL
        WHEN LBBM = '49' THEN JPSL
        WHEN LBBM = '18' THEN JPSL
        ELSE 0 END) AS JPSL

        FROM (SELECT XMBH FROM TJ_TJJLMXB  WHERE tjbh='%s' AND SFZH='1' ) AS A

        INNER JOIN (SELECT XMBH,JPSL,LBBM FROM TJ_XMDM WHERE jpsl is NOT NULL) AS B ON A.XMBH=B.XMBH
    ''' % tjbh