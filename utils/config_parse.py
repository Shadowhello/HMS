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
