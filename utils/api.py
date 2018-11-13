from collections import OrderedDict
import requests
from pprint import pprint
import urllib.parse
from utils import gol

# 使用装饰器改写
# 提取公共功能

# print(response.status_code)     # 打印状态码
# print(response.url)             # 打印请求url
# print(response.headers)         # 打印头信息
# print(response.cookies)         # 打印cookie信息
# print(response.text)            # 以文本形式打印网页源码
# print(response.content)         # 以字节流形式打印
# print(response.json())          # 同json.loads(response.text)

def trans_pacs_pic(tjbh,ksbm,xmbh):
    url_default = "http://10.7.200.101:4009/api/pacs/pic/%s/%s/%s" %(tjbh,ksbm,xmbh)
    url_config = gol.get_value('api_pacs_pic','')
    if url_config:
        url = url_config %(tjbh,ksbm,xmbh)
    else:
        url = url_default
    try:
        response = requests.post(url)
        if response.status_code == 200:
            if response.json()['code'] == 1:
                return True
            else:
                return False
    except Exception as e:
        return False



# 发送短信
def sms_api(mobile,context):
    url = "http://10.8.200.103/MzyySoa/soa/sendSms"
    #url="http://10.8.200.103/MzyySoa/soa/sendSms2?"
    data = OrderedDict([('mobile', mobile), ('content', context.encode("gbk")), ('smsId', 999)])
    response = requests.post(url, params=data)
    #response.text ={"msg": "参数异常!", "ret": "4"}
    #response.text ={"msg": "执行成功!", "ret": "1"}
    if "执行成功" in response.text:
        return 1
    else:
        return 0

def get_ocr(picname):
    url_default = "http://10.7.200.101:4009/api/pic2txt/"
    # url_config = gol.get_value('api_pic2txt')
    url_config = None
    if url_config:
        url = url_config
    else:
        url = url_default
    file_obj = {"file": (picname, open(picname, "rb"))}
    try:
        response = requests.post(url,files=file_obj)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print('URL：%s 请求失败！错误信息：%s' %(url,e))

# 从微信端获取二维码图片 字节流
def get_barcode_wx(xm,sfzh,sjhm,email='',address=''):
    url = 'http://app.nbmzyy.com/tjadmin/pInfoSubmit'
    # url = 'http://10.7.200.60:80/tjadmin/pInfoSubmit'
    #url = 'http://10.7.200.27:8089/tjadmin/pInfoSubmit'
    head = {}
    head['realName'] = urllib.parse.quote(xm)
    head['idCardNum'] = sfzh
    head['phoneNumber'] = sjhm
    head['email'] = ''
    head['address'] = ''
    head['Content-Type'] = 'application/json'

    response = requests.post(url,headers=head)
    if response.status_code==200:
        print(response.content)
        f = open('1.png', "wb")
        for chunk in response.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        f.close()

def api_print(tjbh,printer):
    url = gol.get_value("api_report_print",None)
    if url:
        # try:
        response = requests.post(url %(tjbh,printer))
        if response.status_code == 200:
            if response.json()['code']==1:
            # if '报告打印成功' in response.json():
                return True
            else:
                return False
        else:
            return False
        # except Exception as e:
        #     print(e)
        #     return False


# 构建二维码测试请求
def request_post_wx():
    params= {'tjbh': '100000125', 'xm': '张三', 'sfzh': '330227198702040773','sjhm':'15058494793','login_id':'17sx15'}
    url = "http://10.7.103.205:4000/api/qrcode/%s/%s " %('100000125','17sx15')
    requests.post(url)


# get 请求
def request_get(url,save_file=None):
    '''
    :param url:             请求地址
    :param save_file:       下载文件 save_file
    :return:
    '''
    response = requests.get(url)
    if response.status_code==200:
        try:
            f = open(save_file, "wb")
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
            f.close()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False

