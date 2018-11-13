from importlib import import_module
import zipfile,rarfile,os
from utils.envir import *


if __name__=="__main__":
    set_env(False)
    log =gol.get_value('log')
    try:
        # 采用动态模块为解决 打包后关闭和启动exe的问题
        module_class = getattr(import_module(gol.get_value('update_module')), gol.get_value('update_class'))
        module_class()
    except Exception as e:
        log.info('更新程序运行失败！错误信息：%s' %e)