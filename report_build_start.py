# 存储目录主结构：
# /report/年/月/日/tjbh/
# 图片位置：/report/2018/2018-09/2018-09-01/166820124/image/...
# html位置：/report/2018/2018-09/2018-09-01/166820124/166820124.html
# pdf位置：/report/2018/2018-09/2018-09-01/166820124/166820124.pdf
# 166820124.html,166820124.pdf 后缀采用加密方式

# 正向步骤：
# 一、调用API
# 1、客户端审核完成调用 API服务；传递参数：tjbh 默认参数html
# 2、API服务传递 消息 给服务进程 队列
# 二、生成HTML
# 3、获取彩超、内镜、心电图、骨密度、人体成分等图片到指定目录下
# 4、如果缺少某类图片，写入数据库中
# 5、生成html
# 三、生成PDF
# 6、客户端审阅完成调用 API服务：传递参数：tjbh 默认参数pdf
# 7、生成PDF

# 反向步骤：
# 一、取消审阅
# 1、客户端取消审阅调用 API服务：传递参数：tjbh 默认参数pdf
import time,os,ujson
import shutil
from collections import OrderedDict
import pdfkit
from utils import set_report_env,BarCodeBuild,cur_datetime,RemoteFileHandler,fileRename
from utils import gol
from app_reportserver import *
from jinja2 import Template
from mako.template import Template as Template2
from pprint import pprint
from PyPDF2.pdf import PdfFileReader
from wand.image import Image
from utils.bmodel import *
import gc

def report_run_api(queue):
    try:
        report_run(queue)
    except Exception as e:
        print("报告服务运行出错，错误信息：%s" %e)

