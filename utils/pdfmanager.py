from PyPDF2.pdf import PdfFileReader, PdfFileWriter
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import re,os,shutil
from utils import gol

# PDF转换文本
def pdf2txt(filename):

    file = open(filename, 'rb')             #  以二进制读模式打开
    praser = PDFParser(file)                #  用文件对象来创建一个pdf文档分析器
    doc = PDFDocument()                     #  创建一个PDF文档
    praser.set_document(doc)                #  连接分析器 与文档对象
    doc.set_parser(praser)
    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    # 创建PDf 资源管理器 来管理共享资源
    rsrcmgr = PDFResourceManager()
    # 创建一个PDF设备对象
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # 创建一个PDF解释器对象
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pdfStrList = []
    # 循环遍历列表，每次处理一个page的内容
    for page in doc.get_pages():            # doc.get_pages() 获取page列表
        interpreter.process_page(page)
        # 接受该页面的LTPage对象
        layout = device.get_result()
        for x in layout:
            if hasattr(x, "get_text"):
                pdfStrList.append(x.get_text())
            else:
                pass
    return pdfStrList

def parse(filename,file_type,regular=None):

    if file_type == '01': # 电测听
        pass
    elif file_type == '04':  # 骨密度
        for i,value in enumerate(pdf2txt(filename)):
            if i==5:
                tmp = value.split('\n')[0]
                if len(tmp) == 9 and tmp.isdigit():
                    try:
                        tjbh = tmp
                        jcys = value.split('\n')[1]
                        jcrq = value.split('\n')[2]
                        print(tjbh,jcys,jcrq)
                    except Exception as e:
                        print('文件：%s 解析错误，错误信息：%s' %(filename,e))
                        shutil.copy2(filename, os.path.join(r'E:\PDF-\04\error', os.path.basename(filename)))
                        os.remove(filename)
                else:
                    shutil.copy2(filename, os.path.join(r'E:\PDF-\04\tmp',os.path.basename(filename)))
                    os.remove(filename)
    else:
        pass

#解析PDF
class CPdf2TxtManager():

    def __init__(self):
        '''''
        Constructor
        '''

    def parse(self, filename,equip_type):
        file = open(filename, 'rb')             #  以二进制读模式打开
        praser = PDFParser(file)                #  用文件对象来创建一个pdf文档分析器
        doc = PDFDocument()                     #  创建一个PDF文档
        praser.set_document(doc)                #  连接分析器 与文档对象
        doc.set_parser(praser)
        # 提供初始化密码
        # 如果没有密码 就创建一个空的字符串
        doc.initialize()
        # 检测文档是否提供txt转换，不提供就忽略
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pdfStrList = []
        pdfinfo={"tjbh":'',"file":'','xm':'',"jcrq":'',"jcys":''}
        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages():            # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            for x in layout:
                if hasattr(x, "get_text"):
                    pdfStrList.append(x.get_text())
                else:
                    pass

        if equip_type=='01':
            try:
                if int(pdfStrList[0][0:9]):
                    pdfinfo["tjbh"]=pdfStrList[0][0:9]
                    pdfinfo["file"] = pdfStrList[0][0:9] + "_01.pdf"
                    pdfinfo["jcrq"]=''
            except Exception as e:
                try:
                    if int(pdfStrList[1][0:9]):
                        pdfinfo["tjbh"] = pdfStrList[1][0:9]
                        pdfinfo["file"] = pdfStrList[1][0:9] + "_01.pdf"
                        pdfinfo["jcrq"] = ''
                except Exception as e:
                    pdfinfo["tjbh"] = pdfStrList[3][0:9]
                    pdfinfo["file"] = pdfStrList[3][0:9] + "_01.pdf"
                    pdfinfo["jcrq"] = ''

        elif equip_type == '04':  # 骨密度
            new_string = "".join(pdfStrList)
            print(new_string)
        elif equip_type == '08': # 心电图
            new_string="".join(pdfStrList)
            re_tjbh = re.compile(gol.get_value('regular_tjbh'), re.DOTALL)
            re_xm = re.compile(gol.get_value('regular_xm'), re.DOTALL)
            re_jcrq = re.compile(gol.get_value('regular_jcrq'), re.DOTALL)
            tjbh = re_tjbh.findall(new_string)
            xm = re_xm.findall(new_string)
            jcrq = re_jcrq.findall(new_string)

            if tjbh:
                pdfinfo["tjbh"]=tjbh[0].strip()
                pdfinfo["file"] = tjbh[0].strip() + "_08.pdf"
            else:
                pdfinfo["tjbh"]=''
            if xm:
                pdfinfo["xm"] = xm[0].strip()
            else:
                pdfinfo["xm"]=''
            if jcrq:
                pdfinfo["jcrq"] = jcrq[0].strip()
            else:
                pdfinfo["jcrq"] = ''

        else:
            print("设备类型：%s，暂不支持解析，请联系管理员！" %gol.get_value('equip_type','00'))


        if gol.get_value('system_debug',0):
            print("文件%s  原格式：\n%s\n" %(filename,pdfStrList))
            print("文件%s解析格式：\n%s\n" %(filename,pdfinfo))


        return pdfinfo


#读取PDF并进行剪切
class ReadPdf(object):

    def __init__(self,in_file):
        self.pdf_read = PdfFileReader(open(in_file, 'rb'))
        self.pdf_write = PdfFileWriter()

    def parse(self,out_file,type):
        for page in self.pdf_read.pages:

            if type=='01':
                # 电测听 剪切方案
                pass
                # page.mediaBox.setUpperLeft((0,606))
                # page.mediaBox.setUpperRight((595,606))
                # page.mediaBox.setLowerLeft((0,0))
                # page.mediaBox.setLowerRight((595,0))
            elif type=='02':
                # 人体成分(投放) 剪切方案
                page.mediaBox.setUpperLeft((0, 765))
                page.mediaBox.setUpperRight((595, 765))
                page.mediaBox.setLowerLeft((0, 22))
                page.mediaBox.setLowerRight((595, 22))
            elif type=='03':
                pass

            elif type=='04':
                # 骨密度 剪切方案
                page.mediaBox.setUpperLeft((0, 860))
                page.mediaBox.setUpperRight((595, 860))
                page.mediaBox.setLowerLeft((0, 80))
                page.mediaBox.setLowerRight((595, 80))

            elif type=='05':
                # #超声骨密度 剪切方案
                page.mediaBox.setUpperLeft((0, 842))
                page.mediaBox.setUpperRight((595, 842))
                page.mediaBox.setLowerLeft((0, 35))
                page.mediaBox.setLowerRight((595, 35))

            else:
                pass

            self.pdf_write.addPage(page)

        ous = open(out_file, 'wb')
        self.pdf_write.write(ous)
        ous.close()


# 初始化-查找文件
def fileiter(root_path):
    for root, dirs, files in os.walk(root_path):
        if files and not dirs:  # 必须是指定目录的下级目录
            for file in files:
                yield os.path.join(root, file), file

if __name__=="__main__":
    dir = r'E:\PDF-\04\create'
    for filename,_ in fileiter(dir):
        parse(filename,'04')
            # if i.isdigit():
            #     print(i)