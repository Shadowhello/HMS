#结果接收功能

# 检验到体检
def lis2pes(result:dict,items:dict):
    tmp = {}
    tmp['tjbh'] = result['tjbh']
    tmp['xmbh'] = items.get(result['xmbh'],'99999999')  #转码 LIS->PES 过程
    tmp['ckfw'] = result['ckfw']
    tmp['xmdw'] = result['xmdw']
    tmp['xmbh'] = result['xmbh']
    tmp['jg'] = result['xmjg']
    tmp['jcys'] = result['jcys']
    tmp['jcrq'] = result['jcrq']
    tmp['shys'] = result['shys']
    tmp['shrq'] = result['shrq']

    tmp['zxpb'] = '1'
    tmp['jsbz'] = '1'
    if result['ycts']:
        tmp['ycts'] = result['ycts']
        tmp['ycbz'] = '1'

    return tmp