def report_run(queue):
    #######################初始化 全局参数######################################
    pdf_options = set_report_env(True)
    log = gol.get_value('report_log')
    # from pprint import pprint
    # pprint(pdf_options)
    ####################### 获取变量 ###########################
    pdf_config = pdfkit.configuration(wkhtmltopdf=gol.get_value('report_dll'))  # wkhtmltopdf 所在位置，带路径。如果加入环境变量，则需路径；
    pdf_css = gol.get_value('report_css')                                       # 主文件样式表
    pdf_cover_css = gol.get_value('report_cover_css')                           # 封面样式表
    pdf_bg_img = gol.get_value('report_head_pic')                               # 封面背景图
    pdf_sign_img = gol.get_value('report_sign')                                 # 签名图片位置
    html_css = gol.get_value('report_html_css')                                 # 主文件样式表
    html_bg_img = gol.get_value('report_html_head_pic')                         # 封面背景图
    html_sign_img = gol.get_value('report_html_sign')                           # 签名图片位置
    session_tjxt = gol.get_value('session_tjxt')                                # 数据库链接
    session_cxk = gol.get_value('session_cxk')                                  # 数据库链接
    cachet = {'zjys':None,'shys':None,'warn':None,'syys':None}                  # 公章、总检、审核医生签名
    footer_user = pdf_options['footer-left']
    html_path =gol.get_value('report_html_resource')
    gc_count = 0
    ####################### 数据准备：图片、首页、html ###########################
    while True:
        if not queue.empty():                                                           # 循环
            mes_obj = queue.get_nowait()                                                 # 获取进程队列消息,非阻塞模式
            gc_count = gc_count + 1
            # 显式释放内存
            if gc_count==100:
                gc.collect()
            # print('%s 从进程队列中获得消息：%s' %(cur_datetime(),ujson.dumps(mes_obj)))
            log.info('从进程队列中获得消息：%s' %ujson.dumps(mes_obj))
            tjbh = mes_obj['tjbh']                                                      # 获取体检编号
            action = mes_obj['action']                                                  # 获取执行动作 ：生成HTML还是生成PDF
            time_start = time.time()
            # pdf 数据对象
            pdf_data_obj = PdfData(session_tjxt,session_cxk,gol.get_value('report_path'),tjbh,action)
            # 设置状态
            pdf_data_obj.set_bgzt(action)
            # 设置html 路径
            pdf_data_obj.set_html_path(html_path)
            # ######################## PDF 报告封面是否单独生成 #######################
            i_user = pdf_data_obj.get_user_data
            if not i_user:
                log.info("未查询到顾客：%s 信息 " %tjbh)
                return
            if action=='pdf':
                # 资源文件位置不一致
                i_user['css'] = pdf_css
                i_user['cover_css'] = pdf_cover_css
                i_user['head_pic'] = pdf_bg_img
                sign_img = pdf_sign_img
                # 传输 图片
                pdf_data_obj.transfer_pic()
                # 单独生成封面
                write_home_html(pdf_data_obj.get_head_html,i_user)
                ######################## PDF 报告主体 从内容页开始写入 #######################
                pdf_build_obj = buildBodyHtml(pdf_data_obj.get_body_html,pdf_css)
            else:
                # 资源文件位置不一致
                i_user['css'] = html_css
                i_user['head_pic'] = html_bg_img
                sign_img = html_sign_img
                pdf_data_obj.transfer_pic(True)
                # HTML 报告
                ######################## PDF 报告主体 从首页开始写入 #######################
                pdf_build_obj = buildBodyHtml(pdf_data_obj.get_html, pdf_css,False)
                pdf_data_obj.set_bglj(pdf_data_obj.get_html)
                pdf_build_obj.write_home(i_user)
            ######################## 写入排班信息 ########################
            pdf_build_obj.write_yspb(pdf_data_obj.get_yspb)
            ######################## 写入小结、建议信息 ########################
            summarys, suggestions = pdf_data_obj.get_user_xjjy
            pdf_build_obj.write_xj(summarys)
            pdf_build_obj.write_jy(suggestions)
            ######################## 写入总检、审核医生签名及公章 ########################
            cachet['zjys'] = os.path.join(sign_img,'%s.png' %i_user['zjys'])
            cachet['shys'] = os.path.join(sign_img,'%s.png' %i_user['shys'])
            if i_user['syys']:
                cachet['syys'] = os.path.join(sign_img,'%s.png' %i_user['syys'])
            else:
                cachet['syys'] = None
            cachet['warn'] = warn
            pdf_build_obj.write_cachet(cachet)
            ######################## 写入项目结果 #######################
            pdf_build_obj.write_items(pdf_data_obj.get_item_result)
            ######################## 写入设备报告 #######################
            equip_pic = pdf_data_obj.get_equip_pic
            if equip_pic:
                pdf_build_obj.write_equip(equip_pic)
            ######################## 写入保健处方 #######################
            health = pdf_data_obj.get_jkcf
            if health:
                pdf_build_obj.write_health_care(health)
            # 关闭文件
            pdf_build_obj.close()
            time_end = time.time()
            print("%s: %s HTML报告生成成功！耗时：%s " % (cur_datetime(),tjbh,time_end - time_start))
            log.info("%s: %s HTML报告生成成功！耗时：%s " % (cur_datetime(),tjbh,time_end - time_start))
            # print('HTML头文件：%s' % pdf_data_obj.get_head_html)
            # print('HTML主文件：%s' % pdf_data_obj.get_body_html)
            if action == 'pdf':
                pdf_options['footer-left'] =footer_user  % (i_user['tjbh'], i_user['xm'], i_user['xb'], i_user['nl'])
                # pprint(pdf_options)
                ######################### 生成 PDF #######################
                pdfkit.from_file(
                    input=pdf_data_obj.get_body_html,  # path to HTML file or list with paths or file-like object
                    output_path=pdf_data_obj.get_pdf,  # path to output PDF file. False means file will be returned as string.
                    options=pdf_options,               # (optional) dict with wkhtmltopdf options, with or w/o '--'
                    configuration=pdf_config,          # (optional) instance of pdfkit.configuration.Configuration()
                    cover=pdf_data_obj.get_head_html,  # (optional) string with url/filename with a cover html page
                    css=pdf_css                        # (optional) string with path to css file which will be added to a single input file
                )
                time_end2 = time.time()
                print("%s: %s PDF报告生成成功！耗时：%s " %(cur_datetime(),tjbh,time_end2 - time_start))
                log.info("%s: %s PDF报告生成成功！耗时：%s " % (cur_datetime(),tjbh,time_end2 - time_start))
                pdf_data_obj.set_bglj(pdf_data_obj.get_pdf)
            ############################## 更新数据库 ########################################
            pdf_data_obj.update_user_report()
        else:
            time.sleep(1)

def write_home_html(filename,user:dict):
    # 如果已存在，则删除
    if os.path.exists(filename):
        os.remove(filename)
    html_obj = open(filename, 'a', encoding="utf8")
    html_obj.write(Template2(pdf_html_home_page).render(user=user))

# PDF 数据对象：用于生成数据
# PDF 生成对象：用于生成HTML
class buildBodyHtml(object):

    def __init__(self,filename,file_css,is_single=True):
        '''
        :param filename: HTML文件名称
        :param file_css: 样式表
        :param is_single: 是否单独写入head HTML文件
        '''
        # 如果已存在，则删除
        if os.path.exists(filename):
            os.remove(filename)
        self.html_obj = open(filename, 'a', encoding="utf8")
        if is_single:
            self.html_obj.write(Template2(pdf_html_head).render(file_css=file_css))

    # 写入首页
    def write_home(self,user):
        self.html_obj.write(Template2(pdf_html_home_page2).render(user=user))

    # 写入医生排班
    def write_yspb(self,pbxx:list):
        self.html_obj.write(Template2(pdf_html_yspb_page).render(pbxx=pbxx))

    # 写入体检小结
    def write_xj(self,summarys):
        self.html_obj.write(Template(pdf_html_summary_page).render(summarys=summarys))

    # 写入体检建议
    def write_jy(self,suggestions):
        if suggestions:
            self.html_obj.write(Template(pdf_html_suggest_page).render(suggestions=suggestions))

    # 写入体检注意事项及公章
    def write_cachet(self,cachet):
        if cachet['syys']:
            self.html_obj.write(Template2(pdf_html_cachet_page2).render(cachet=cachet))
        else:
            self.html_obj.write(Template2(pdf_html_cachet_page).render(cachet=cachet))

    # 写入体检结果项目
    def write_items(self,items):
        # from app_reportserver.report_items import write_item_test
        # write_item_test(items)
        self.html_obj.write(Template2(pdf_html_item_page).render(items=items))

    # 写入设备项目报告
    def write_equip(self,equips):
        self.html_obj.write(Template2(pdf_html_equip_page).render(equips=equips))

    # 写入保健处方
    def write_health_care(self,health):
        self.html_obj.write(Template2(pdf_html_health_page).render(health=health))

    # 关闭文件
    def close(self):
        self.html_obj.write(pdf_html_tail)
        self.html_obj.close()

