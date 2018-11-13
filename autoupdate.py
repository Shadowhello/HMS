from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt,QThread,pyqtSignal,QTimer,QProcess
from PyQt5.QtGui import *
import requests,os,platform,sys,zipfile,logging
from utils import config_parse
from importlib import import_module
from configobj import ConfigObj

class AutoUpdateUI(QWidget):

    '''
    # 1、请求新版本：本地版本、系统类型
    # 2、下载压缩包 到临时目录
    # 3、删除本地重复文件
    # 4、解压缩
    # 5、退出本程序
    # 6、启动主程序
    # 7、更新本地版本号
    '''

    def __init__(self,paras):
        super(AutoUpdateUI,self).__init__()
        self.setWindowIcon(Icon('mztj'))
        self.setWindowTitle('明州体检')
        self.setFixedSize(500,400)
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 窗口模式，去掉标题栏
        self.initUI()
        self.setBackgroundImage()
        self.setParas(paras)
        if self.system_name:
            system = self.system_name
        else:
            system = get_system()
        response = requests.get(self.update_url %(system,self.sys_version))
        if response.status_code == 200:
            describe = response.json()['describe']
            self.version = response.json()['version']
            self.gp_top.setTitle('版本V%s：更新内容' %str(self.version))
            self.on_describe_show(self.version,'；\r\n'.join(describe.split('；')))
            self.on_pb_progress_start()
        else:
            mes_about(self,'已是最新版本')
            self.close()

    def initUI(self):
        lt_main = QVBoxLayout()
        ######## 更新内容 #########################
        self.gp_top = QGroupBox('更新内容')
        lt_top = QHBoxLayout()
        self.tb_up_describe = QTextBrowser()
        self.tb_up_describe.setStyleSheet('''font: 75 12pt '微软雅黑';color: rgb(0,128,0);''')
        lt_top.addWidget(self.tb_up_describe)
        self.gp_top.setLayout(lt_top)
        ########进度条############################
        lt_bottom = QHBoxLayout()
        self.gp_bottom = QGroupBox('更新进度')
        self.pb_progress=QProgressBar()
        self.pb_progress.setMinimum(0)
        self.pb_progress.setValue(0)
        lt_bottom.addWidget(self.pb_progress)
        self.gp_bottom.setLayout(lt_bottom)
        # 添加布局
        lt_main.addWidget(self.gp_top)
        lt_main.addWidget(self.gp_bottom)
        self.setLayout(lt_main)

    def setBackgroundImage(self):
        palette=QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(file_ico("17_big.png"))))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def setParas(self,paras:dict):
        self.sys_version = paras.get('system_version',1.0)
        self.system_name = paras.get('system_platform',None)
        self.update_url = paras.get('system_update',"http://10.7.200.101:4009/api/version/%s/%s")
        self.update_down_url = paras.get('system_update_down', "http://10.7.200.101:4009/api/version_file/%s/%s")

    def on_pb_progress_start(self):
        self.update_thread = AutoUpdateThread()
        self.update_thread.setParas(self.sys_version,self.update_down_url)
        self.update_thread.signalDes.connect(self.on_describe_show, type=Qt.QueuedConnection)
        self.update_thread.signalCurNum.connect(self.on_pb_progress_show, type=Qt.QueuedConnection)
        self.update_thread.signalMaxNum.connect(self.set_progress_value, type=Qt.QueuedConnection)
        self.update_thread.signalCur.connect(self.on_mes_show, type=Qt.QueuedConnection)
        self.update_thread.signalExit.connect(self.on_thread_exit, type=Qt.QueuedConnection)
        self.update_thread.start()

    # 重新刷新进度条
    def set_progress_value(self,value):
        self.pb_progress.setMaximum(value)
        self.pb_progress.setValue(0)

    # 显示更新内容
    def on_describe_show(self,version,describe):
        self.tb_up_describe.setPlainText(describe)

    #
    def on_mes_show(self,flag,mes):
        self.gp_bottom.setTitle(mes)

    # 进度条
    def on_pb_progress_show(self,value):
        self.pb_progress.setValue(value)
        # 刷新进度条
        dProgress = (self.pb_progress.value() - self.pb_progress.minimum()) * 100.0 / (self.pb_progress.maximum() - self.pb_progress.minimum())
        self.pb_progress.setAlignment(Qt.AlignRight | Qt.AlignVCenter) #对齐方式

    def on_thread_exit(self):
        self.update_thread = None
        # 更新版本信息
        update_version(version_name, self.version)
        mes_about(self,'更新完成！')
        self.close()
        # 启动主进程
        # print(main_process_name)
        # process = QProcess()
        # process.start(main_process_name)

