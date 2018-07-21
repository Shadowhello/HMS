import os,time,sys
from collections import OrderedDict
from jinja2 import Template
from mako.template import Template as  Template2
from reportserver.report_html import *
from utils.base import RemoteFileHandler
from utils.buildbarcode import BarCode

def str2(para:str):
    try:
        if isinstance(para,str):
            return para.encode('latin-1').decode('gbk')
        elif para==None:
            return ''
        else:
            return para
    except Exception as e:
        return para

class ReportBuildHTML(object):

    def __init__(self,outfile:str):
        if os.path.exists(outfile):
            os.remove(outfile)
        self.html_obj=open(outfile, 'a', encoding="utf8")
        # 头部
        self.html_obj.write(html_head)

    # 写入封面，基本信息
    def write_home_page(self,user):
        self.html_obj.write(Template2(html_home_page2).render(user=user))

    # 第二页，写入排班，体检小结，建议
    def write_second_page(self,summarys,suggestions,sign):
        self.html_obj.write(html_second_page)
        self.html_obj.write(Template(html_second_page_xj).render(summarys=summarys))
        self.html_obj.write(Template(html_second_page_jy).render(suggestions=suggestions))
        self.html_obj.write(Template2(html_second_page_sign).render(sign=sign))

    # 写入项目结果
    def write_item_result(self,items):
        self.html_obj.write(Template2(html_tj_xmjg).render(items=items))

    # 写入 设备项目检查报告 ->图片
    def write_equip_result(self,equips):
        self.html_obj.write(Template2(html_tj_equip).render(equips=equips))

    # 写入保健处方
    def write_health_care(self,healths):
        self.html_obj.write(Template2(html_tj_health_care).render(healths=healths))

    # 关闭文件
    def close(self):
        self.html_obj.write(html_tail)
        self.html_obj.close()

