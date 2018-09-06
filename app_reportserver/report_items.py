# 测试项目

def write_item_test(items):
    zhxms = items['zhxm']
    mxxms = items['mxxm']
    jcjl = items['jcjl']
    pic = items['pic']
    # 组合项目
    for item in zhxms.keys():
        xmlx = jcjl[zhxms[item]]['xmlx']
        kslx = jcjl[zhxms[item]]['kslx']
        ksbm = jcjl[zhxms[item]]['ksbm'].strip()
        zhbh = zhxms[item]
        if kslx == '2' or (kslx == '1' and ksbm in ['0001', '0038']):
            for mxxm in mxxms[zhxms[item]]:
                if mxxm['ycbz'] == '1':
                    if mxxm['ycts']:
                        print(mxxm['xmmc'])
                        print(mxxm['jg']+'&nbsp;&nbsp;&nbsp;'+mxxm['ycts'])
                        print(mxxm['xmdw'])
                        print(mxxm['ckfw'])
                    else:
                        print(mxxm['xmmc'],mxxm['jg'],mxxm['xmdw'],mxxm['ckfw'])
                else:
                    print(mxxm['xmmc'], mxxm['jg'], mxxm['xmdw'], mxxm['ckfw'])

                if jcjl[zhxms[item]]['shrq']:
                    jl = "检验医生：%s &nbsp;&nbsp;检验日期：%s &nbsp;&nbsp;&nbsp;&nbsp;审核医生：%s &nbsp;&nbsp;审核日期：%s" % (
                    jcjl[zhxms[item]]['jcys'], jcjl[zhxms[item]]['jcrq'], jcjl[zhxms[item]]['shys'],
                    jcjl[zhxms[item]]['shrq'])

                else:
                    jl = "检查医生：%s &nbsp;&nbsp;检查日期：%s " % (jcjl[zhxms[item]]['jcys'], jcjl[zhxms[item]]['jcrq'])

                print(jl)

        elif kslx == '1':
            for i, mxxm in enumerate(mxxms[zhxms[item]]):
                if i % 2 == 0:
                    if mxxm['ycbz'] == '1':
                        print(mxxm['xmmc'],mxxm['jg'])
                    else:
                        print(mxxm['xmmc'], mxxm['jg'])

                    if len(mxxms[zhxms[item]]) % 2 == 0:
                        if mxxms[zhxms[item]][i + 1]['ycbz'] == '1':
                            print(mxxms[zhxms[item]][i+1]['xmmc'],mxxms[zhxms[item]][i+1]['jg'])
                        else:
                            print(mxxms[zhxms[item]][i+1]['xmmc'],mxxms[zhxms[item]][i+1]['jg'])
                    else:
                        if i + 1 < len(mxxms[zhxms[item]]):
                            if mxxms[zhxms[item]][i + 1]['ycbz'] == '1':
                                print(mxxms[zhxms[item]][i+1]['xmmc'],mxxms[zhxms[item]][i+1]['jg'])
                            else:
                                print(mxxms[zhxms[item]][i+1]['xmmc'],mxxms[zhxms[item]][i+1]['jg'])

                    if jcjl[zhxms[item]]['shrq']:
                        jl = "检验医生：%s &nbsp;&nbsp;检验日期：%s &nbsp;&nbsp;&nbsp;&nbsp;审核医生：%s &nbsp;&nbsp;审核日期：%s" % (
                        jcjl[zhxms[item]]['jcys'], jcjl[zhxms[item]]['jcrq'], jcjl[zhxms[item]]['shys'],
                        jcjl[zhxms[item]]['shrq'])
                    else:
                        jl = "检查医生：%s &nbsp;&nbsp;检查日期：%s " % (jcjl[zhxms[item]]['jcys'], jcjl[zhxms[item]]['jcrq'])

                    print(jl)
        elif kslx=='3':
            for mxxm in mxxms[zhxms[item]]:
                print("检查所见：%s   诊断意见：%s" %(mxxm['jg'],mxxm['zd']))

                if ksbm == '0026':
                    if pic.get(zhbh, []):
                        print(pic[zhbh][0])
                    elif ksbm == '0020':
                        if pic.get(zhbh, []):
                            if len(pic[zhbh])>=2:
                                print(pic[zhbh][0],pic[zhbh][1])