# 打印线程
class AutoUpdateThread(QThread):

    signalCur = pyqtSignal(bool,str)        # 处理过程：成功/失败
    signalDes = pyqtSignal(str, str)       # 处理过程：成功/失败
    signalMaxNum = pyqtSignal(int)              # 最大
    signalCurNum = pyqtSignal(int)              # 当前
    signalExit = pyqtSignal()

    def __init__(self):
        super(AutoUpdateThread,self).__init__()
        self.runing = False

    def setParas(self,version,url):
        # 初始化环境变量
        self.version = version
        self.url = url
        self.runing = True

    def stop(self):
        self.runing = False

    def run(self):
        while self.runing:
            url = self.url %(get_system(),self.version)
            self.signalCur.emit(True, '正在下载更新包')
            self.signalMaxNum.emit(10)
            self.signalCurNum.emit(5)
            response = requests.get(url)
            if response.status_code == 200:
                # 本地临时文件是否存在，是则删除
                dirname, name = os.path.split(os.path.abspath(sys.argv[0]))
                filename = os.path.join(dirname,'update.zip')
                if os.path.exists(filename):
                    try:
                        os.remove(filename)
                    except Exception as e:
                        print(e)
                #################### 下载文件 ################################
                with open(filename, "wb") as f:
                    for i, chunk in enumerate(response.iter_content(chunk_size=512)):
                        if chunk:
                            f.write(chunk)
                            if 4< i < 8:
                                self.signalCurNum.emit(i + 1)

                    # f.close()
                self.signalCurNum.emit(10)
                self.signalCur.emit(True, '更新包下载完成！')
                # try:
                #################### 解压文件 ##############################
                try:
                    with zipfile.ZipFile(filename, "r") as zip_obj:
                        file_num = len(zip_obj.namelist())
                        self.signalCur.emit(True, '文件合计（%s）,开始解压缩文件......' % str(file_num))
                        self.signalMaxNum.emit(file_num)
                        for i,obj in enumerate(zip_obj.infolist()):
                            try:
                                zip_obj.extract(obj.filename)
                                self.signalCurNum.emit(i+1)
                            except Exception as e:
                                self.signalCur.emit(False, '%s' % e)
                    #################### 更新本地版本 ##############################
                    self.stop()
                    self.signalCur.emit(True, '更新完成')
                    self.signalExit.emit()
                except Exception as e:
                    self.stop()
                    print(e)
                    return False
            else:
                self.stop()
                self.signalCur.emit(True,'系统已是最新版本！')
                self.signalExit.emit()


class MessageBox(QMessageBox):

    def __init__(self, *args, count=10, **kwargs):
        super(MessageBox, self).__init__(*args, **kwargs)
        self.setWindowTitle('明州体检')
        self.setWindowIcon(Icon('mztj'))
        self.count = count
        self.setStandardButtons(self.Close)  # 关闭按钮
        self.closeBtn = self.button(self.Close)  # 获取关闭按钮
        self.closeBtn.setText('关闭(%s)' % count)
        self._timer = QTimer(self, timeout=self.doCountDown)
        self._timer.start(1000)

    def doCountDown(self):
        self.closeBtn.setText('关闭(%s)' % self.count)
        self.count -= 1
        if self.count <= 0:
            self._timer.stop()
            self.accept()
            self.close()

def mes_about(parent,message):
    MessageBox(parent, text=message).exec_()

def get_system():
    system = platform.platform()
    if 'Windows-7' in system:
        return 'win7'
    else:
        return 'winxp'

class Icon(QIcon):

    def __init__(self,name):
        super(Icon,self).__init__()
        self.addPixmap(QPixmap(file_ico(name)),QIcon.Normal,QIcon.On)

def file_ico(name):
    #print("图标目标：%s" %os.path.join(app_path(r"\resource\image"),name))
    return os.path.join(app_path(r"\resource\image"),name)

def app_path(name):
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    return "%s%s" %(dirname,name)

def update_file():
    return os.path.join(app_path(r'\tmp'),'update.rar')

def str2(para):
    if not para:
        return ''
    else:
        if isinstance(para,str):
            if para.isdigit():           # 是否都是数字
                return para
            else:
                try:
                    return para.encode('latin-1').decode('gbk')
                except Exception as e:
                    # print('%s 转换失败！错误信息：%s' %(para,e))
                    return para
        else:
            return str(para)

def update_version(filename,version):
    config_write(filename, 'system', values = {'version':version})

#写入配置参数
def config_write(file_ini,section,values,code='UTF-8'):
    if not os.path.exists(file_ini):
        # log.info("写入配置文件：%s失败，文件不存在，请检查！" % file_ini)
        return
    config=ConfigObj(file_ini, encoding=code)
    for i, j in values.items():
        config[section][i] = j
    config.write()


if __name__=="__main__":
    import cgitb
    cgitb.enable(logdir="./error/",format="text")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',filename=r"autoupdate.log")
    paras = config_parse('version.ini')
    process = QProcess()
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    main_process_name = os.path.join(dirname,paras.get('main_process_name', 'hms.exe'))
    version_name = os.path.join(dirname, 'version.ini')
    # # 结束主进程
    try:
        # 采用动态模块为解决 打包后关闭和启动exe的问题
        # process.start("taskkill /F /IM %s" %main_process_name)
        module_class = getattr(import_module('update.update2'), 'main_end')
        module_class()
        logging.info("更新程序启动前，关闭主程序！")
    except Exception as e:
        logging.info("更新程序启动前，发生错误：%s" %e)
    app = QApplication(sys.argv)
    ui = AutoUpdateUI(paras)
    ui.show()
    app.exec_()
    # 启动主进程
    print(main_process_name)
    process.start(main_process_name)
    # try:
    #     # 采用动态模块为解决 打包后关闭和启动exe的问题
    #     module_class = getattr(import_module('update.update2'), 'main_start')
    #     module_class()
    #     logging.info("更新完成，关闭更新程序！")
    # except Exception as e:
    #     logging.info("更新完成，启动主程序时，发生错误：%s" % e)
