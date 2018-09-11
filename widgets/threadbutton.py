from .bwidget import *

# 具有线程功能的查询按钮 用于执行SQL查询等耗时功能
class QueryThreadButton(QPushButton):

    queryClicked = pyqtSignal(bool,list)

    def __init__(self, session, QIcon, name, parent=None):
        super(QueryThreadButton,self).__init__(session, QIcon, name, parent)
        self.session = session
        self.thread = None
        self.clicked.connect(self.execQuery)

    # 启动线程 执行查询
    def execQuery(self,sql):
        if not self.thread:
            self.thread = QueryThread(self.session)
        self.thread.setTask(sql)
        self.thread.signalMes.connect(self.on_mes_show, type=Qt.QueuedConnection)
        self.thread.start()

    def on_mes_show(self,mes:bool,result:list):
        self.queryClicked.emit(mes,result)



# 运行线程
class QueryThread(QThread):

    # 定义信号,定义参数为str类型
    signalMes = pyqtSignal(bool,list)        #成功/失败，任务结果
    signalExit = pyqtSignal()                # 退出线程

    def __init__(self,session):
        super(QueryThread,self).__init__()
        self.runing = False
        self.session = session               # 数据库会话

    def stop(self):
        self.runing = False

    # 启动任务
    def setTask(self,sql:str):
        self.sql =sql
        self.runing = True

    def run(self):
        while self.runing:
            try:
                results = self.session.execute(self.sql).fetchall()
                self.signalMes.emit(True, results)
            except Exception as e:
                self.signalMes.emit(False, [])
            self.stop()


