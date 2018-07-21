import zipfile,rarfile
import os,glob,sys
from utils import gol
from utils.config_parse import config_write

def update_version():
    filename = os.path.join(gol.get_value('app_path'),'version.ini')
    node = 'system'
    values = {'version':str(float(gol.get_value('system_version'))+0.01)}
    config_write(filename, node, values)


def extra_update_file():
    update_path = '%s/%s' %(gol.get_value('app_path') ,gol.get_value('update_path'))
    # update_path_extract = gol.get_value('update_path_extract')
    file_zip = glob.glob(os.path.join(update_path,'*.zip'))
    file_rar = glob.glob(os.path.join(update_path,'*.rar'))
    # print(file_zip,file_rar)

    if file_zip:
        for file_name in file_zip:
            file_zip = zipfile.ZipFile(file_name, 'r')
            file_zip.extractall(gol.get_value('app_path'))
            file_zip.close()
            os.remove(file_name)

    if file_rar:
        for file_name in file_rar:
            file_zip = rarfile.RarFile(file_name, 'r')
            file_zip.extractall(gol.get_value('app_path'))
            file_zip.close()
            os.remove(file_name)

def run():
    main_process_name = gol.get_value('main_process_name', 'hms.exe')
    main_process_path = gol.get_value('main_process_path', 'hms.exe')
    sub_process_name = gol.get_value('sub_process_name', 'cmd.exe')
    log = gol.get_value('log')

    # 结束主进程
    try:
        os.system("taskkill /F /IM %s" %main_process_name)
        log.info('更新主程序前：结束滞留主进程！')
    except Exception as e:
        print(e)

    # 更新文件
    extra_update_file()
    # 更新版本号
    try:
        update_version()
    except Exception as e:
        log.info('版本文件：version.ini 更新失败！错误信息：%s' %e)
    # 启动主进程
    try:
        os.popen(main_process_path)
        log.info('更新主程序完成：重启主进程！')
    except Exception as e:
        print(e)

    # 结束自身进程
    try:
        os.system("taskkill /F /IM %s" %sub_process_name)
        log.info('更新主程序完成：结束自身进程！')
    except Exception as e:
        print(e)

if __name__=="__main__":
    run()

