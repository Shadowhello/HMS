# 全局变量 文件
from pprint import pprint


def init():
    '''
    全局变量字典初始化
    :return: global_dict
    '''
    global global_dict
    global_dict = {}

def keys():
    return list(global_dict.keys())

def set_value(key,value):
    """ 定义一个全局变量 """
    global_dict[key] = value

def get_value(key,defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return global_dict[key]
    except KeyError:
        return defValue

def get_value2(key,defValue=None):
    """ 获得一个全局整型变量,不存在则返回默认值 ，存在不是整型返回默认值"""
    try:
        value = global_dict[key]
        if isinstance(value,(int,float)):
            return int(value)
        elif isinstance(value,str):
            try:
                return int(value)
            except Exception as e:
                return defValue
        else:
            return defValue
    except KeyError:
        return defValue

def get_child_value(key_p,key_c,defValue=None):
    try:
        value_p=global_dict[key_p]
        return value_p.get(key_c,defValue)
    except KeyError:
        return defValue

def print_paras(process_name=None):
    if process_name:
        print("############################ 初始化（%s）全局变量 ###############################" %process_name)
    else:
        print("############################ 初始化全局变量 ###############################")
    pprint(global_dict)
    print("############################               ###############################")
    return global_dict

def merge(new_dict):
    for key in new_dict.keys():
        global_dict[key]=new_dict[key]

def keys():
    return global_dict.keys()