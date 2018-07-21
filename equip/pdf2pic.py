from wand.image import Image
import os

def Pdf2Pic(pdf):

    img_obj = Image(filename=pdf, resolution=300)
    #img_obj.convert('jpg')

    req_image = []
    for img in img_obj.sequence:
        img_page = Image(image=img)
        req_image.append(img_page.make_blob('png'))

    # 遍历req_image,保存为图片文件
    i = 0
    for img in req_image:
        ff = open(str(os.path.splitext(pdf)[0]) + '.png', 'wb')
        ff.write(img)
        ff.close()
        i += 1

if __name__=="__main__":
    Pdf2Pic("165560254_04.pdf")