# PDF 数据对象：用于生成数据
class PdfData(object):

    def __init__(self,session_tjk,session_cxk,path,tjbh,action):
        '''
        :param session_tjk: 体检库连接会话
        :param session_cxk: 查询库连接会话
        :param path: 根目录
        :param tjbh: 唯一表示
        '''
        # 初始化 数据
        self.session_tjk = session_tjk
        self.session_cxk = session_cxk
        self.tjbh = tjbh
        self.path =path
        self.action =action
        #
        self.citems = OrderedDict()    # 组合项目
        # key 用于标题，value 用于获取子项目明细
        # 示例如下：
        # OrderedDict([('一般检查(身高体重血压)', '0101'),
        #              ('内科', '0102'),
        #              ('外科', '0202'),
        #               ...................
        #              ('血常规', '1202'),
        #              ('尿常规(自动化分析)', '1308'),
        #              ('大生化', '1076'),
        #               ...................
        #              ('常规心电图', '0806'),
        #              ('颈椎正侧位(不出片)', '501707'),
        #              ('双(多)能骨密度', '501576'),
        #              ('头颅CT平扫(不出片)-低剂量', '501905'),
        #               ...................
        #           ])

        self.ditems = {}    # 明细项目
        # 示例 如下 ：
        # {'0101': [{'ckfw': '80-220','jg': '172.5','ksbm': '0001  ','kslx': '1','xmbh': '010012','xmdw': 'cm','xmmc': '身高','ycbz': '0','ycts': '','zd': ''},
        #           {'ckfw': '30-150','jg': '80','ksbm': '0001  ','kslx': '1','xmbh': '010011','xmdw': 'kg','xmmc': '体重','ycbz': '0','ycts': '','zd': ''},
        #           ...................
        #           {'ckfw': '18-24','jg': '27.04','ksbm': '0001  ','kslx': '1','xmbh': '090003','xmdw': '','xmmc': '体重指数(BMI)','ycbz': '1','ycts': '↑','zd': ''},
        #           ...................
        #          ],
        #  '0102': [{'ckfw': '','jg': '','ksbm': '0002  ','kslx': '1','xmbh': '010158','xmdw': '','xmmc': '足背动脉搏动','ycbz': '0','ycts': '','zd': ''},
        #           {'ckfw': '','jg': '','ksbm': '0002  ','kslx': '1','xmbh': '010117','xmdw': '','xmmc': '一般状况','ycbz': None,'ycts': '','zd': ''},
        #           ...................
        #           {'ckfw': '','jg': '无殊','ksbm': '0002  ','kslx': '1','xmbh': '010112','xmdw': '','xmmc': '肺','ycbz': '0','ycts': '','zd': ''},
        #           ...................
        #           ],
        # ...................
        # }
        self.jcjl = {}      # 检查记录
        # {'0101': {'jcrq': '2018-08-17','jcys': '薛颖','ksbm': '0001  ','kslx': '1','shrq': None,'shys': '','xmlx': '1','zhbh': '0101'},
        #  '0102': {'jcrq': '2018-08-17','jcys': '巫伟军','ksbm': '0002  ','kslx': '1','shrq': None,'shys': '','xmlx': '1','zhbh': '0102'},
        #  '0202': {'jcrq': '2018-08-17','jcys': '巫伟军','ksbm': '0003  ','kslx': '1','shrq': None,'shys': '','xmlx': '1','zhbh': '0202'},
        #   ...................
        # }
        self.pic = {}          # B超、内镜图片信息
        self.equip_pic=[]      # 设备报告图片路径
        self.io_jkcf = False   # 是否有健康处方
        self.out_file = None   # HTML 报告路径或者PDF报告路径
        self.cur_dir = None    # 该体检编号
        self.set_cur_dir()     # 设置当前目录
        self.html_path = None  # 设置HTML 资源跟路径

        # 汇总数据 待插入TJ_BGGL 表格
        self.user_data = {
            'tjbh':tjbh,
            'sybz':[]

        }

    # 设置报告状态 这里只有 html 审核完成待审阅 pdf 审阅完成待打印
    def set_bgzt(self,filetype):
        if filetype =='html':
            self.user_data['bgzt'] = '1'
        else:
            self.user_data['bgzt'] = '2'

    # 设置报告输出路径
    def set_bglj(self,filename):
        if filename.endswith('.pdf'):
            self.user_data['bgms'] = '1'
            # 获取PDF 页码
            try:
                pdf_read_obj = PdfFileReader(filename)
                self.user_data['bgym'] = pdf_read_obj.getNumPages()
            except Exception as e:
                print("获取报告页码出错，错误信息：%s" %e)
        else:
            self.user_data['bgms'] = '0'
        self.user_data['bglj'] = self.cur_dir

    def set_html_path(self,path):
        self.html_path = path

    # 获得用户数据
    @property
    def get_user_data(self):
        result = self.session_tjk.query(MV_RYXX).filter(MV_RYXX.tjbh == self.tjbh).scalar()
        if result:
            # 更新用户数据
            self.user_data['djrq'] = str(result.djrq)[0:19]
            self.user_data['djgh'] = result.djgh
            self.user_data['djxm'] = str2(result.djxm)
            self.user_data['qdrq'] = str(result.qdrq)[0:19]
            self.user_data['zjgh'] = result.zjys
            self.user_data['zjxm'] = str2(result.zjxm)
            self.user_data['zjrq'] = str(result.zjrq)[0:19]
            self.user_data['shgh'] = result.shys
            self.user_data['shxm'] = str2(result.shxm)
            self.user_data['shrq'] = str(result.shrq)[0:19]
            #########################################
            if result.io_jkcf=='1':
                self.io_jkcf = True
            i_user = result.pdf_dict
            if self.action=='pdf':
                i_user['tm'] = os.path.join(self.get_img_dir, '%s.png' % self.tjbh)
            else:
                i_user['tm'] = os.path.join(self.get_html_img_dir, '%s.png' % self.tjbh).replace(self.html_path,'')
            return i_user

        return {}

    # 获得该人保存的图片目录
    @property
    def get_img_dir(self):
        dday = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
        dyear = dday[0:4]
        dmonth = dday[0:7]
        cur_path = '%s/%s/%s/%s/%s/img/' % (self.path, dyear, dmonth, dday, self.tjbh)
        if not os.path.exists(cur_path):
            os.makedirs(cur_path)
        return cur_path

    # 获得该人保存的图片目录（HTML 用）
    @property
    def get_html_img_dir(self):
        dday = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
        dyear = dday[0:4]
        dmonth = dday[0:7]
        cur_path = '%s/%s/%s/%s/%s/img/' % (self.html_path, dyear, dmonth, dday, self.tjbh)
        if not os.path.exists(cur_path):
            os.makedirs(cur_path)
        return cur_path

    # 设置保存目录
    def set_cur_dir(self):
        # 如果已经存在，则用原来的路径
        result = self.session_tjk.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh==self.tjbh).scalar()
        if result:
            if result.bglj:
                report_file_rename(result.bglj,self.tjbh,self.action)
                self.cur_dir = result.bglj
                # return result.bglj
                return
        # 如果不存在，则生成当日路径
        dday = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
        dyear = dday[0:4]
        dmonth = dday[0:7]
        cur_path = '%s/%s/%s/%s/%s/' % (self.path, dyear, dmonth, dday, self.tjbh)
        if not os.path.exists(cur_path):
            os.makedirs(cur_path)
        self.cur_dir = cur_path
        # print("体检编号:%s 报告路径：%s" %(self.tjbh,self.cur_dir))

    # 获得封面 名称
    @property
    def get_head_html(self):
        return os.path.join(self.cur_dir, 'cover.html')

    # 获得内容页面 名称
    @property
    def get_body_html(self):
        return os.path.join(self.cur_dir, 'body.html')

    # 获得内容页面 名称
    @property
    def get_html(self):
        return os.path.join(self.cur_dir, '%s.html' %self.tjbh)

    # 输出生成的pdf名称
    @property
    def get_pdf(self):
        return os.path.join(self.cur_dir, '%s.pdf' %self.tjbh)

    # 获取小结、建议内容
    @property
    def get_user_xjjy(self):
        # 小结、建议
        results = self.session_tjk.query(MT_TJ_JBQK).filter(MT_TJ_JBQK.tjbh == self.tjbh).order_by(MT_TJ_JBQK.jbpx).all()
        summarys = []
        suggestions = []
        for result in results:
            summarys.append(str2(result.jbmc))
            suggestions.append(str2(result.jynr))
        if not summarys:
            sql = "select jy from tj_tjdjb where tjbh='%s';" %self.tjbh
            results = self.session_tjk.execute(sql).fetchall()
            if results:
                try:
                    summarys = [str2(results[0][0])]
                except Exception as e:
                    print(e,results[0])

        return summarys, suggestions

    @property
    def get_item_result(self):
        # 获取所有结果
        results = self.session_tjk.\
            query(MV_TJJLMXB).\
            filter(MV_TJJLMXB.tjbh == self.tjbh)\
            .order_by(MV_TJJLMXB.kslx, MV_TJJLMXB.ksbm,MV_TJJLMXB.zhbh,MV_TJJLMXB.xssx).all()

        for result in results:

            if result.sfzh == '1':
                self.citems[str2(result.xmmc)] = result.zhbh
                # 检查记录明细
                tmp = {}
                tmp['jcys'] = str2(result.jcys)
                tmp['jcrq'] = result.jcrq
                tmp['shys'] = str2(result.shys)
                tmp['shrq'] = result.shrq
                tmp['zhbh'] = result.zhbh
                tmp['xmlx'] = result.xmlx
                tmp['kslx'] = result.kslx
                tmp['ksbm'] = result.ksbm
                self.jcjl[result.zhbh] = tmp
                if result.zhbh not in list(self.ditems.keys()):
                    self.ditems[result.zhbh] = []
                    # 组合项目 分 普通检查和单机设备检查 便于 设备报告项目放在最后面
                    # if result.zhbh not in zhbh_equip_parent:
                    #     zh_items[str2(result.xmmc)] =result.zhbh
                    # else:
                    #     equip_items[str2(result.xmmc)] = result.zhbh
            else:
                if result.zhbh not in list(self.ditems.keys()):
                    self.ditems[result.zhbh] = []
                self.ditems[result.zhbh].append(result.mxxm())

        return {'zhxm': self.citems, 'mxxm': self.ditems, 'jcjl': self.jcjl, 'pic': self.pic}

    # 迁移图像或者生成图片 到指定位置
    def transfer_pic(self,flag=False):
        # 是否迁移HTML 图片
        # 默认为PDF 图片
        # ################ 1、条码号图片  ##########################
        if flag:
            bc = BarCodeBuild(path=self.get_html_img_dir)
        else:
            bc = BarCodeBuild(path=self.get_img_dir)
        bc.create2(self.tjbh)
        # ################ 2、B超、内镜、病理图片 ########################
        # 文件传输服务
        hander_pis = RemoteFileHandler('administrator', 'tomtaw')
        hander_pacs = RemoteFileHandler('administrator', 'Admin2389')
        # 取图片，是否齐全
        results = self.session_tjk.query(MT_TJ_PACS_PIC).filter(MT_TJ_PACS_PIC.tjbh == self.tjbh).all()
        tmp = None
        count = 0
        for result in results:
            if tmp == result.zhbh:
                count = count + 1
            else:
                count = 1
                tmp = result.zhbh
            if flag:
                file_local = os.path.join(self.get_html_img_dir, '%s_%s_%s.jpg' % (result.tjbh, result.zhbh, count))
            else:
                file_local = os.path.join(self.get_img_dir, '%s_%s_%s.jpg' % (result.tjbh, result.zhbh, count))
            # 病理
            if result.ksbm.strip() == '0026':
                if result.picpath:
                    file_remote = result.picpath.replace('\\', '/').lstrip('//')
                    is_done, error = hander_pis.down(file_remote, file_local)
                    if is_done:
                        if not self.pic.get(result.zhbh, 0):
                            self.pic[result.zhbh] = []
                        #
                        if flag:
                            self.pic[result.zhbh].append(file_local.replace(self.html_path,''))
                        else:
                            self.pic[result.zhbh].append(file_local)
                else:
                    # 缺图
                    print('%s：(%s)病理科室：项目(%s)不存在图片！' %(cur_datetime(),self.tjbh,result.zhbh))
                    self.user_data['sybz'].append('病理科室：项目（%s）不存在图片；' %result.zhbh)

            # PACS
            elif result.ksbm.strip() in ['0020', '0024']:
                if result.picname:
                    file_remote = '10.7.200.101/d$/space/pic/%s' % result.picname.replace('\\', '/')
                    is_done, error = hander_pacs.down(file_remote, file_local)
                    if is_done:
                        if not self.pic.get(result.zhbh, 0):
                            self.pic[result.zhbh] = []
                        if flag:
                            # print(file_local)
                            # print(file_local.replace(self.html_path, ''))
                            self.pic[result.zhbh].append(file_local.replace(self.html_path, ''))
                        else:
                            self.pic[result.zhbh].append(file_local)
                        #self.pic[result.zhbh].append(file_local)
                else:
                    # 缺图
                    print('%s：(%s)彩超/内镜科室：项目（%s）不存在图片！' %(cur_datetime(),self.tjbh,result.zhbh))
                    self.user_data['sybz'].append('彩超/内镜科室：项目（%s）不存在图片；' % result.zhbh)
            else:
                pass

        # 4、骨密度、心电图、人体成分
        results = self.session_tjk.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == self.tjbh,MT_TJ_TJJLMXB.sfzh == '1').all()
        for zhbh in list(set([result.zhbh for result in results])&set(list(('501576','0806','5402')))):
            result = self.session_tjk.query(MT_TJ_EQUIP).filter(MT_TJ_EQUIP.tjbh == self.tjbh,MT_TJ_EQUIP.xmbh == zhbh).scalar()
            # 服务端
            if result:
                if flag:
                    file_local = os.path.join(self.get_html_img_dir, '%s_%s.png' % (result.tjbh, result.xmbh))
                else:
                    file_local = os.path.join(self.get_img_dir, '%s_%s.png' % (result.tjbh, result.xmbh))
                #file_local = os.path.join(self.get_img_dir, '%s_%s.png' % (result.tjbh, result.xmbh))
                if result.file_path:
                    if os.path.exists(result.file_path.replace('.pdf', '.png')):
                        try:
                            shutil.copy2(result.file_path.replace('.pdf', '.png'),file_local)
                            # shutil.copy2(file_local, result.file_path)
                        except Exception as e:
                            print("文件复制失败，错误信息：%s。源码错误：report_build_start/line 521" %(e))
                    else:
                        # 存在PDF，不存在png 图片,则后台转换，针对历史报告
                        if os.path.exists(result.file_path):
                            pdf2pic(result.file_path,file_local)
                        else:
                            pass
                    # 添加
                    if flag:
                        self.pic[result.xmbh] = file_local.replace(self.html_path, '')
                    else:
                        self.pic[result.xmbh] = file_local
                        # self.pic[result.xmbh] = file_local
                else:
                    # 如果心电图PDF不存在，则从DCP_FIELS 读取
                    if zhbh == '0806':
                        result = self.session_tjk.query(MT_DCP_files).filter(MT_DCP_files.cusn == self.tjbh).scalar()
                        if result:
                            tmp_file = "%s_08.pdf" % self.tjbh
                            with open(tmp_file, "wb") as f:
                                f.write(result.filecontent)
                            pdf2pic(tmp_file, file_local)
                            os.remove(tmp_file)

                    # 添加
                    if flag:
                        self.pic['0806'] = file_local.replace(self.html_path, '')
                    else:
                        self.pic['0806'] = file_local
            # 本地测试
            # if result:
                # if flag:
                #     file_local = os.path.join(self.get_html_img_dir, '%s_%s.png' % (result.tjbh, result.xmbh))
                # else:
                #     file_local = os.path.join(self.get_img_dir, '%s_%s.png' % (result.tjbh, result.xmbh))
                # # file_local = os.path.join(self.get_img_dir, '%s_%s.png' % (result.tjbh, result.xmbh))
                # file_remote = '10.7.200.101/d$/%s' % result.file_path.replace('D:/', '').replace('.pdf', '.png')
                # is_done, error = hander_pacs.down(file_remote, file_local)
                # if is_done:
                    # 添加
                    # if flag:
                    #     self.pic[result.xmbh] = file_local.replace(self.html_path, '')
                    # else:
                    #     self.pic[result.xmbh] = file_local
                    # self.pic[result.xmbh] = file_local

            else:
                # 缺图
                print('%s (%s)设备接口：项目（%s）不存在图片！' %(cur_datetime(),self.tjbh,zhbh))
                self.user_data['sybz'].append('设备接口：项目（%s）不存在图片；' % zhbh)

    # 获取医生排班信息
    @property
    def get_yspb(self):
        datas = []
        # 空格字符串
        space_str = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        pbxq_match = {
            1: '星期一',
            2: '星期二',
            3: '星期三',
            4: '星期四',
            5: '星期五',
            6: '星期六',
            7: '星期日'
        }
        pbxw_match = {
            1: '上午',
            2: '下午'
        }
        results = self.session_cxk.query(MT_TJ_YSPB).filter(MT_TJ_YSPB.ZFBZ == '0').order_by(MT_TJ_YSPB.PBXQ,MT_TJ_YSPB.PBID).all()
        if results:
            for result in results:
                # 示例
                # 周一下午:14:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;呼吸内科主任：纪成
                datas.append(pbxq_match.get(result.PBXQ) +
                             pbxw_match.get(result.PBSXW) +
                             '：' +
                             result.PBKSSJ +
                             '-' +
                             result.PBJSSJ +
                             space_str +
                             result.YSXX
                             )

        return datas

    # 获取设备 报告 心电图 0806、分体成分 5402、骨密度501576
    @property
    def get_equip_pic(self):
        tmp = []
        for key in ['0806', '501576', '5402']:
            if self.pic.get(key,''):
                tmp.append(self.pic[key])

        return tmp

    @property
    def get_jkcf(self):
        health = {}
        if self.io_jkcf:
            bjcf_body = OrderedDict()
            result = self.session_tjk.query(MT_TJ_BJCF_TITLE).filter(MT_TJ_BJCF_TITLE.inuser == '1').scalar()
            if result:
                # 固定2项
                bjcf_body[str2(result.ltitle1)] = ''.join(['<p>' + i + '</p>' for i in str2(result.body1).split('\r\n')]) # '<p>' + str2(result.body1) + '</p>'
                bjcf_body[str2(result.ltitle2)] = ''.join(['<p>' + i + '</p>' for i in str2(result.body2).split('\r\n')]) # '<p>' + str2(result.body2) + '</p>'
                health['title'] = str2(result.title)
                health['stitle'] = str2(result.stitle)


            results = self.session_tjk.execute(get_bjcf_detail(self.tjbh)).fetchall()
            for result in results:
                bjcf_body[str2(result[0])] =''.join(['<p>' + i + '</p>' for i in str2(result[1]).split('\r\n')])             #.replace('\r\n','<br>')

            health['body'] = bjcf_body
            # pprint(bjcf_body)
        return health

    # 更新用户数据
    def update_user_report(self):

        self.user_data['sybz'] = '；'.join(self.user_data['sybz'])
        # pprint(self.user_data)
        result = self.session_tjk.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == self.tjbh).scalar()
        if result:
            if result.bgzt== '0':
                # 待追踪
                try:
                    self.session_tjk.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == self.tjbh).update({
                        MT_TJ_BGGL.sybz: self.user_data['sybz'],
                        MT_TJ_BGGL.bgzt: '1',
                        MT_TJ_BGGL.zjrq: self.user_data['zjrq'],
                        MT_TJ_BGGL.zjgh: self.user_data['zjgh'],
                        MT_TJ_BGGL.zjxm: self.user_data['zjxm'],
                        MT_TJ_BGGL.shrq: self.user_data['shrq'],
                        MT_TJ_BGGL.shgh: self.user_data['shgh'],
                        MT_TJ_BGGL.shxm: self.user_data['shxm'],
                        MT_TJ_BGGL.bglj: self.user_data['bglj']
                    })
                    self.session_tjk.commit()
                except Exception as e:
                    self.session_tjk.rollback()
                    print('插入 MT_TJ_BGGL 记录失败！错误代码：%s' % e)
            # 已经审核状态
            elif result.bgzt == '1':
                try:
                    self.session_tjk.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == self.tjbh).update({
                        MT_TJ_BGGL.sybz: self.user_data['sybz'],
                        MT_TJ_BGGL.bglj: self.user_data['bglj']
                    })
                    self.session_tjk.commit()
                except Exception as e:
                    self.session_tjk.rollback()
                    print('插入 MT_TJ_BGGL 记录失败！错误代码：%s' % e)
            else:
                # 已审阅 更新下PDF 页码
                try:
                    self.session_tjk.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == self.tjbh).update({
                        MT_TJ_BGGL.sybz: self.user_data['sybz'],
                        MT_TJ_BGGL.bgym: self.user_data.get('bgym',0),
                    })
                    self.session_tjk.commit()
                except Exception as e:
                    self.session_tjk.rollback()
                    print('插入 MT_TJ_BGGL 记录失败！错误代码：%s' % e)
        else:
            try:
                self.session_tjk.bulk_insert_mappings(MT_TJ_BGGL, [self.user_data])
                self.session_tjk.commit()
            except Exception as e:
                self.session_tjk.rollback()
                print('插入 MT_TJ_BGGL 记录失败！错误代码：%s' %e)

