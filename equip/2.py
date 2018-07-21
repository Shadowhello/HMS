import io
from wand.image import Image
from wand.color import Color
from PyPDF2 import PdfFileReader, PdfFileWriter

memo = {}

def getPdfReader(filename):
    reader = memo.get(filename, None)
    if reader is None:
        reader = PdfFileReader(filename, strict=False)
        memo[filename] = reader
    return reader

def run_convert(filename, page, res=300):
    idx = page + 1
    pdfile = getPdfReader(filename)
    pageObj = pdfile.getPage(page)
    dst_pdf = PdfFileWriter()
    dst_pdf.addPage(pageObj)

    pdf_bytes = io.BytesIO()
    dst_pdf.write(pdf_bytes)
    pdf_bytes.seek(0)

    img = Image(file=pdf_bytes, resolution=res)
    img.format = 'jpg'
    img.compression_quality = 300
    # img.background_color = Color("white")
    img_path = '%s%d.jpg' % (filename[:filename.rindex('.')], idx)
    img.save(filename=img_path)
    img.destroy()


if __name__=="__main__":
    run_convert("165560254_04.pdf",0)