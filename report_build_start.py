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
import time
import pdfkit
from utils import set_report_env,BarCodeBuild
from utils import gol
from app_reportserver import *
from utils.bmodel import *






def run(queue=None):
    #######################初始化 全局参数######################################
    pdf_options = set_report_env(True)
    # from pprint import pprint
    # pprint(pdf_options)
    pdf_config = pdfkit.configuration(wkhtmltopdf=gol.get_value('report_dll'))
    pdf_css = gol.get_value('report_css')
    pdf_cover=gol.get_value('report_cover')
    pdf_bg_img = gol.get_value('report_head_pic')
    # 数据库链接
    session_tjxt = gol.get_value('session_tjxt')
    ####################### 数据准备：图片、首页、html ###########################
    tjbh = '165572931'
    # 该体检编号所在目录
    root_path = get_cur_dir(gol.get_value('report_path'),tjbh)
    # 该体检编号 图片所在目录
    root_path_image = get_img_dir(gol.get_value('report_path'),tjbh)
    # 准备 图片
    transfer_pic(session_tjxt,root_path_image,tjbh)
    # PDF 报告首页 并生成
    pdf_head_html = os.path.join(root_path, 'head.html')
    i_user = get_user(session_tjxt,tjbh)
    i_user['tm'] = os.path.join(root_path_image,'%s.png' %tjbh)
    i_user['css'] = pdf_css
    i_user['head_pic'] = pdf_bg_img
    if i_user:
        write_home_html(pdf_head_html,i_user)


    #######################开始 处理 #######################################
    if not queue:
        return
    while True:
        # 处理的应该是两种请求：生成HTML PDF 方式 {'tjbh':123456789,'mode':'html'}
        handle = queue.get()
        if handle:
            tjbh = handle['tjbh']
            mode = handle['mode']
            if mode=='pdf':
                time_start = time.time()
                pdfkit.from_file(file_html, file_pdf,options=pdf_options,configuration=pdf_config,cover=pdf_cover,css=pdf_css)
                time_end = time.time()
                print('%s 体检编号：%s 生成PDF报告成功，耗时：%s 秒！' %(cur_datetime(),tjbh,time_end - time_start))
            elif mode =='html':
                time_start = time.time()
                time_end = time.time()
                print('%s 体检编号：%s 生成HTML报告成功，耗时：%s 秒！' %(cur_datetime(),tjbh,time_end - time_start))
            else:
                pass

        time.sleep(2)

def write_home_html(filename,user:dict):
    html_obj = open(filename, 'a', encoding="utf8")
    html_obj.write(Template2(pdf_html_home_page).render(user=user))


# 迁移图像或者生成图片 到指定位置
def transfer_pic(session,path,tjbh):
    # ################ 1、条码号图片  ##########################
    bc= BarCodeBuild(path=path)
    bc.create2(tjbh)
    # ################ 2、B超、内镜、病理图片 ########################
    # 文件传输服务
    hander_pis = RemoteFileHandler('administrator','tomtaw')
    hander_pacs = RemoteFileHandler('administrator', 'Admin2389')
    # 取图片，是否齐全
    results=session.query(MT_TJ_PACS_PIC).filter(MT_TJ_PACS_PIC.tjbh == tjbh).all()
    tmp = None
    count = 0
    pic = {}
    for result in results:
        if tmp==result.zhbh:
            count = count +1
        else:
            count = 1
            tmp = result.zhbh

        file_local = os.path.join(path,'%s_%s_%s.jpg' % (result.tjbh, result.zhbh, count))
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
    # 4、骨密度、心电图、人体成分
    results = session.query(MT_TJ_EQUIP).filter(MT_TJ_EQUIP.tjbh == tjbh).all()


# 获得当日的保存目录
def get_cur_dir(dirname,tjbh):
    dday = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    dyear = dday[0:4]
    dmonth = dday[0:7]
    cur_path = '%s/%s/%s/%s/%s/' %(dirname,dyear,dmonth,dday,tjbh)
    if not os.path.exists(cur_path):
        os.makedirs(cur_path)

    return cur_path

# 获得当日某人保存的图片目录
def get_img_dir(dirname,tjbh):
    dday = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    dyear = dday[0:4]
    dmonth = dday[0:7]
    cur_path = '%s/%s/%s/%s/%s/img/' %(dirname,dyear,dmonth,dday,tjbh)
    if not os.path.exists(cur_path):
        os.makedirs(cur_path)

    return cur_path

def get_user(session,tjbh):
    result = session.query(MV_RYXX).filter(MV_RYXX.tjbh == tjbh).scalar()
    if result:
        return result.pdf_dict
    return {}

if __name__ =='__main__':
    run()