if __name__=="__main__":
    app_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    # 提取数据
    #env = Environment()
    # gols=env.make_globals({'g_element_top':0})

    tjbh='153192497'
    # tjbh = '149520265'

    from reportserver.model import *
    # 初始化
    ms_engine = create_engine('mssql+pymssql://bsuser:admin2389@10.8.200.201:1433/tjxt',encoding='utf8',echo=False)
    ms_session = sessionmaker(bind=ms_engine)()
    ora_engine= create_engine('oracle+cx_oracle://TJ_CXK:TJ_CXK@oracle101',encoding='gbk')
    ora_session = sessionmaker(bind=ora_engine)()

    describe = '''
    说明:<br />
    1.你过去患的疾病，因这次体检范围所限未能发现的情况，仍按原诊断及治疗。<br />
    2.查出的疾病请及时治疗,异常项目请到医院复查。<br />
    3.尽管我们会尽最大的努力，但因为医学的局限性和检查方式不同，有些疾病仍难以发现。<br />
    4.请详细阅读各项检查结果，如与总检结论不符或有疑惑，请及时与总检医生联系，联系电话:0574-83009689。<br />
    5.宁波明州医院国际保健中心总台联系电话:0574-83009619。<br />
    '''
    #  模板变量初始化
    zh_items=OrderedDict()
    equip_items = OrderedDict()
    mx_items={}
    jcjl = {}
    sign = {}
    health = {}

    bc= BarCode()
    bc.create2(tjbh)

    # 文件传输服务
    hander_pis = RemoteFileHandler('administrator','tomtaw')
    hander_pacs = RemoteFileHandler('administrator', 'Admin2389')
    time_start = time.time()
    # 人员信息
    user = ms_session.query(MV_RYXX).filter(MV_RYXX.tjbh == tjbh).scalar()
    user_i = user.dict()
    user_i['tm'] = os.path.join(app_path,'%s.png' %user.tjbh)
    report_title = '体检编号：%s     姓名：%s   性别：%s   年龄：%s ' %(user.tjbh,str2(user.xm),str2(user.xb),user.nl)
    sign['zjys'] = str2(user.zjys)
    sign['shys'] = str2(user.shys)
    sign['describe'] = describe

    # 取图片，是否齐全
    results=ms_session.query(MT_TJ_PACS_PIC).filter(MT_TJ_PACS_PIC.tjbh == tjbh)
    tmp = None
    count = 0
    pic = {}
    for result in results:
        if tmp==result.zhbh:
            count = count +1
        else:
            count = 1
            tmp = result.zhbh

        file_local = 'F:/HMS/reportserver/%s_%s_%s.jpg' % (result.tjbh, result.zhbh, count)
        # 病理
        if result.ksbm.strip()=='0026':
            file_remote = result.picpath.replace('\\','/').lstrip('//')
            is_done, error = hander_pis.down(file_remote, file_local)
            if is_done:
                if not pic.get(result.zhbh,0):
                    pic[result.zhbh] = []
                pic[result.zhbh].append(file_local)

        # PACS
        elif result.ksbm.strip() in ['0020','0024']:
            file_remote = '10.7.200.101/d$/space/pic/%s' %result.picname.replace('\\', '/')
            is_done, error = hander_pacs.down(file_remote, file_local)
            if is_done:
                if not pic.get(result.zhbh,0):
                    pic[result.zhbh] = []
                pic[result.zhbh].append(file_local)
        else:
            pass

    # 设备报告图片 心电图 0806、分体成分 5402、骨密度501576 从TJ_EQUIP 中获取
    equip_pic = ['F:/HMS/reportserver/153192497_0806.png','F:/HMS/reportserver/153192497_501576.jpg','F:/HMS/reportserver/153192497_5402.png']

    # 医生排班
    #results2 = ora_session.query(M_TJ_YSPB).filter(M_TJ_YSPB.ZFBZ=='0').order_by(M_TJ_YSPB.PBXQ).all()
    #for i in results2:
    #    print(i.YSXX)

    # 小结、建议
    results = ms_session.query(MT_TJ_JBQK).filter(MT_TJ_JBQK.tjbh == tjbh).order_by(MT_TJ_JBQK.jbpx).all()
    summarys=[]
    suggestions=[]
    for result in results:
        summarys.append(str2(result.jbmc))
        suggestions.append(str2(result.jynr))

    # 如果需要合并在一起  项目与图片
    # zhbh_equip_parent =[] #['0806','5402','501576'] # 要检测的
    # zhbh_equip_self =[]  # 自身的

    # 项目结果
    results = ms_session.query(MV_TJJLMXB).filter(MV_TJJLMXB.tjbh == tjbh).order_by(MV_TJJLMXB.kslx,MV_TJJLMXB.ksbm,MV_TJJLMXB.zhbh,MV_TJJLMXB.xssx).all()
    for result in results:
        if result.sfzh=='1':
            zh_items[str2(result.xmmc)] = result.zhbh
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
            jcjl[result.zhbh] = tmp
            if result.zhbh not in list(mx_items.keys()):
                mx_items[result.zhbh] = []

            # 组合项目 分 普通检查和单机设备检查
            # if result.zhbh not in zhbh_equip_parent:
            #     zh_items[str2(result.xmmc)] =result.zhbh
            # else:
            #     equip_items[str2(result.xmmc)] = result.zhbh
        else:
            if result.zhbh not in list(mx_items.keys()):
                mx_items[result.zhbh] = []
            mx_items[result.zhbh].append(result.mxxm())

    items = {'zhxm':zh_items,'mxxm':mx_items,'jcjl':jcjl,'pic':pic}

    # 获取保健处方
    if user.io_jkcf:
        health_title = ms_session.query(MT_TJ_BJCF_TITLE).filter(MT_TJ_BJCF_TITLE.inuser == '1').scalar()

        health['title'] = health_title.to_dict()
        health['body'] = 0
    else:
        pass

    # 生成html
    file_html ="C:/Users/Administrator/Desktop/pdf测试/test.html"
    file_pdf = "C:/Users/Administrator/Desktop/pdf测试/test.pdf"
    file_css = "F:/HMS/reportserver/report.css"
    html = ReportBuildHTML(file_html)
    html.write_home_page(user_i)
    html.write_second_page(summarys,suggestions,sign)
    html.write_item_result(items)
    if equip_pic:
        html.write_equip_result(equip_pic)

    if user.io_jkcf:
        html.write_health_care(health)
    html.close()


    time_end = time.time()
    print('totally cost', time_end - time_start)

    import webbrowser

    webbrowser.open(file_html)

    # raise EOFError
    import pdfkit
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe')
    options = {
    'page-size':'A4',
    'margin-top':'0.5in',
    'margin-right':'0.5in',
    'margin-bottom':'0.5in',
    'margin-left':'0.5in',
    'encoding':"UTF-8",
    'outline':None,                #  显示目录(文章中h1,h2来定)
    'outline-depth':1,             #  设置目录的深度（默认为4）
    'title':'测试',
    'dump-outline': 'toc.xml',
    'header-right': '浙江大学明州医院国际医疗保健', #(设置在中心位置的页眉内容)
    #'header-font-name':Arial,  #(设置页眉的字体名称)
    'header-font-size':12,     #设置页眉的字体大小
    #'header-right':'[page]/[toPage]',
    #'header-html':'header.html',  #添加一个HTML页眉,后面是网址
    #'header-line':None,  页眉下面的线
    'footer-left': report_title,
    #'footer-center':'明州国际医疗保健',
    'footer-right':'第[page]页 共[toPage]页',
    #'footer-html':'header.html',
    # 'footer-line':None, 页脚上面的线
    'enable-javascript':None
    #'user-style-sheet':file_css
    }
    cover_file='F:/HMS/reportserver/head.html',
    pdfkit.from_file(file_html, file_pdf,options=options,configuration=config,cover=cover_file,css=file_css)

    time_end2 = time.time()
    print('totally cost', time_end2 - time_start)