from datalink.model import *
from sqlfiles.sql_cdc import *
import pandas as pd

yxs =['前列腺增生','肾囊肿','肾结石','输尿管结石','肾积水','肾肿瘤','肾上腺占位','肾上腺肿瘤','肾上腺增粗',
     '肾上腺增厚','膀胱肿瘤','膀胱占位','膀胱沟疝','睾丸鞘膜积液']

# PSA >6
# 红细胞(RBC) > 15


# 前列腺彩超及CT类项目
def select_1(zd,jy):
    for yx in yxs:
        if yx in zd:
            return True
        elif yx in jy:
            return True
    return False

def select(result:list):
    if result[-1] == '140049':
        if float2(result[-4]) > 6:
            return True
    elif result[-1] in ['120058','130059']:
        if float2(result[-4]) >= 10:
            return True
    else:
        if select_1(str2(result[-3]), str2(result[-2])):
            return True

    return False

def float2(result):
    if not result:
        return 0
    else:
        try:
            return float(result)
        except Exception as e:
            print(e)
            return 0



if __name__ =="__main__":
    # 疾病筛选
    # 泌尿科
    engine = create_engine('mssql+pymssql://bsuser:admin2389@10.8.200.201:1433/tjxt', encoding='utf8', echo=False)
    session = sessionmaker(bind=engine)()
    results = session.execute(SQL_CDC %('2018-08-03','2018-09-10')).fetchall()

    datas = []
    cols = ['tjbh', 'xm', 'xb', 'nl', 'sjhm', 'sfzh', 'addr', 'dwmc', 'ysje', 'qdrq', 'xmmc', 'xmjg', 'xmzd', 'jy']

    for result in results:
        if select(result):
            ryxx = {'tjbh': ''}
            # 记录当前人员信息
            ryxx['tjbh'] = result[0]
            ryxx['xm'] = str2(result[1])
            ryxx['xb'] = str2(result[2])
            ryxx['nl'] = result[3]
            ryxx['sjhm'] = result[4]
            ryxx['sfzh'] = result[5]
            ryxx['addr'] = str2(result[6])
            ryxx['dwbh'] = result[7]
            ryxx['dwmc'] = str2(result[8])
            ryxx['ysje'] = float(result[9])
            ryxx['djrq'] = result[10]
            ryxx['qdrq'] = result[11]
            ryxx['tjrq'] = result[12]
            ryxx['zjrq'] = result[13]
            ryxx['shrq'] = result[14]
            ryxx['zjys'] = str2(result[15])
            ryxx['shys'] = str2(result[16])
            ryxx['xmmc'] = str2(result[-5])
            ryxx['xmjg'] = str2(result[-4])
            ryxx['xmzd'] = str2(result[-3])
            ryxx['jy'] = str2(result[-2])

            datas.append(ryxx)

    filename ='C:/Users/Administrator/Desktop/三门核电/1.xlsx'
    df = pd.DataFrame(data=datas)
    df.to_excel(filename, columns=cols, index=False)