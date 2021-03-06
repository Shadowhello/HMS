from .base import *
from .config_parse import *
from .dbconn import *
from .config_log import get_log_class
from utils import gol

# 初始化全局变量
def set_equip_env(termial=False):
    app_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    parse_log = get_log_class('parse.log')
    gol.init()
    gol.set_value('parse_log', parse_log)                               # 添加设备日志   # 防止多进程日志写入冲突
    gol.set_value("host_name",hostname())                               # 添加主机名
    gol.set_value("host_ip", hostip())                                  # 添加主机IP
    gol.set_value("app_path", app_path)                                 # 添加程序根目录
    gol.set_value("path_tmp","%s/tmp/" %app_path)                       # 添加临时文件目录
    gol.set_value("path_ico", "%s/resource/image/" %app_path)           # 添加资源文件目录
    gol.set_value("path_sql", "%s/sqlfiles/" % app_path)                # 添加SQL文件目录

    # 读取配置文件,加入全局参数
    parse_log.info('程序启动......')
    gol.merge(config_parse('mztj.ini'))               # 主程序配置
    parse_log.info('读取配置(mztj.ini)文件成功')
    gol.merge(config_parse('parse.ini'))              # 设备解析配置
    parse_log.info('读取配置(parse.ini)文件成功')
    gol.merge(config_parse('custom.ini'))             # 用户登录信息
    parse_log.info('读取配置(custom.ini)文件成功')
    gol.merge(config_parse('version.ini'))            # 版本信息
    parse_log.info('读取配置(version.ini)文件成功')
    gol.merge(config_parse('database.ini',True))      # 数据库配置
    parse_log.info('读取配置(database.ini)文件成功')

    # app_api = APIRquest(login_id=gol.get_value('login_user_id',''),
    #                 host = gol.get_value('api_host',''),
    #                 port = gol.get_value('api_port',''),
    #                 log = gol.get_value('log','')
    #                 )
    # gol.set_value('app_api', app_api)                                           # 添加API请求


    ####################体检数据链接#####################################
    session = get_tjxt_session(
        hostname=gol.get_value('tjxt_host','10.8.200.201'),
        dbname=gol.get_value('tjxt_database','tjxt'),
        user=gol.get_value('tjxt_user', 'bsuser'),
        passwd=gol.get_value('tjxt_passwd', 'admin2389'),
        port=gol.get_value2('tjxt_port', 1433),
        echo=termial
    )
    gol.set_value("tjxt_session_local", session)
    if termial:
        gol.print_paras()
