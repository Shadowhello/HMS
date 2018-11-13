import zipfile,rarfile
import os,glob,sys
from utils import gol
from utils.config_parse import config_write
import subprocess

def update_version():
    filename = os.path.join(gol.get_value('app_path'),'version.ini')
    node = 'system'
    values = {'version':str(float(gol.get_value('system_version'))+0.01)}
    config_write(filename, node, values)

def extra_update_file():
    update_path = '%s/%s' %(gol.get_value('app_path') ,gol.get_value('update_path'))
    file_zips = glob.glob(os.path.join(update_path,'*.zip'))
    file_rars = glob.glob(os.path.join(update_path,'*.rar'))
    # print(file_zip,file_rar)

    if file_zips:
        for file_zip in file_zips:
            file_zip_obj = zipfile.ZipFile(file_zip, 'r')
            for file in file_zip_obj.namelist():
                try:
                    file_zip_obj.extract(file, gol.get_value('app_path'))
                except Exception as e:
                    print("文件%s：解压失败。错误信息：%s" %(file,e))
            # file_zip.extractall(gol.get_value('app_path'))
            file_zip_obj.close()
            os.remove(file_zip)

    if file_rars:
        for file_rar in file_rars:
            file_rar_obj = rarfile.RarFile(file_rar, 'r')
            for file in file_rar_obj.namelist():
                try:
                    file_rar_obj.extract(file, gol.get_value('app_path'))
                except Exception as e:
                    print("文件%s：解压失败。错误信息：%s" %(file,e))
            #file_rar_obj.extractall(gol.get_value('app_path'))
            file_rar_obj.close()
            os.remove(file_rar)

def main_end():
    # 结束主进程
    main_process_name = "hms.exe"
    try:
        os.system("taskkill /F /IM %s" %main_process_name)
    except Exception as e:
        print(e)

def main_start():
    # 启动主进程
    main_process_name = "hms.exe"
    try:
        os.popen(main_process_name)
    except Exception as e:
        try:
            os.popen(main_process_name)
        except Exception as e:
            print(e)


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
    pass



