'''
	功能：利用百度官方api，读取图片中的文字，同时将文字转换成语音
'''
from aip import AipOcr,AipSpeech
from functools import reduce

class BaiDuAPI(object):

    # """ 你的 APPID AK SK """
    APP_ID = '14238273'
    API_KEY = 'Wie6KuTOYulYblTEITKdeQAv'
    SECRET_KEY = 'XPqD1IuqnQ5QOUFdMLDkqyU0rySfwdet'

    def __init__(self):
        self.client_AipOcr = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        # 语音识别
        #self.client_AipSpeech = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def pic2txt(self, filename):
        '''根据图像识别文字'''
        image = self.getPictuer(filename)
        texts = self.client_AipOcr.basicGeneral(image)
        return texts

    @staticmethod
    def getPictuer(filename):
        with open(filename, 'rb') as fp:
            return fp.read()

    # 解析体检编号
    def get_tjbh(self,filename):
        texts = self.pic2txt(filename)
        comtent = reduce(lambda x, y: x + y, [words['words'] for words in texts['words_result']])
        re_tjbh = re.compile(r"D\|?(\d{9})", re.DOTALL)
        tjbhs = re_tjbh.findall(comtent)
        if tjbhs:
            return tjbhs[0]
        else:
            return ''





if __name__ == '__main__':
    # demo 测试
    baiduapi = BaiDuAPI()
    import glob,re
    from utils.api import get_ocr
    filenames = glob.glob(r'E:\PDF-\03\*.png')
    for filename in filenames:
        print(get_ocr(filename))

        # texts = baiduapi.pic2txt(filename)
        # comtent = reduce(lambda x, y: x + y, [words['words'] for words in texts['words_result']])
        # print(comtent)
        # re_tjbh = re.compile(r"D\|?(\d{9})", re.DOTALL)
        # tjbhs = re_tjbh.findall(comtent)
        # tjbh =tjbhs[0]