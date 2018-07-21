import  win32api
import win32print




print('获得系统默认打印机名称：%s' %win32print.GetDefaultPrinter())    # 获得str
print('获得系统默认打印机名称：%s' %win32print.GetDefaultPrinterW())   # 获得unicode
# print('获得指定打印机打开句柄：%s' %win32print.OpenPrinter(win32print.GetDefaultPrinter()))
# print('获得指定打印机有关信息：%s' %win32print.ClosePrinter(win32print.GetDefaultPrinter()))

filename = r'F:\HMS\utils\165560254_04.pdf'
try:
    win32api.ShellExecute(0, 'print', filename, win32print.GetDefaultPrinter(), '.', 0)
except Exception as e:
    print('打印失败！错粗信息：%s \n 处理方式：请安装PDF阅读器 AcroRd32.exe 并设置为默认打开方式。')

from widgets.bwidget import *



