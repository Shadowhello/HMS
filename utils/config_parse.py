import os,sys,base64
from configobj import ConfigObj


crypt_code = 'gbk'

def app_root(name):
    try:
        path = os.path.dirname(os.path.abspath(__file__))
    except NameError:  # We are the main py2exe script, not a module
        path = os.path.dirname(os.path.abspath(sys.argv[0]))

    return os.path.join(path,name)

# 加密
def encrypt(content:str):
    try:
        return str(base64.b64encode(content.encode(crypt_code)), crypt_code)
    except Exception as e:
        return ''

# 解密
def decrypt(content:str):
    try:
        return base64.b64decode(content.encode(crypt_code)).decode(crypt_code)
    except Exception as e:
        return ''

#读取配置参数
def config_parse(file_ini,crypt=False,code='UTF-8'):
    if not os.path.exists(file_ini):
        # log.info("读取配置文件：%s失败，文件不存在，请检查！" % file_ini)
        return {}
    # log.info("读取配置文件：%s"%file_ini)
    config=ConfigObj(file_ini, encoding=code)
    tmp={}
    if crypt:
        for key_p in config.keys():
            for key_c in config[key_p].keys():
                new_key=key_p+"_"+key_c
                value = decrypt(config[key_p][key_c])
                try:
                    new_value = int(value)
                except Exception as e:
                    new_value = value
                tmp[new_key] = new_value
    else:
        for key_p in config.keys():
            for key_c in config[key_p].keys():
                new_key=key_p+"_"+key_c
                try:
                    if config[key_p][key_c] in ['False','false']:
                        value = False
                    elif config[key_p][key_c] in ['True','true']:
                        value = True
                    else:
                        value = int(config[key_p][key_c])
                except Exception as e:
                    value = config[key_p][key_c]
                tmp[new_key]=value

    return tmp

#报告服务配置，由于PDF生成参数多且可随意组合，特殊处理分下面三点：
# 1、_ 替换为 -
# 2、节点名称不拼接
# 3、如果值为None,none 改参数则不进入列表
#
def config_report_parse(file_ini,code='UTF-8'):
    if not os.path.exists(file_ini):
        return {}
    config=ConfigObj(file_ini, encoding=code)
    # 需要解析进入 全局变量的 和不需要进入全局变量的
    parse={}
    no_parse = {}
    for key_p in config.keys():
        for key_c in config[key_p].keys():
            value = config[key_p][key_c]
            if key_p =='pdf':
                new_key=key_c
                # 对 bool值 处理
                if value in ['False', 'false']:
                    no_parse[new_key] = False
                elif value in ['True', 'true']:
                    no_parse[new_key] = True
                elif value in ['None', 'none']:
                    pass
                # 对整数处理
                elif value.isdigit():
                    # 判断是否是0开头的 默认为字符串
                    if value.startswith('0'):
                        no_parse[new_key] = value
                    else:
                        no_parse[new_key] = int(value)
                else:
                    no_parse[new_key] = value
            else:
                new_key = key_p + "_" + key_c

                # 对 bool值 处理
                if value in ['False', 'false']:
                    parse[new_key] = False
                elif value in ['True', 'true']:
                    parse[new_key] = True
                elif value in ['None', 'none']:
                    parse[new_key] = None
                # 对整数处理
                elif value.isdigit():
                    # 判断是否是0开头的 默认为字符串
                    if value.startswith('0'):
                        parse[new_key] = value
                    else:
                        parse[new_key] = int(value)
                else:
                    parse[new_key] = value


    return parse,no_parse

#写入配置参数
def config_write(file_ini,section,values,crypt=False,code='UTF-8'):
    if not os.path.exists(file_ini):
        # log.info("写入配置文件：%s失败，文件不存在，请检查！" % file_ini)
        return

    config=ConfigObj(file_ini, encoding=code)
    if crypt:
        for i, j in values.items():
            if isinstance(j,int):
                config[section][i] = encrypt(str(j))
            else:
                config[section][i] = encrypt(j)
        config.write()
    else:
        for i, j in values.items():
            config[section][i] = j
        config.write()
    # log.info("写入配置文件：%s" %file_ini)

if __name__=="__main__":
    file_ini = "F:\HMS\database.ini"
    tjxt_info = {"host":"10.8.200.201","database":"tjxt","user":"bsuser","passwd":"admin2389","port":1433}
    tjxt_bg_info = {"dns": "oracle101", "database": "TJ_CXK", "user": "TJ_CXK", "passwd": "TJ_CXK", "port": 1521}
    config_write(file_ini, "tjxt", tjxt_info, True)
    #config_write(file_ini, "tjxt_bg", tjxt_bg_info, True)
    #print(config_parse(file_ini,True))
