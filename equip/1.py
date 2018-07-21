import PyPDF2, os, openpyxl, sys, time, threading
from openpyxl.cell import *

# 测试的pdf提取文档
pdf_test = "document.pdf"


def single_Pdf_extract(filename):
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pages = pdfReader.numPages  # 显示页数 在第4100行时读取pdfReader也会出错
    if pages > 30:
        pages = 30

    # pageObj=pdfReader.getPage(0) #读取第一页的字符,第一页可读取
    # content=pageObj.extractText() #输出第一页字符
    # 页面写入
    content = ""
    for page in range(pages):
        pageObj = pdfReader.getPage(page)  # 读取第一页的字符,第一页可读取
        content += pageObj.extractText()  # 输出第一页字符
        print("识别出的内容：%s" %content)
    pdfFileObj.close()
    return content


content = single_Pdf_extract(pdf_test)
