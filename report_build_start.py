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
import time,os
from collections import OrderedDict
import pdfkit
from utils import set_report_env,BarCodeBuild,cur_datetime,RemoteFileHandler
from utils import gol
from app_reportserver import *
from jinja2 import Template
from mako.template import Template as Template2
from pprint import pprint







def run(queue=None):
    #######################初始化 全局参数######################################
    pdf_options = set_report_env(True)
    # from pprint import pprint
    # pprint(pdf_options)
    pdf_config = pdfkit.configuration(wkhtmltopdf=gol.get_value('report_dll'))
    pdf_css = gol.get_value('report_css')
    pdf_bg_img = gol.get_value('report_head_pic')
    pdf_sign_img = gol.get_value('report_sign')         # 签名图片位置
    # 数据库链接
    session_tjxt = gol.get_value('session_tjxt')
    session_cxk = gol.get_value('session_cxk')
    # 定义变量
    cachet = {'zjys':None,'shys':None,'warn':None}     # 公章、总检、审核医生签名
    ####################### 数据准备：图片、首页、html ###########################
    tjbh = '165572931'
    # pdf 数据对象
    pdf_data_obj = PdfData(session_tjxt,session_cxk,gol.get_value('report_path'),tjbh)
    # 该体检编号所在目录
    root_path = pdf_data_obj.get_cur_dir
    # 该体检编号 图片所在目录
    root_path_image = pdf_data_obj.get_img_dir

    # 传输 图片
    pdf_data_obj.transfer_pic()
    # ######################## PDF 报告首页 并生成 #######################
    i_user = pdf_data_obj.get_user_data
    if i_user:
        i_user['css'] = pdf_css
        i_user['head_pic'] = pdf_bg_img
        write_home_html(pdf_data_obj.get_head_html,i_user)
    # pdfkit.from_file(
    #     input=pdf_data_obj.get_head_html,  # path to HTML file or list with paths or file-like object
    #     output_path=pdf_data_obj.get_pdf,  # path to output PDF file. False means file will be returned as string.
    #     options=pdf_options,               # (optional) dict with wkhtmltopdf options, with or w/o '--'
    #     configuration=pdf_config,          # (optional) instance of pdfkit.configuration.Configuration()
    # )
    # return
    ######################## PDF 报告主体 并生成 #######################
    pdf_build_obj = buildBodyHtml(pdf_data_obj.get_body_html,pdf_css)
    ######################## 写入排班信息 ########################
    pdf_build_obj.write_yspb(pdf_data_obj.get_yspb)
    ######################## 写入小结、建议信息 ########################
    summarys, suggestions = pdf_data_obj.get_user_xjjy
    pdf_build_obj.write_xj(summarys)
    pdf_build_obj.write_jy(suggestions)
    ######################## 写入总检、审核医生签名及公章 ########################
    cachet['zjys'] = os.path.join(pdf_sign_img,'%s.png' %i_user['zjys'])
    cachet['shys'] = os.path.join(pdf_sign_img,'%s.png' %i_user['shys'])
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
    print('HTML头文件：%s' % pdf_data_obj.get_head_html)
    print('HTML主文件：%s' % pdf_data_obj.get_body_html)
    # pprint(pdf_options)
    pdf_options['footer-left'] = pdf_options['footer-left'] % (i_user['tjbh'], i_user['xm'], i_user['xb'], i_user['nl'])
    ######################### 生成 PDF #######################
    pdfkit.from_file(
        input=pdf_data_obj.get_body_html,  # path to HTML file or list with paths or file-like object
        output_path=pdf_data_obj.get_pdf,  # path to output PDF file. False means file will be returned as string.
        options=pdf_options,               # (optional) dict with wkhtmltopdf options, with or w/o '--'
        configuration=pdf_config,          # (optional) instance of pdfkit.configuration.Configuration()
        cover=pdf_data_obj.get_head_html,  # (optional) string with url/filename with a cover html page
        # css=pdf_css                        # (optional) string with path to css file which will be added to a single input file
    )
    #######################开始 处理 #######################################
    # if not queue:
    #     return
    # while True:
    #     # 处理的应该是两种请求：生成HTML PDF 方式 {'tjbh':123456789,'mode':'html'}
    #     handle = queue.get()
    #     if handle:
    #         tjbh = handle['tjbh']
    #         mode = handle['mode']
    #         if mode=='pdf':
    #             time_start = time.time()
    #             pdfkit.from_file(pdf_body_html, file_pdf,options=pdf_options,configuration=pdf_config,cover=pdf_head_html,css=pdf_css)
    #             time_end = time.time()
    #             print('%s 体检编号：%s 生成PDF报告成功，耗时：%s 秒！' %(cur_datetime(),tjbh,time_end - time_start))
    #         elif mode =='html':
    #             time_start = time.time()
    #             time_end = time.time()
    #             print('%s 体检编号：%s 生成HTML报告成功，耗时：%s 秒！' %(cur_datetime(),tjbh,time_end - time_start))
    #         else:
    #             pass
    #
    #     time.sleep(2)