# get 请求 下载文件  返回二进制流
def api_file_down(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return False

# post 请求
def api_equip_upload(url,filename):
    file_obj = {"file": (filename, open(filename, "rb"))}
    try:
        response = requests.post(url,files=file_obj)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print('URL：%s 请求失败！错误信息：%s' %(url,e))


class APIRquest(object):

    def __init__(self,login_id,host,port,log):
        self.log =log
        self.host = host
        self.port = port
        self.login_id = login_id

    def get_url(self,url):
        return 'http://%s:%s/%s' %(self.host,str(self.port),url)

    def set_file_type(self,file_type):
        self.file_type = file_type


    def request(self,url,method='get',headers={},filename=None,datas=None):
        '''
        :param url:         请求地址
        :param method:      请求方法 get/post
        :param headers:     用户信息
        :param filename:      上传的文件
        :param datas:       上传的数据
        :return:            {"code"0,"mes":xx,"data":xx}
        '''
        headers['user'] = str(self.login_id)
        pprint(headers)
        try:
            if method=='get':
                response = requests.get(self.get_url(url))
            else:
                file_obj = {"file": (filename, open(filename, "rb"))}
                response = requests.post(self.get_url(url),headers=headers, data=datas,files=file_obj)
                if response.status_code == 200:
                    self.log.info('API：%s 上传请求成功！' % url)
                # print(response.status_code)
                # print(response.json())
                # return ujson.loads(response.text)
                return response.json()
        except Exception as e:
            self.log.info('API：%s 请求失败！错误：%s' %(url,e))


def request_create_report(tjbh,filetype='html'):
    url = gol.get_value('api_report_create') %(filetype,tjbh,'BSSA')
    response = requests.post(url)
    if response.status_code == 200:
        print('API：%s 上传请求成功！' % url)
        return response.json()
    else:
        print('API：%s 上传请求失败！' % url)
        return False




if __name__=="__main__":
    from utils.envir import set_env
    from utils import str2
    #sql = "SELECT TJBH FROM TJ_TJDJB WHERE  (del <> '1' or del is null) and QD='1' and SHRQ>='2018-08-25' AND SHRQ<'2018-09-30' AND SUMOVER='1'; "
    # 处理遗漏的
    # sql = "SELECT TJBH FROM TJ_TJDJB WHERE SUMOVER='1' AND SHRQ>='2018-09-01' AND QD='1' AND (del <> '1' or del is null) AND TJBH NOT IN (SELECT TJBH FROM TJ_BGGL WHERE BGZT<>'0')"
    # # 处理PDF 生成的
    # # sql = "SELECT TJBH FROM TJ_BGGL WHERE SYRQ>='2018-09-28'"
    # #sql = "SELECT TJBH FROM TJ_TJDJB WHERE SUMOVER='1' AND SHRQ>='2018-09-01' AND dybj IS NULL AND (del <> '1' or del is null) AND tjqy IN ('1','2','3','4')  "
    set_env()
    # # # 网络打印
    # #
    session = gol.get_value('tjxt_session_local')
    # # sql = "select jy from tj_tjdjb where tjbh='%s';" % '165582991'
    # # results = session.execute(sql).fetchall()
    # # print(str2(results[0][0]))
    # # raise
    # # 招工自动审阅完成 生成PDF
    #sql = "SELECT TJ_BGGL.TJBH FROM TJ_BGGL INNER JOIN TJ_TJDJB ON TJ_BGGL.TJBH=TJ_TJDJB.TJBH AND TJ_BGGL.bgzt='1' AND TJ_TJDJB.zhaogong='1' AND TJ_TJDJB.TJLX='1' " \
    #sql = "SELECT TJBH FROM TJ_TJDJB WHERE SHRQ>='2018-07-01' AND SHRQ<'2018-07-10' AND SUMOVER='1' AND zhaogong='0'  AND (del <> '1' or del is null);"
    sql = "SELECT TJBH FROM TJ_TJDJB WHERE SHRQ>='2018-07-18' AND SHRQ<'2018-08-01' AND SUMOVER='1'  AND (del <> '1' or del is null) " \
          "AND TJBH NOT IN (SELECT TJBH FROM TJ_BGGL WHERE SHRQ>='2018-07-18' AND SHRQ<'2018-08-01'); "
    results = session.execute(sql).fetchall()
    for result in results:
        request_create_report(result[0], 'pdf')
        #request_create_report(result[0], 'pdf')
    #print(get_barcode_wx('测试5','330227199902040663','13736093866'))
    # request_create_report('176570130','pdf')
    #request_post_wx()
