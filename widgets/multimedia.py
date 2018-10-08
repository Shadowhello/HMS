from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from widgets.bwidget import *


class Camera(QWidget):

    def __init__(self,parent=None):
        super(Camera,self).__init__(parent)
        self.initUI()
        self.initParas()
        self.cb_camera_selector.currentIndexChanged.connect(self.on_camera_select)
        self.btn_stop.clicked.connect(self.on_camera_stop)
        self.btn_start.clicked.connect(self.on_camera_start)
        self.btn_take.clicked.connect(self.on_camera_take)
        # 特殊变量

    def initUI(self):

        lt_main = QVBoxLayout()
        # 摄像头 展示
        lt_top = QHBoxLayout()
        gp_top = QGroupBox('摄像头')
        # 设置取景器
        self.viewfinder = QCameraViewfinder()
        self.viewfinder.show()
        lt_top.addWidget(self.viewfinder)
        lt_top.addStretch()
        gp_top.setLayout(lt_top)
        # 摄像头 社遏制
        lt_middle = QHBoxLayout()
        gp_middle  = QGroupBox('设置')
        self.cb_camera_selector = QComboBox()
        self.cb_camera_degree = QComboBox()
        self.cb_camera_degree.addItems(['0','90','180','270'])
        lt_middle.addWidget(QLabel("切换摄像头："))
        lt_middle.addWidget(self.cb_camera_selector)
        lt_middle.addWidget(QLabel("旋转角度："))
        lt_middle.addWidget(self.cb_camera_degree)
        lt_middle.addStretch()
        gp_middle.setLayout(lt_middle)

        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox('功能栏')
        self.btn_start = QPushButton(Icon('启动'), '启动')
        self.btn_stop = QPushButton(Icon('停止'), '停止')
        self.btn_take = QPushButton(Icon('拍照'), '拍照')
        lt_bottom.addWidget(self.btn_start)
        lt_bottom.addWidget(self.btn_stop)
        lt_bottom.addWidget(self.btn_take)
        lt_bottom.addStretch()
        gp_bottom.setLayout(lt_bottom)
        # 添加布局
        lt_main.addWidget(gp_top)
        lt_main.addWidget(gp_middle)
        lt_main.addWidget(gp_bottom)
        self.setLayout(lt_main)

    def initParas(self):
        self.cb_camera_selector.addItems([QCamera.deviceDescription(c) for c in QCamera.availableDevices()])
        self.camera_objs = QCameraInfo.availableCameras()

        # 打开默认的摄像头
        self.on_camera_select(0)
        self.set_image = QImageEncoderSettings()
        self.set_audio = QAudioEncoderSettings()
        self.set_video = QVideoEncoderSettings()

    # 选择摄像头
    def on_camera_select(self, i):
        self.cur_camera_name = self.cb_camera_selector.currentText()
        self.camera = QCamera(self.camera_objs[i])
        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
        self.save_seq = 0
        self.on_camera_start()

        self.capture = QCameraImageCapture(self.camera)
        self.capture.error.connect(lambda i, e, s: self.alert(s))


    # 拍照
    def on_camera_take(self,filename=None):
        if filename:
            pass
        else:
            self.viewfinder.setContrast(100)
            timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
            self.capture.capture(os.path.join("d:/", "%s-%04d-%s.jpg" % (
                self.cur_camera_name,
                self.save_seq,
                timestamp
            )))
            self.save_seq += 1

    # 开始
    def on_camera_start(self):
        self.camera.start()
        self.btn_start.setDisabled(True)
        self.btn_stop.setDisabled(False)

    # 停止
    def on_camera_stop(self):
        self.camera.stop()
        self.btn_start.setDisabled(False)
        self.btn_stop.setDisabled(True)

    def alert(self, mes):
        """
        Handle errors coming from QCamera dn QCameraImageCapture by displaying alerts.
        """
        err = QErrorMessage(self)
        err.showMessage(mes)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui=Camera()
    ui.show()
    app.exec_()
    # print(QCameraInfo().defaultCamera())

    # QImageEncoderSettings
    # for device_obj in QCamera.availableDevices():
    #     camera_name = QCamera.deviceDescription(device_obj)
    #     print(QCamera.supportedViewfinderResolutions())
    #     print(camera_name)
