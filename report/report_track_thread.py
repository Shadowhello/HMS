from PyQt5.QtCore import QThread,pyqtSignal
from utils import gol
from report.model import *

# 获取PES 体检结果
class PesResultThread(QThread):
    # 定义信号,定义参数为str类型
    signalConnFail = pyqtSignal(bool,str)   # 连接失败
    signalPost = pyqtSignal(str,list)           # 更新界面
    signalExit = pyqtSignal()
    tjbh = None

    def __init__(self):
        super(PesResultThread, self).__init__()
        self.session = gol.get_value('tjxt_session_thread')
        self.running = False

    def stop(self):
        self.running = False

    def setStart(self,tjbh):
        self.running = True
        self.tjbh = tjbh

    def run(self):
        while self.running:
            if self.tjbh:
                result = self.session.execute(get_pis_sql(self.tjbh)).fetchall()
                self.signalPost.emit('PES',result)
            else:
                pass
            self.running = False

# 获取PIS 结果
class PisResultThread(QThread):
    # 定义信号,定义参数为str类型
    signalConnFail = pyqtSignal(bool,str)   # 连接失败
    signalPost = pyqtSignal(str,list)           # 更新界面
    signalExit = pyqtSignal()
    tjbh = None

    def __init__(self):
        super(PisResultThread, self).__init__()
        self.session = gol.get_value('pis_session')
        self.running = False

    def stop(self):
        self.running = False

    def setStart(self,tjbh):
        self.running = True
        self.tjbh = tjbh

    def run(self):
        while self.running:
            if self.tjbh:
                result = self.session.execute(get_pis_sql(self.tjbh)).fetchall()
                self.signalPost.emit('PIS',result)
            else:
                pass
            self.running = False

# 获取PACS 结果
class PacsResultThread(QThread):

    # 定义信号,定义参数为str类型
    signalConnFail = pyqtSignal(bool,str)   # 连接失败
    signalPost = pyqtSignal(str,list)           # 更新界面
    signalExit = pyqtSignal()
    tjbh = None

    def __init__(self):
        super(PacsResultThread, self).__init__()
        self.session = gol.get_value('pacs_session')
        self.running = False

    def stop(self):
        self.running = False

    def setStart(self,tjbh):
        self.running = True
        self.tjbh = tjbh

    def run(self):
        while self.running:
            if self.tjbh:
                result = self.session.execute(get_pacs_sql(self.tjbh)).fetchall()
                self.signalPost.emit('PACS',result)
            else:
                pass
            self.running = False

# 获取LIS 结果
class LisResultThread(QThread):

    # 定义信号,定义参数为str类型
    signalConnFail = pyqtSignal(bool,str)       # 连接失败
    signalPost = pyqtSignal(str,dict)           # 更新界面
    signalExit = pyqtSignal()
    tjbh = None

    def __init__(self):
        super(LisResultThread, self).__init__()
        self.session_pes = gol.get_value('tjxt_session_thread')
        self.session_lis = gol.get_value('lis_session')
        self.running = False

    def stop(self):
        self.running = False

    def setStart(self,tjbh):
        self.running = True
        self.tjbh = tjbh

    def run(self):
        while self.running:
            if self.tjbh:
                result = {}
                result_pes = self.session_pes.execute(get_pes_sql(self.tjbh)).fetchall()
                result_lis = self.session_lis.execute(get_lis_sql(self.tjbh)).fetchall()
                result['lis'] = list2dict(result_lis)
                result['pes'] = result_pes
                self.signalPost.emit('LIS',result)
            else:
                pass
            self.running = False

#
def list2dict(results:list):
    new_results = {}
    for result in results:
        if result[0] not in list(new_results.keys()):
            # 字典无此key，说明还未有数据，初始化列表
            new_results[result[0]] = []
        new_results[result[0]].append(result[1:])
    return new_results
