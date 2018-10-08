from .model import *
from utils import gol

#在浏览器中打开PDF报告
def get_pdf_url(session,tjbh):
    # 优先打开 新系统生成的
    result = session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).scalar()
    if result:
        filename = os.path.join(result.bglj, '%s.pdf' % tjbh).replace('D:/activefile/', '')
        url = gol.get_value('api_pdf_new_show') % filename
        return url
    else:
        try:
            ora_session = gol.get_value('cxk_session')
            result = ora_session.query(MT_TJ_PDFRUL).filter(MT_TJ_PDFRUL.TJBH == tjbh).scalar()
            if result:
                url = gol.get_value('api_pdf_old_show') % result.PDFURL
                return url
            else:
                return False
        except Exception as e:
            return False