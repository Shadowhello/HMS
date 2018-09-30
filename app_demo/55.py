from PyPDF2 import PdfFileReader,PdfFileMerger,PdfFileWriter

# filename =r"C:\Users\Administrator\Desktop\pdf测试\149520265.pdf"
# filename_xdt =r"C:\Users\Administrator\Desktop\pdf测试\149520265_08.pdf"
# pdf_read_obj = PdfFileReader(filename)
# pdf_write_obj = PdfFileWriter()
#
# page_num = pdf_read_obj.getNumPages()
# page_last_obj = pdf_read_obj.getPage(page_num-1)
# page_last_obj.rotateClockwise(90)
# pdf_write_obj.addPage(page_last_obj)
# pdf_write_obj.write(open(filename_xdt, 'wb'))


def pdfSplit(pdf_main,pdf_part):
    pdf_read_obj = PdfFileReader(pdf_main)
    pdf_write_obj = PdfFileWriter()
    page_num = pdf_read_obj.getNumPages()
    page_last_obj = pdf_read_obj.getPage(page_num - 1)
    page_last_obj.rotateClockwise(90)
    pdf_write_obj.addPage(page_last_obj)
    pdf_write_obj.write(open(pdf_part, 'wb'))

