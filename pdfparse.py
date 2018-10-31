from watchdog.observers.read_directory_changes import WindowsApiObserver as Observer
from watchdog.events import FileSystemEventHandler
from utils.pdfmanager import *
from utils.api import *
from utils.base import *
from utils.envir_equip import set_equip_env
from utils.bmodel import *

# 说明：
# 2017-09-01 0.1  新增设备接口，增加设备：骨密度、心电图、电测听、大便仪、超声骨密度、C13/14
# 2018-05-01 0.2  重构设备接口，增加外出联网，增加设备：DR放射、肺功能（COM）
# 2018-07-26 0.3  重构设备接口
# 1、增加 PDF转Pic功能；
# 2、增加绩效、归档、日志补充 TJ_CZJLB,TJ_FILE_ACTIVE；
# 3、HTTP上传取代SMB上传方式；
# 2018-09-20 0.31  增加设备接口：人体成分（特殊版）图像识别功能，调用百度API进行识别解析体检编号，(Tesseract-OCR 识别率低，放弃本地识别模式)

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
        # 上传文件请求地址
        self.url = gol.get_value('api_equip_upload','')
        # 日志
        self.log = gol.get_value('parse_log')
        # 登录用户信息
        self.login_id = gol.get_value('login_user_id', '未知'),
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
        print("文件：%s 监听到，等待%s秒后进行处理！" %(filename,self.monitor_file_sleep))
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
                # 人体成分特殊处理，如果采用本地识别需要人工智能训练包，较繁琐且识别率无法保证，因此采用HTTP向百度人工智能请求
                s0 = time.time()
                if self.equip_type == '03':
                    pdfinfo = {"patient":'',"tjbh":'',"file":'',"operate_time":''}
                    old_file=os.path.join(self.monitor_file_parse,os.path.basename(filename))
                    shutil.copy2(filename, old_file)
                    pic_file = pdf2pic(old_file)
                    tjbh = get_ocr(pic_file)
                    if tjbh:
                        pdfinfo['tjbh'] = tjbh
                        pdfinfo['file'] = '%s_03.pdf' %tjbh
                        new_file = os.path.join(self.monitor_file_parse,'%s_03.pdf' %tjbh)
                        new_file_pic = os.path.join(self.monitor_file_parse, '%s_03.png' % tjbh)
                        # PDF 和图片均重命名
                        os.rename(old_file, new_file)
                        os.rename(pic_file, new_file_pic)
                        cost = time.time() - s0
                        self.log.info("文件：%s -> %s 解析完成！耗时：%s秒" % (filename, pic_file, str(round(cost, 2))))
                        # 合并解析信息
                        new_pdfinfo = dict(pdfinfo, **self.equip_info)
                        new_pdfinfo['operate_time'] = cur_datetime()
                        response = api_equip_upload(self.url, new_file)
                        if response:
                            new_pdfinfo['file_path'] = response['data']
                            self.log.info("文件：%s 上传成功！" % new_file)
                        else:
                            self.log.info("文件：%s 上传失败！" % new_file)
                        response = api_equip_upload(self.url, new_file_pic)
                        if response:
                            self.log.info("文件：%s 上传成功！" % new_file_pic)
                        else:
                            self.log.info("文件：%s 上传失败！" % new_file_pic)
                        # 删除文件
                        if self.monitor_file_handle:
                            os.remove(filename)
                    else:
                        self.log.info("图片：%s 解析体检编号失败！" %pic_file)
                        return
                else:
                    # 解析PDF
                    pdfinfo=txtparse(filename,self.equip_type)
                    if not pdfinfo:
                        self.log.info("文件：%s 解析失败！" % filename)
                        return
                    cost = time.time() - s0
                    self.log.info("文件：%s -> %s 解析完成！耗时：%s秒" %(filename,pdfinfo['file'],str(round(cost,2))))
                    # 合并解析信息
                    new_pdfinfo=dict(pdfinfo,**self.equip_info)
                    # from pprint import pprint
                    # pprint(new_pdfinfo)
                    if pdfinfo['file']:
                        # 移动文件
                        new_file=os.path.join(self.monitor_file_parse,pdfinfo['file'])
                        shutil.copy2(filename, new_file)
                        # 上传文件
                        if self.url:
                            s1 = time.time()
                            response = api_equip_upload(self.url,new_file)
                            if response:
                                new_pdfinfo['file_path'] = response['data']
                                cost = time.time()-s1
                                self.log.info("文件%s 上传成功！耗时：%s" % (new_file, str(round(cost, 2))))
                            else:
                                self.log.info("文件上传失败！错误信息：请求失败！")
                        else:
                            self.log.info("文件上传失败！错误信息：上传地址不存在！")

                        # 删除文件
                        if self.monitor_file_handle:
                            os.remove(filename)
                    else:
                        new_file = None
                s3 = time.time()
                # 数据库更新
                self.update_db(pdfinfo['tjbh'],new_file,new_pdfinfo)
                cost = time.time() - s3
                self.log.info("数据库操作完成！耗时：%s秒" % str(round(cost, 2)))
                # 返回 消息给 UI
                if self.process_queue:
                    self.process_queue.put(pdfinfo['tjbh'])
                    #self.process_queue.put('100000130') #测试
                    self.log.info("向UI传递消息：%s" %pdfinfo['tjbh'])
                if self.equip_type == '03':
                    pass
                else:
                    # 转换成图片,主要应用体检报告，嵌入到HTML中
                    try:
                        s2 = time.time()
                        pic_file = pdf2pic(new_file)
                        cost = time.time() - s2
                        self.log.info("Pdf(%s)->Pic转换成功！耗时：%s秒" % (new_file, str(round(cost, 1))))
                        response = api_equip_upload(self.url, pic_file)
                        if response:
                            new_pdfinfo['file_path'] = response['data']
                            self.log.info("文件(PDF与PNG)：%s 上传成功！" %new_file)
                        else:
                            self.log.info("文件上传失败！错误信息：请求失败！")
                    except Exception as e:
                        print(e)
                        self.log.info("Pdf(%s)->Pic转换失败！" % new_file)
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
        try:
            result = self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,MT_TJ_TJJLMXB.xmbh == EquipNo[self.equip_type]).scalar()
            if result:
                if self.equip_type=='03':
                    try:
                        self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,MT_TJ_TJJLMXB.zhbh == EquipNo[self.equip_type]).update({
                            MT_TJ_TJJLMXB.zxpb: '1',MT_TJ_TJJLMXB.jsbz: '1',MT_TJ_TJJLMXB.qzjs: None,
                            MT_TJ_TJJLMXB.jg: '检查已做，详见人体成分报告。',MT_TJ_TJJLMXB.jcys: self.login_id,MT_TJ_TJJLMXB.jcrq: cur_datetime()
                        })
                        self.session.commit()
                    except Exception as e:
                        self.session.rollback()
                        self.log.info("体检顾客：%s，更新表TJ_TJJLMXB失败！错误信息：%s" % (tjbh, e))
                else:
                    if result.jsbz !='1':
                        try:
                            self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,MT_TJ_TJJLMXB.zhbh == EquipNo[self.equip_type]).update({MT_TJ_TJJLMXB.zxpb: '3'})
                            self.session.commit()
                        except Exception as e:
                            self.session.rollback()
                            self.log.info("体检顾客：%s，更新表TJ_TJJLMXB失败！错误信息：%s" % (tjbh, e))
            else:
                self.log.info("体检顾客：%s，无项目：%s" %(tjbh,EquipName[self.equip_type]))
        except Exception as e:
            self.log.info("体检顾客：%s，查询表TJ_TJJLMXB失败！错误信息：%s" % (tjbh, e))

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
                equip_info['create_time'] = cur_datetime()
                self.session.bulk_insert_mappings(MT_TJ_EQUIP, [equip_info])
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.log.info("体检顾客：%s，更新表TJ_EQUIP失败！错误信息：%s" %(tjbh,e))

        # 更新归档表 TJ_FILE_ACTIVE

        # 更新 DCP_files 心电图 需要
        if filename:
            if self.equip_type=='08':
                dcp_info = {}
                dcp_info['cusn'] = tjbh
                dcp_info['department'] = '0018'
                dcp_info['filename'] = '%s.PDF' %tjbh
                dcp_info['filecontent'] = open(filename, 'rb').read()
                dcp_info['uploadtime'] = cur_datetime()
                dcp_info['flag'] = '0'
                try:
                    self.session.query(MT_DCP_files).filter(MT_DCP_files.cusn == tjbh).delete()
                    self.session.bulk_insert_mappings(MT_DCP_files, [dcp_info])
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                    self.log.info("体检顾客：%s，更新表DCP_files失败！错误信息：%s" %(tjbh,e))

# 运行监控服务
def run(queue=None):
    import cgitb
    cgitb.enable(logdir="./error/",format="text")
    set_equip_env(False)
    log = gol.get_value('parse_log')
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