from datalink.model import *
from sqlfiles.sql_ncd import *
import re

pattern1 = re.compile(r'约(\d?×\d?)mm')              # 匹配整数 * 整数
pattern2 = re.compile(r'约(\d?×\d\.\d?)mm')          # 匹配整数 * 小数
pattern3 = re.compile(r'约(\d\.\d?×\d?)mm')          # 匹配小数 * 整数
pattern4 = re.compile(r'约(\d\.\d?×\d\.\d?)mm')      # 匹配小数 * 小数

#pat_int = re.compile(r'(\d?)')              # 匹配整型
#pat_float = re.compile(r'(\d?\.\d?)')       # 匹配浮点型


def bulk_insert(session,datas):
    try:
        session.bulk_insert_mappings(MT_MB_YSKH, datas)
        session.commit()
    except Exception as e:
        session.rollback()
        print('批量插入失败！错误代码：%s' %e)   # Cannot insert duplicate key row
        for data in datas:
            try:
                session.bulk_insert_mappings(MT_MB_YSKH, [data])
                session.commit()
            except Exception as e:
                session.rollback()
                print('单个插入失败！错误代码：%s' %e)
                print(data)


def jzx_is_yc(results:list):
    if results:
        for result in results:
            for i in result[0].split('×'):
                try:
                    if int(i)>=8:
                        return True
                except Exception as e:
                    print(e)

    return False


def float2(result):
    if isinstance(result,str):
        try:
            return float(result)
        except Exception as e:
            return None
    elif isinstance(result,(int,float)):
        return result
    else:
        return None

class Item(object):

    def __init__(self,xmbh,xmjg,ycbz,ycts):
        self.xmbh = xmbh
        self.xmjg = xmjg
        self.ycbz = ycbz
        self.ycts = ycts

    @property
    def result(self):
        if self.xmbh=='050067':
            return str2(self.xmjg)
        else:
            return float2(self.xmjg)

    # 项目是否异常
    @property
    def is_yc(self):
        if self.ycbz=='1':
            return True
        else:
            return False

    # 项目偏高 还是偏低
    @property
    def is_hl(self):
        if self.ycts == '↑':
            return True
        else:
            return False



def xm_to_dict(xmxx:dict):
    # 同一人默认结果
    tmp={
            'is_gxy': '0', 'is_gxz': '0','is_gns': '0', 'is_gxt': '0', 'is_jzx': '0', 'glu': None,
            'glu2': None, 'hbalc': None, 'ua': None, 'tch': None, 'tg': None,'hdl': None,
            'ldl': None, 'hbp': None, 'lbp': None, 'jzxcs': None,'is_yc_glu':'0','is_yc_glu2':'0',
            'is_yc_hbalc': '0','is_yc_ua':'0','is_yc_tch':'0','is_yc_tg':'0','is_yc_hdl':'0',
            'is_yc_ldl':'0','is_yc_hbp': '0','is_yc_lbp':'0'
            }

    is_mbgl = False

    gxy = ['010015','010010']
    is_gxy = False
    gxz = ['100035','100036','100037','100038']
    is_gxz = False
    gns = ['100032']
    is_gns = False
    gxt = ['100033','100045','120031']
    is_gxt = False
    jzx = ['050067']
    is_jzx = False

    for xmbh in xmxx.keys():
        item = xmxx[xmbh]
        if xmbh in gxy:
            if item.is_yc:
                if xmbh == '010010':
                    tmp['is_yc_hbp'] = '1'
                else:
                    tmp['is_yc_lbp'] = '1'
                # 高值
                if item.is_hl:
                    tmp['is_gxy'] = '1'       # 血压异常
                    is_gxy = True

            if xmbh == '010010':
                tmp['hbp'] = item.result
            else:
                tmp['lbp'] = item.result

        elif xmbh in gxz:
            if item.is_yc:
                if xmbh == '100035':
                    tmp['is_yc_tch'] = '1'
                elif xmbh == '100036':
                    tmp['is_yc_tg'] = '1'
                elif xmbh == '100037':
                    tmp['is_yc_hdl'] = '1'
                else:
                    tmp['is_yc_ldl'] = '1'
                # 高值
                if item.is_hl:
                    tmp['is_gxz'] = '1'       # 血脂异常
                    is_gxz = True
            if xmbh == '100035':
                tmp['tch'] = item.result
            elif xmbh == '100036':
                tmp['tg'] = item.result
            elif xmbh == '100037':
                tmp['hdl'] = item.result
            else:
                tmp['ldl'] = item.result

        elif xmbh in gns:
            if item.is_yc:
                tmp['is_yc_ua'] = '1'
                if  item.is_hl:
                    tmp['is_gns'] = '1'       # 尿酸异常
                    is_gns = True

            tmp['ua'] = item.result

        elif xmbh in gxt:
            if item.is_yc:
                if xmbh == '100033':
                    tmp['is_yc_glu'] = '1'
                elif xmbh == '100045':
                    tmp['is_yc_glu2'] = '1'
                else:
                    tmp['is_yc_hbalc'] = '1'

                if item.is_hl:
                    tmp['is_gxt'] = '1'       # 血糖异常
                    is_gxt = True
            if xmbh == '100033':
                tmp['glu'] = item.result
            elif xmbh == '100045':
                tmp['glu2'] = item.result
            else:
                tmp['hbalc'] = item.result

        elif xmbh in jzx:
            jg1 = pattern1.findall(item.result)
            jg2 = pattern2.findall(item.result)
            jg3 = pattern3.findall(item.result)
            jg4 = pattern4.findall(item.result)
            jg = jg1 + jg2 + jg3 + jg4
            if jzx_is_yc(jg):
                tmp['is_jzx'] = '1'  # 甲状腺异常
                is_jzx = True
                tmp['jzxcs'] = item.result

        else:
            pass

    return any([is_gxy,is_gxz,is_gns,is_gxt,is_jzx]),tmp




if __name__ =="__main__":
    # 四高+甲状腺 筛选
    engine = create_engine('mssql+pymssql://bsuser:admin2389@10.8.200.201:1433/tjxt', encoding='utf8', echo=False)
    session = sessionmaker(bind=engine)()
    #  '2018-01-10','2018-01-21'
    results = session.execute(SQL_NCD %('2018-11-14','2018-11-15')).fetchall()
    count = 0
    #ryxx = {'tjbh':'','xm':'','xb':'','nl':0,'sjhm':'','sfzh':'','dwbh':'','dwmc':'','addr':'','ysje':0.00,
    #       'djrq':'','tjrq':'','qdrq':'','zjrq':'','shrq':'','zjys':'','shys':''}
    ryxx = {'tjbh':''}
    xmxx = {}
    tmp = []
    for result in results:
        if ryxx['tjbh']!=result[0]:
            if ryxx['tjbh']:
                flag,jcjl =xm_to_dict(xmxx)
                if flag:
                    tmp.append(dict(ryxx,**jcjl))
                    count = count +1
                    if count == 200:
                        bulk_insert(session,tmp)
                        print('插入记录：%s 行！' % str(count))
                        count = 0
                        #session.bulk_insert_mappings(MT_MB_YSKH,tmp)
                        tmp =[]

                xmxx = {}
                ryxx = {}
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
            xmxx[result[-1]] = Item(result[-1], result[-4], result[-3], str2(result[-2]))
        else:
            # 同一个人只叠加项目
            xmxx[result[-1]] = Item(result[-1], result[-4], result[-3], str2(result[-2]))

    if tmp:
        bulk_insert(session,tmp)
        print('插入记录：%s 行！' % str(len(tmp)))

    #session.commit()
        #raise  EOFError


