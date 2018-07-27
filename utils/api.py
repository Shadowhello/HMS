import requests
from pprint import pprint

# 使用装饰器改写
# 提取公共功能

# print(response.status_code)     # 打印状态码
# print(response.url)             # 打印请求url
# print(response.headers)         # 打印头信息
# print(response.cookies)         # 打印cookie信息
# print(response.text)            # 以文本形式打印网页源码
# print(response.content)         # 以字节流形式打印
# print(response.json())          # 同json.loads(response.text)


# get 请求
def request_get(url,save_file=None):
    '''
    :param url:             请求地址
    :param save_file:       下载文件 save_file
    :return:
    '''
    response = requests.get(url)
    if response.status_code==200:
        f = open(save_file, "wb")
        for chunk in response.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        f.close()
        return True
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