def pdf2pic(pdf,new_file=None):
    name = os.path.splitext(os.path.basename(pdf))[0] # 文件名称，不带路径
    img_obj = Image(filename=pdf, resolution=300)
    req_image = []
    for img in img_obj.sequence:
        img_page = Image(image=img)
        if name[-3:] == '_08':
            # 心电图 顺时针旋转 90度
            img_page.rotate(90)
        req_image.append(img_page.make_blob('png'))
    # 遍历req_image,保存为图片文件
    i = 0
    if not new_file:
        new_file = str(os.path.splitext(pdf)[0]) + '.png'
    for img in req_image:
        ff = open(new_file, 'wb')
        ff.write(img)
        ff.close()
        i += 1

    return new_file

# 指定文件存在，则重命名
def report_file_rename(path,tjbh,action):
    filename = os.path.join(path, '%s.%s' %(tjbh,action))
    if os.path.exists(filename):
        fileRename(filename)

class MT_TJ_BGGL(BaseModel):

    __tablename__ = 'TJ_BGGL'

    tjbh = Column(String(16), primary_key=True,nullable=True)           # 体检编号
    bgzt = Column(CHAR(1), nullable=True)                               # 报告状态 默认：追踪(0) 审核完成待审阅(1) 审阅完成待打印(2) 打印完成待整理(3) 4 整理  5 领取
    djrq = Column(DateTime, nullable=True)                              # 登记日期
    djgh = Column(String(16), nullable=False)                           # 登记工号
    djxm = Column(String(16), nullable=False)                           # 登记姓名
    qdrq = Column(DateTime, nullable=True)                              # 签到日期
    qdgh = Column(String(16), nullable=False)                           # 签到工号
    qdxm = Column(String(16), nullable=False)                           # 签到姓名
    sdrq = Column(DateTime, nullable=False)                             # 收单日期
    sdgh = Column(String(16), nullable=False)                           # 收单工号
    sdxm = Column(String(16), nullable=False)                           # 收单姓名
    zzrq = Column(DateTime, nullable=False,)                            # 追踪日期
    zzgh = Column(String(16), nullable=False)                           # 追踪工号
    zzxm = Column(String(16), nullable=False)                           # 追踪姓名
    zzbz = Column(Text, nullable=False)                                 # 追踪备注    记录电话等沟通信息，强制接收等信息
    zjrq = Column(DateTime, nullable=False)                             # 总检日期
    zjgh = Column(String(16), nullable=False)                           # 总检工号
    zjxm = Column(String(16), nullable=False)                           # 总检姓名
    zjbz = Column(Text, nullable=False)                                 # 总检备注
    shrq = Column(DateTime, nullable=False)                             # 审核日期
    shgh = Column(String(16), nullable=False)                           # 审核工号
    shxm = Column(String(16), nullable=False)                           # 审核姓名
    shbz = Column(Text, nullable=False)                                 # 审核备注    记录退回原因
    syrq = Column(DateTime, nullable=False)                             # 审阅日期
    sygh = Column(String(16), nullable=False)                           # 审阅工号
    syxm = Column(String(16), nullable=False)                           # 审阅姓名
    sybz = Column(Text, nullable=False)                                 # 审阅备注    记录退回原因
    sysc = Column(Integer, nullable=False, default=0)                   # 当次审阅时长 默认 0
    dyrq = Column(DateTime, nullable=False)                             # 打印日期
    dygh = Column(String(16), nullable=False)                           # 打印工号
    dyxm = Column(String(16), nullable=False)                           # 打印姓名
    dyfs = Column(CHAR(1), nullable=False)                              # 打印方式 默认 0 租赁打印  1 本地打印  2 自助打印
    dycs = Column(Integer, nullable=True, default=0)                    # 打印次数 默认 0
    zlrq = Column(DateTime, nullable=False)                             # 整理日期
    zlgh = Column(String(16), nullable=False)                           # 整理工号
    zlxm = Column(String(16), nullable=False)                           # 整理姓名
    zlhm = Column(String(16), nullable=False)                           # 整理货号
    lqrq = Column(DateTime, nullable=False)                             # 领取日期
    lqgh = Column(String(16), nullable=False)                           # 领取工号
    lqxm = Column(String(16), nullable=False)                           # 领取姓名
    lqfs = Column(String(16), nullable=False)                           # 领取方式
    lqbz = Column(Text, nullable=False)                                 # 领取备注    记录领取信息
    bgym = Column(Integer, nullable=True, default=0)                    # 报告页码，默认0页
    bglj = Column(String(250), nullable=False)                          # 报告路径 只存储对应PDF、HTML根路径
    bgms = Column(CHAR(1), nullable=False,default='0')                  # 报告模式 默认HTML 1 PDF
    last_item_done = Column(DateTime, nullable=False)                   # 最后一个项目完成时间
    jpdyrq = Column(DateTime, nullable=False)                           # 胶片打印日期
    jpdygh = Column(String(16), nullable=False)                         # 胶片打印工号
    jpdyxm = Column(String(16), nullable=False)                         # 胶片打印姓名
    jpsl = Column(String(16), nullable=False)                           # 胶片数量
    jpjjjl = Column(String(250), nullable=False)                        # 胶片交接记录
    bgth = Column(CHAR(1), nullable=True)                               # 报告退回          0 审核退回  1审阅退回
    gcbz = Column(Text, nullable=False)                                 # 过程备注    记录领取信息

