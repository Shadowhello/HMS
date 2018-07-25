from watchdog.observers.read_directory_changes import WindowsApiObserver as Observer
from watchdog.events import FileSystemEventHandler
from utils.pdfmanager import *
from utils.api import *
from utils.base import *
from utils.envir import set_env

def upload_api(file_old,file_new):
    shutil.copy2(file_old, file_new)
    if gol.get_value('monitor_file_handle', True):
        # 是否删除原始文件
        os.remove(file_old)
    # 文件上传API
    response = upload_file(file_new)
    if response:
        if response['is_success'] == 1:
            # 上传成功删除，解析文件
            os.remove(file_new)

# 监听文件生成，解析，上传
class MonitorHandler(FileSystemEventHandler):

    def __init__(self,queue=None):
        super(MonitorHandler, self).__init__()
        self.process_queue = queue

    # 初始化参数
    def initParas(self):
        self.equip_type=str(gol.get_value('equip_type','00')).zfill(2)
        self.monitor_file_types = gol.get_value('monitor_file_types', ['.pdf', '.bmp', '.'])
        self.monitor_file_handle = gol.get_value('monitor_file_handle', True)
        self.monitor_file_sleep = gol.get_value('monitor_file_sleep', 2)
        self.log = gol.get_value('log')

    def on_created(self, event):
        # 监控到的文件
        filename = event.src_path
        self.log.info("文件：%s 监听生成！" % filename)
        equip_info={
                    'equip_type':self.equip_type,
                    'equip_name':EquipName[self.equip_type],
                    'xmbh': EquipNo[self.equip_type],
                    'host_name':gol.get_value('host_name', ''),
                    'host_ip':gol.get_value('host_ip', ''),
                    'oldfile':filename,
                    'login':gol.get_value('login_user_id', 'BSSA')
                }
        # 多少秒后处理
        time.sleep(self.monitor_file_sleep)
        # 前缀名 后缀名
        prefix_name=os.path.splitext(filename)[0]
        suffix_name=os.path.splitext(filename)[1]
        if suffix_name in self.monitor_file_types:
            # 解析
            if suffix_name=='.gnd':
                pass
                # #
                # result = get_cyct_result(filename)
                # from pprint import pprint
                # # 更新操作用户
                # result['jcys']=login_user
                # upload(result)
                # # self.conn.insert_cyct(result)

            elif suffix_name == '.pdf':
                # 解析PDF
                pdfinfo=parse(filename,equip_type)
                log.info("文件：%s -> %s 解析完成！" %(filename,pdfinfo['file']))
                new_pdfinfo=dict(pdfinfo,**info)
                # 解析后移动文件
                if pdfinfo['file']:
                    new_file=os.path.join(gol.get_value('monitor_fileparse', 'C:/'),pdfinfo['file'])
                    # 上传文件
                    upload_api(filename,new_file)

                # 数据上传API
                # upload(new_pdfinfo)
                # print(new_pdfinfo)
                # if equip_type == '01':
                #     sql=get_sql(prefix_name,'501716','胸部正位(不出片)','0019  ','X线摄影室',login_user)
                #     post_sql(sql)
                if equip_type == '08':
                #########################################
                    info["TJBH"] = new_pdfinfo['tjbh']
                    info["sql"] = get_sql(new_pdfinfo['tjbh'],'0806','心电图','0018  ','心电图室',login_user)
                    print(info["sql"])
                    info["OPERATOR"] = login_user
                    info["JCRQ"] = curren_datetime()
                    info["EQUIP_JG1"] = ''
                    info["EQUIP_JG2"] = ''
                    info["XMBH"] = '0806'
                    info["NAME"] = '心电图'
                    info["TYPE"] = '08'
                    response = post_fgn(info)
                    if response:
                        logger.info("体检编号：%s，心电图 上传成功！" % prefix_name)
                    else:
                        logger.info("体检编号：%s，心电图 上传失败！" % prefix_name)
                    print(info)
                    raise EOFError
            elif suffix_name == '.DCM':
                # 不做解析，只上传,DR
                pass
            else:
                pass
        else:
            print('%s 不需要被解析！' %filename)

    # 文件操作：解析、删除、上传
    def file_handle(self,filename,):
        # 前缀名 后缀名
        prefix_name=os.path.splitext(filename)[0]
        suffix_name=os.path.splitext(filename)[1]
        if suffix_name in self.monitor_file_types:
            # 解析 电测听 数值
            if suffix_name=='.gnd':
                pass


# 运行监控服务
def run(queue):
    # set_env()
    # for i in range(100):
    #     time.sleep(100)
    #     queue.put(i)
    log = gol.get_value('log')
    monitor_file_paths = gol.get_value('monitor_file_paths', 'C:/')
    monitor_polling_timer = gol.get_value('monitor_polling_timer', 2)
    observer = Observer()
    event_handler = MonitorHandler(queue)
    if isinstance(monitor_file_paths,list):
        for file_path in monitor_file_paths:
            if sure_path(file_path):
                observer.schedule(event_handler, file_path, True)
    else:
        if sure_path(monitor_file_paths):
            observer.schedule(event_handler, monitor_file_paths, True)

    log.info("设备监控服务已启动......")
    observer.start()
    try:
        while True:
            time.sleep(monitor_polling_timer)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    set_env()
    run()