from zeep import Client
import zeep,json,base64,os

# 胶片打印服务
def webservice_film():
    url = "http://10.8.200.24/FilmService/WebFilmService.asmx?WSDL"
    client = zeep.Client(url)
    # 获取打印机列表
    result = client.service.GetPrinters()
    # 根据检查号获取胶片
    #result2 = client.service.GetFilmByAccessno(110016983684)
    #打印出结果
    print(result)


# PACS 图像服务
def webservice_pacs(tjbh,xmbh,path):
    url = "http://10.8.200.220:7059/WebGetFileView.asmx?WSDL"
    client = zeep.Client(url)
    result = json.loads(client.service.f_GetUISFilesByTJ_IID(tjbh+xmbh))
    filenames = []
    if result['IsSuccess']=='true':
        pic_datas = result['Datas']
        count = 0
        for pic_data in pic_datas:
            count = count + 1
            filename = os.path.join(path,'%s_%s_%s.jpg' %(tjbh,xmbh,count))
            with open(filename,"wb") as f:
                f.write(base64.b64decode(pic_data))
            filenames.append(filename)

    return filenames

if __name__ == '__main__':
    webservice_film()