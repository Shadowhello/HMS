from zeep import Client
import zeep

url = "http://10.8.200.24/FilmService/WebFilmService.asmx?WSDL"
client = zeep.Client(url)
# 获取打印机列表
#result = client.service.GetPrinters()
# 根据检查号获取胶片
result2 = client.service.GetFilmByAccessno(110016983684)

#打印出结果
print(result2)