def write_home_html(filename,user:dict):
    # 如果已存在，则删除
    if os.path.exists(filename):
        os.remove(filename)
    html_obj = open(filename, 'a', encoding="utf8")
    html_obj.write(Template2(pdf_html_home_page).render(user=user))

# PDF 数据对象：用于生成数据
# PDF 生成对象：用于生成HTML
class buildBodyHtml(object):

    def __init__(self,filename,file_css):
        # 如果已存在，则删除
        if os.path.exists(filename):
            os.remove(filename)
        self.html_obj = open(filename, 'a', encoding="utf8")
        self.html_obj.write(Template2(pdf_html_head).render(file_css=file_css))

    # 写入医生排班
    def write_yspb(self,pbxx:list):
        self.html_obj.write(Template2(pdf_html_yspb_page).render(pbxx=pbxx))

    # 写入体检小结
    def write_xj(self,summarys):
        self.html_obj.write(Template(pdf_html_summary_page).render(summarys=summarys))

    # 写入体检建议
    def write_jy(self,suggestions):
        self.html_obj.write(Template(pdf_html_suggest_page).render(suggestions=suggestions))

    # 写入体检注意事项及公章
    def write_cachet(self,cachet):
        self.html_obj.write(Template2(pdf_html_cachet_page).render(cachet=cachet))

    # 写入体检结果项目
    def write_items(self,items):
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

    def __init__(self,session_tjk,session_cxk,path,tjbh):
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

    # 获得用户数据
    @property
    def get_user_data(self):
        result = self.session_tjk.query(MV_RYXX).filter(MV_RYXX.tjbh == self.tjbh).scalar()
        if result:
            if result.io_jkcf=='1':
                self.io_jkcf = True
            i_user = result.pdf_dict
            i_user['tm'] = os.path.join(self.get_img_dir, '%s.png' % self.tjbh)
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

    # 获得当日的保存目录
    @property
    def get_cur_dir(self):
        dday = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
        dyear = dday[0:4]
        dmonth = dday[0:7]
        cur_path = '%s/%s/%s/%s/%s/' % (self.path, dyear, dmonth, dday, self.tjbh)
        if not os.path.exists(cur_path):
            os.makedirs(cur_path)
        return cur_path

    # 获得首页
    @property
    def get_head_html(self):
        return os.path.join(self.get_cur_dir, 'head.html')

    # 获得主体页面
    @property
    def get_body_html(self):
        return os.path.join(self.get_cur_dir, 'body.html')

    # 输出生成的pdf名称
    @property
    def get_pdf(self):
        return os.path.join(self.get_cur_dir, '%s.pdf' %self.tjbh)

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
    def transfer_pic(self):
        # ################ 1、条码号图片  ##########################
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

            file_local = os.path.join(self.get_img_dir, '%s_%s_%s.jpg' % (result.tjbh, result.zhbh, count))
            # 病理
            if result.ksbm.strip() == '0026':
                file_remote = result.picpath.replace('\\', '/').lstrip('//')
                is_done, error = hander_pis.down(file_remote, file_local)
                if is_done:
                    if not self.pic.get(result.zhbh, 0):
                        self.pic[result.zhbh] = []
                    self.pic[result.zhbh].append(file_local)

            # PACS
            elif result.ksbm.strip() in ['0020', '0024']:
                file_remote = '10.7.200.101/d$/space/pic/%s' % result.picname.replace('\\', '/')
                is_done, error = hander_pacs.down(file_remote, file_local)
                if is_done:
                    if not self.pic.get(result.zhbh, 0):
                        self.pic[result.zhbh] = []
                    self.pic[result.zhbh].append(file_local)
            else:
                pass
        # 4、骨密度、心电图、人体成分
        results = self.session_tjk.query(MT_TJ_EQUIP).filter(MT_TJ_EQUIP.tjbh == self.tjbh).all()
        if results:
            for result in results:
                file_local = os.path.join(self.get_img_dir, '%s_%s.png' % (result.tjbh, result.xmbh))
                file_remote = '10.7.200.101/d$/%s' % result.file_path.replace('D:/', '').replace('.pdf', '.png')
                is_done, error = hander_pacs.down(file_remote, file_local)
                if is_done:
                    self.pic[result.xmbh] = file_local
        else:
            pass

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
            pprint(bjcf_body)

        return health


if __name__ =='__main__':
    run()