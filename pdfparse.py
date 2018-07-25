from watchdog.observers.read_directory_changes import WindowsApiObserver as Observer
from watchdog.events import FileSystemEventHandler
from utils.pdfmanager import *
from utils.api import *
from utils.base import *
from utils.envir import set_env
from utils.bmodel import *

# 操作数据库
def bulk_insert(session,datas):
    try:
        session.bulk_insert_mappings(MT_TJ_CZJLB, datas)
        session.commit()
    except Exception as e:
        session.rollback()
        print('插入失败！错误代码：%s' %e)


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
        self.initParas()

    # 初始化参数
    def initParas(self):
        # 数据库链接
        self.session = gol.get_value('tjxt_session_local')
        # 设备类型
        self.equip_type=str(gol.get_value('equip_type','00')).zfill(2)
        # 监控文件类型
        self.monitor_file_types = gol.get_value('monitor_file_types', ['.pdf', '.bmp', '.'])
        # 解析目录
        self.monitor_file_parse = gol.get_value('monitor_file_parse', 'C:/')
        # 是否删除原文件
        self.monitor_file_handle = gol.get_value('monitor_file_handle', True)
        # 监听后 等待多少秒后再处理
        self.monitor_file_sleep = gol.get_value('monitor_file_sleep', 2)
        # 日志
        self.log = gol.get_value('log')
        # 设备记录表
        self.equip_info={
                    'equip_type':self.equip_type,
                    'equip_name':EquipName[self.equip_type],
                    'xmbh': EquipNo[self.equip_type],
                    'hostname':gol.get_value('host_name', ''),
                    'hostip':gol.get_value('host_ip', ''),
                    'operator':gol.get_value('login_user_id', '未知'),
                    'operator2': gol.get_value('login_user_name', '未知'),
                    'operate_area': gol.get_value('login_area', '未知')
                }
        # 操作记录表
        self.czlj_info = {
            'jllx':EquipAction[self.equip_type],
            'jlmc': EquipActionName[self.equip_type],
            'tjbh':'',
            'mxbh':EquipNo[self.equip_type],
            'czgh':gol.get_value('login_user_id', ''),
            'czxm': gol.get_value('login_user_name', '未知'),
            'czsj':'',
            'czqy': gol.get_value('login_area', '未知')
        }

    def on_created(self, event):
        filename = event.src_path
        self.log.info("文件：%s 监听到，等待%s秒后进行处理！" %(filename,self.monitor_file_sleep))
        time.sleep(self.monitor_file_sleep)
        self.file_handle(filename)

    # 被监听文件：监听->解析->移动删除->上传
    def file_handle(self,filename):
        # 前缀名 后缀名
        prefix_name=os.path.splitext(filename)[0]
        suffix_name=os.path.splitext(filename)[1]
        if suffix_name in self.monitor_file_types:
            # 解析 电测听 数值
            if suffix_name=='.gnd':
                pass
                # result = get_cyct_result(filename)
                # from pprint import pprint
                # # 更新操作用户
                # result['jcys']=login_user
                # upload(result)
                # # self.conn.insert_cyct(result)
            elif suffix_name == '.pdf':
                # 解析PDF
                pdfinfo=txtparse(filename,self.equip_type)
                self.log.info("文件：%s -> %s 解析完成！" %(filename,pdfinfo['file']))
                # 合并解析信息
                new_pdfinfo=dict(pdfinfo,**self.equip_info)
                from pprint import pprint
                pprint(new_pdfinfo)

                # 移动文件
                if pdfinfo['file']:
                    new_file=os.path.join(self.monitor_file_parse,pdfinfo['file'])
                    shutil.copy2(filename, new_file)
                    # 上传文件
                    # upload_api(filename,new_file)
                    # 删除文件
                    if self.monitor_file_handle:
                        os.remove(filename)
                else:
                    new_file = None
                # 数据库更新
                self.update_db(pdfinfo['tjbh'],new_file,new_pdfinfo)
            else:
                pass

    # 更新数据库
    def update_db(self,tjbh,filename,equip_info:dict):
        self.czlj_info['tjbh'] = tjbh
        self.czlj_info['czsj'] = cur_datetime()
        # 更新记录：TJ_CZJLB
        try:
            self.session.bulk_insert_mappings(MT_TJ_CZJLB, [self.czlj_info])
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.log.info("体检顾客：%s，插入表TJ_CZJLB失败！错误信息：%s" %(tjbh,e))

        # 更新记录：TJ_TJJLMXB
        # 判断项目是否已小结
        result = self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,MT_TJ_TJJLMXB.xmbh == EquipNo[self.equip_type]).scalar()
        if result:
            if result.jsbz !='1':
                try:
                    self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,MT_TJ_TJJLMXB.zhbh == EquipNo[self.equip_type]).update({MT_TJ_TJJLMXB.zxpb: '3'})
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                    self.log.info("体检顾客：%s，更新表TJ_TJJLMXB失败！错误信息：%s" % (tjbh, e))
        else:
            self.log.info("体检顾客：%s，无项目：%s" %(tjbh,EquipName[self.equip_type]))

        # 更新记录：TJ_EQUIP
        try:
            result = self.session.query(MT_TJ_EQUIP).filter(MT_TJ_EQUIP.tjbh == tjbh,MT_TJ_EQUIP.equip_type == self.equip_type).scalar()
            if result:
                # 存在则更新,PDF更新
                self.session.query(MT_TJ_EQUIP).filter(MT_TJ_EQUIP.tjbh == tjbh,
                                                       MT_TJ_EQUIP.equip_type == self.equip_type
                                                       ).update(
                                                                {
                                                                    MT_TJ_EQUIP.modify_time: cur_datetime(),
                                                                    MT_TJ_EQUIP.file_path: equip_info['file_path'],            # 上传后的路径
                                                                    MT_TJ_EQUIP.operator: equip_info['operator'],              # 操作工号
                                                                    MT_TJ_EQUIP.operate_time: equip_info['operate_time'],      # 操作时间
                                                                    MT_TJ_EQUIP.hostname: equip_info['hostname'],
                                                                    MT_TJ_EQUIP.hostip: equip_info['hostip'],
                                                                    MT_TJ_EQUIP.operator2: equip_info['operator2'],            # 操作姓名
                                                                    MT_TJ_EQUIP.operate_area: equip_info['operate_area'],      # 操作区域
                                                                 }
                                                                )
            else:
                self.session.bulk_insert_mappings(MT_TJ_EQUIP, [equip_info])
                self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.log.info("体检顾客：%s，更新表TJ_EQUIP失败！错误信息：%s" %(tjbh,e))

        # 更新 DCP_files
        if filename:
            if self.equip_type=='08':
                dcp_info = {}
                dcp_info['cusn'] = tjbh
                dcp_info['department'] = '0018'
                dcp_info['filename'] = '%s.PDF' %tjbh
                dcp_info['filecontent'] = open(filename, 'rb').read()
                dcp_info['uploadtime'] = cur_datetime()
                dcp_info['flag'] = '0'
                self.session.query(MT_DCP_files).filter(MT_DCP_files.cusn == tjbh).delete()
                try:
                    self.session.bulk_insert_mappings(MT_DCP_files, [dcp_info])
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                    self.log.info("体检顾客：%s，更新表DCP_files失败！错误信息：%s" %(tjbh,e))

# 运行监控服务
def run(queue=None):
    set_env()
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
    run()