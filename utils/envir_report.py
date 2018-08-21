from .base import *
from .config_parse import *
from .dbconn import *
from .config_log import get_log_class
from utils import gol

# 初始化全局变量
def set_report_env(termial=False):
    app_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    # 打开日志功能
    report_log = get_log_class('report.log')
    gol.init()
    # 添加基础参数
    gol.set_value('report_log', report_log)                               # 添加设备日志   # 防止多进程日志写入冲突
    gol.set_value("host_name",hostname())                               # 添加主机名
    gol.set_value("host_ip", hostip())                                  # 添加主机IP
    gol.set_value("app_path", app_path)                                 # 添加程序根目录
    gol.set_value("path_tmp","%s/tmp/" %app_path)                       # 添加临时文件目录

    # 读取本地配置文件,加入全局参数
    report_log.info('程序启动......')
    parse, no_parse = config_report_parse('report.ini')
    gol.merge(parse)                         # 服务配置
    report_log.info('读取配置(mztj.ini)文件成功')
    # 连接数据库，设置session
    ####################体检数据链接#####################################
    try:
        session = get_tjxt_session(
            hostname=gol.get_value('tjxt_host','10.8.200.201'),
            dbname=gol.get_value('tjxt_database','tjxt'),
            user=gol.get_value('tjxt_user', 'bsuser'),
            passwd=gol.get_value('tjxt_passwd', 'admin2389'),
            port=gol.get_value2('tjxt_port', 1433)
        )
    except Exception as e:
        session = None
        report_log.info('连接体检数据库失败！错误信息：%s' %e)
    try:
        cxk_session = get_cxk_session()
    except Exception as e:
        cxk_session = None
        report_log.info('连接外网查询库数据库失败！错误信息：%s' %e)
    gol.set_value("session_tjxt", session)
    gol.set_value("session_cxk", cxk_session)
    if termial:
        gol.print_paras()

    return no_parse