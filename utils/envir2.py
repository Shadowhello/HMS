# 定制化环境变量
from .base import *
from .config_parse import *
from utils import gol


def Init_env_vars(config_inis:list):
    app_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    gol.init()
    gol.set_value('app_path', app_path)
    gol.set_value("host_name",hostname())
    gol.set_value("host_ip", hostip())

    # 读取配置文件,加入全局参数
    for config_ini in config_inis:
        gol.merge(config_parse(config_ini))               # 主程序配置
    gol.print_paras('API服务')