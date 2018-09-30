import win32api
import win32print
import subprocess

def print_pdf_acroRd32(filename,printer=None):
    try:
        if printer:
            return win32api.ShellExecute(0, 'print', filename, printer, '.', 0)
        else:
            return win32api.ShellExecute(0, 'print', filename, win32print.GetDefaultPrinter(), '.', 0)
    except Exception as e:
        print('打印失败！错误信息：%s \n 处理方式：请安装PDF阅读器 AcroRd32.exe 并设置为默认打开方式。')
        return False

def print_pdf_gsprint(filename,printer=None,page_end=None):
    if not printer:
        printer = win32print.GetDefaultPrinter()
    if page_end:
        command = r'gsprint -color -printer "%s" %s -from 0 -to %s' % (printer, filename, page_end)
    else:
        command =r'gsprint -color -printer "%s" %s' %(printer,filename)
    try:
        result = subprocess.run(command, shell=True)
        return result.returncode
    except Exception as e:
        result = subprocess.call(command, shell=True)
        return result


if __name__=="__main__":
    #print(win32print.EnumPrinters())
    print(print_pdf_gsprint("D:/155200056.pdf","pdfFactory Pro",11))