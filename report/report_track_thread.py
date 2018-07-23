from PyQt5.QtCore import QThread,pyqtSignal
from utils import gol
from report.model import *


# 获取PACS 结果
class PacsResultThread(QThread):
    # 定义信号,定义参数为str类型
    signalConnFail = pyqtSignal(bool,str)   # 连接失败
    signalPost = pyqtSignal(list)           # 更新界面
    signalExit = pyqtSignal()
    tjbh = None

    def __init__(self):
        super(PacsResultThread, self).__init__()
        self.session = gol.get_value('pis_session')

    def stop(self):
        self.running = False

    def setStart(self,tjbh):
        self.running = True
        self.tjbh = tjbh

    def run(self):
        while self.running:
            if self.tjbh:
                result = self.session.execute(get_pis_sql(self.tjbh)).fetchall()
                self.signalPost.emit(result)
            else:
                pass
            self.running = False