if __name__ =='__main__':
    # import cgitb
    # # 非pycharm编辑器可用输出错误
    # #sys.excepthook = cgitb.Hook(1, None, 5, sys.stderr, 'text')
    # cgitb.enable(logdir="./error/",format="text")
    from utils.dbconn import get_tjxt_session
    from queue import Queue
    session = get_tjxt_session(
        hostname='10.8.200.201',
        dbname='tjxt',
        user='bsuser',
        passwd='admin2389',
        port=1433
    )
    q = Queue()
    #sql = "SELECT TJBH FROM TJ_TJDJB WHERE  (del <> '1' or del is null) and QD='1' and SHRQ>='2018-08-25' AND SHRQ<'2018-09-30' AND SUMOVER='1'; "
    # 处理遗漏的
    sql = "SELECT TJBH FROM TJ_TJDJB WHERE SUMOVER='1' AND SHRQ>='2018-09-01' AND QD='1' AND (del <> '1' or del is null) AND TJBH NOT IN (SELECT TJBH FROM TJ_BGGL WHERE BGZT<>'0')"
    # 处理没有报告路径的
    sql2 = "SELECT TJBH FROM TJ_BGGL WHERE bgzt='1' AND BGLJ IS NULL"
    # 处理PDF 生成的
    # sql = "SELECT TJBH FROM TJ_BGGL WHERE SYRQ>='2018-09-28'"
    #sql = "SELECT TJBH FROM TJ_TJDJB WHERE SUMOVER='1' AND SHRQ>='2018-09-01' AND dybj IS NULL AND (del <> '1' or del is null) AND tjqy IN ('1','2','3','4')  "
    results = session.execute(sql).fetchall()
    for result in results:
        q.put({'tjbh': result[0], 'action': 'html'})
    results = session.execute(sql2).fetchall()
    for result in results:
        q.put({'tjbh': result[0], 'action': 'html'})
    # sql = "SELECT  "
    # q.put({'tjbh': '165583081', 'action': 'html'})
    report_run(q)