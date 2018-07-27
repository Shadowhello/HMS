from PyPDF2.pdf import PdfFileReader, PdfFileWriter
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import re,os,shutil,time
from utils import gol
from wand.image import Image

def cur_datetime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

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

# 字符串解析
def txtparse(filename,file_type,regular=None,error_path='D:/'):
    info = {}
    # 电测听
    if file_type == '01':
        pdfStrList = pdf2txt(filename)
        try:
            if pdfStrList[0][0:9].isdigit():
                info["patient"] = ''
                info["tjbh"] = pdfStrList[0][0:9]
                info["file"] = pdfStrList[0][0:9] + "_01.pdf"
                info["operate_time"] = date_format(pdfStrList[2].split('\n')[0][1:])
            elif pdfStrList[1][0:9].isdigit():
                info["patient"] = pdfStrList[0].split('\n')[0].strip()
                info["tjbh"] = pdfStrList[1][0:9]
                info["file"] = pdfStrList[1][0:9] + "_01.pdf"
                info["operate_time"] = date_format(pdfStrList[3].split('\n')[0][5:])
            elif pdfStrList[3][0:9].isdigit():
                info["patient"] = ''
                info["tjbh"] = pdfStrList[3][0:9]
                info["file"] = pdfStrList[3][0:9] + "_01.pdf"
                info["operate_time"] = date_format(pdfStrList[5].split('\n')[0][1:])
            else:
                shutil.copy2(filename, os.path.join(error_path, os.path.basename(filename)))
        except Exception as e:
            shutil.copy2(filename, os.path.join(error_path, os.path.basename(filename)))
            print(e)
            info["patient"] = ''
            info["tjbh"] = ''
            info["file"] = ''
            info["operate_time"] = ''


    elif file_type == '04':     # 骨密度

        pdfStrList = pdf2txt(filename)
        if pdfStrList[3][0:9].isdigit():
            ######## 体检编号 ######################
            tjbh = pdfStrList[3][0:9]
            ######## 姓名 ######################
            try:
                xm = pdfStrList[1].split('\n')[0].replace(', ','')
            except Exception as e:
                xm = ''
            ######## 检查日期 ######################
            try:
                tmp_tjbh = pdfStrList[3].split('\n')
                if len(tmp_tjbh) == 5:
                    jcrq = tmp_tjbh[2] + ' ' + tmp_tjbh[3]
                else:
                    jcrq = cur_datetime()
            except Exception as e:
                jcrq = cur_datetime()

        elif pdfStrList[4][0:9].isdigit():
            ######## 体检编号 ######################
            tjbh = pdfStrList[4][0:9]
            ######## 姓名 ######################
            try:
                xm = pdfStrList[1].split('\n')[0].replace(', ','')
            except Exception as e:
                xm = ''
            ######## 检查日期 ######################
            try:
                tmp_tjbh = pdfStrList[4].split('\n')
                if len(tmp_tjbh) == 5:
                    jcrq = tmp_tjbh[2] + ' ' + pdfStrList[3].split('\n')[0]
                else:
                    jcrq = cur_datetime()
            except Exception as e:
                jcrq = cur_datetime()
            #print(xm, tjbh, jcrq)

        elif pdfStrList[5][0:9].isdigit():
            ######## 体检编号 ######################
            tjbh = pdfStrList[5][0:9]
            ######## 姓名 ######################
            try:
                xm = pdfStrList[3].split('\n')[0].replace(', ','')
            except Exception as e:
                xm = ''
            ######## 检查日期 ######################
            try:
                tmp_tjbh = pdfStrList[5].split('\n')
                if len(tmp_tjbh) == 2:
                    tmp_jcrq = pdfStrList[6].split('\n')
                    if len(tmp_jcrq) == 3:
                        jcrq = pdfStrList[6].split('\n')[0] + ' ' + pdfStrList[7].split('\n')[0]
                    elif len(tmp_jcrq) == 4:
                        jcrq = tmp_jcrq[0] + ' ' + tmp_jcrq[1]
                    else:
                        jcrq = cur_datetime()
                elif len(tmp_tjbh) == 5:
                    jcrq = tmp_tjbh[2] + ' ' + pdfStrList[6].split('\n')[0]
                else:
                    jcrq = cur_datetime()
            except Exception as e:
                jcrq = cur_datetime()
            # print(pdfStrList)
            # print(xm,tjbh,jcrq)

        elif pdfStrList[6][0:9].isdigit():
            ######## 体检编号 ######################
            tjbh = pdfStrList[6][0:9]
            ######## 姓名 ######################
            try:
                xm = pdfStrList[3].split('\n')[0].replace(', ','')
            except Exception as e:
                xm = ''
            ######## 检查日期 ######################
            try:
                tmp_tjbh = pdfStrList[6].split('\n')
                if len(tmp_tjbh) == 2:
                    tmp_jcrq = pdfStrList[6].split('\n')
                    if len(tmp_jcrq) == 3:
                        jcrq = pdfStrList[6].split('\n')[0] + ' ' + pdfStrList[7].split('\n')[0]
                    elif len(tmp_jcrq) == 4:
                        jcrq = tmp_jcrq[0] + ' ' + tmp_jcrq[1]
                    else:
                        jcrq = cur_datetime()
                elif len(tmp_tjbh) == 5:
                    jcrq = tmp_tjbh[2] + ' ' + pdfStrList[6].split('\n')[0]
                else:
                    jcrq = cur_datetime()
            except Exception as e:
                jcrq = cur_datetime()
            # print(pdfStrList)
            # print(xm,tjbh,jcrq)

        elif pdfStrList[7][0:9].isdigit():
            ######## 体检编号 ######################
            tjbh = pdfStrList[7][0:9]
            ######## 姓名 ######################
            try:
                xm = pdfStrList[3].split('\n')[0].replace(', ','')
            except Exception as e:
                xm = ''
            ######## 检查日期 ######################
            try:
                tmp_tjbh = pdfStrList[7].split('\n')
                if len(tmp_tjbh) == 5:
                    jcrq = tmp_tjbh[2] + ' ' + pdfStrList[9].split('\n')[0]
                else:
                    jcrq = cur_datetime()
            except Exception as e:
                jcrq = cur_datetime()

        elif pdfStrList[18][0:9].isdigit():
            ######## 体检编号 ######################
            tjbh = pdfStrList[18][0:9]
            ######## 姓名 ######################
            try:
                xm = pdfStrList[3].split('\n')[0].replace(', ','')
            except Exception as e:
                xm = ''
            ######## 检查日期 ######################
            try:
                tmp_tjbh = pdfStrList[18].split('\n')
                if len(tmp_tjbh) == 5:
                    jcrq = tmp_tjbh[2] + ' ' + pdfStrList[20].split('\n')[0]
                elif len(tmp_tjbh) == 6:
                    jcrq = tmp_tjbh[2] + ' ' + tmp_tjbh[3]
                else:
                    jcrq = cur_datetime()
                    print(len(tmp_tjbh),tmp_tjbh)
            except Exception as e:
                jcrq = cur_datetime()

        else:
            print('无法解析的文件：%s' %filename)
            print(pdfStrList)
            xm =''
            tjbh = ''
            jcrq = ''

        info["patient"] = xm
        info["tjbh"] = tjbh
        info["file"] =  "%s_04.pdf" %tjbh
        info["operate_time"] = jcrq

        # for i,value in enumerate(pdf2txt(filename)):

        #         tmp = value.split('\n')[0]
        #         if len(tmp) == 9 and tmp.isdigit():
        #             try:
        #                 tjbh = tmp
        #                 jcys = value.split('\n')[1]
        #                 jcrq = value.split('\n')[2]
        #                 print(tjbh,jcys,jcrq)
        #             except Exception as e:
        #                 print('文件：%s 解析错误，错误信息：%s' %(filename,e))
        #                 shutil.copy2(filename, os.path.join(r'E:\PDF-\04\error', os.path.basename(filename)))
        #                 os.remove(filename)
        #         else:
        #             shutil.copy2(filename, os.path.join(r'E:\PDF-\04\tmp',os.path.basename(filename)))
        #             os.remove(filename)

    elif file_type == '08':
        # 心电图
        new_string = "".join(pdf2txt(filename))
        re_tjbh = re.compile(gol.get_value('regular_tjbh'), re.DOTALL)
        re_xm = re.compile(gol.get_value('regular_xm'), re.DOTALL)
        re_jcrq = re.compile(gol.get_value('regular_jcrq'), re.DOTALL)
        tjbh = re_tjbh.findall(new_string)
        xm = re_xm.findall(new_string)
        jcrq = re_jcrq.findall(new_string)

        if tjbh:
            info["tjbh"] = tjbh[0].strip()
            info["file"] = tjbh[0].strip() + "_08.pdf"
        else:
            info["tjbh"] = ''
        if xm:
            info["patient"] = xm[0].strip()
        else:
            info["patient"] = ''
        if jcrq:
            info["operate_time"] = jcrq[0].strip()
        else:
            info["operate_time"] = cur_datetime()

    else:
        pass

    return info


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


def pdf2pic(pdf):
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
    new_file = str(os.path.splitext(pdf)[0]) + '.png'
    for img in req_image:
        ff = open(new_file, 'wb')
        ff.write(img)
        ff.close()
        i += 1

    return new_file


# 初始化-查找文件
def fileiter(root_path):
    for root, dirs, files in os.walk(root_path):
        if files and not dirs:  # 必须是指定目录的下级目录
            for file in files:
                yield os.path.join(root, file), file
# '2018/1/28'
# '2017/12/23'
def date_format(date_str):
    tmp = date_str.split('/')
    return tmp[0]+'-'+tmp[1].zfill(2)+'-'+tmp[2].zfill(2)+' 00.00.00'

if __name__=="__main__":
    dir = r'E:\PDF-\04\create'
    for filename,_ in fileiter(dir):
        print(txtparse(filename,'04'))
            # if i.isdigit():
            #     print(i)