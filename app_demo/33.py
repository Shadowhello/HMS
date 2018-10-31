from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

# QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        f = QFont("ZYSong18030", 12)
        self.setFont(f)

        self.setWindowTitle("Image Processor")
        self.imageLabel = QLabel()
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.setCentralWidget(self.imageLabel)
        self.image = QImage()
        if self.image.load("176380131_501780_2.jpg"):
            self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
            self.resize(self.image.width(), self.image.height())

        self.createActions()
        self.createMenus()
        self.createToolBars()

    def createActions(self):
        self.zoominAction = QAction(QIcon("放大.png"), self.tr("放大"), self)
        self.zoominAction.setShortcut("Ctrl+P")
        self.zoominAction.setStatusTip(self.tr("放大"))
        self.zoominAction.triggered.connect(self.slotZoomin)

        self.deflateAction = QAction(QIcon("缩小.png"), self.tr("缩小"), self)
        self.deflateAction.setShortcut("Ctrl+A")
        self.deflateAction.setStatusTip(self.tr("缩小"))
        self.deflateAction.triggered.connect(self.slotDeflate)

        self.circumgyrate = QAction(QIcon("旋转.png"), self.tr("旋转"), self)
        self.circumgyrate.setShortcut("Ctrl+B")
        self.circumgyrate.setStatusTip(self.tr("旋转"))
        self.circumgyrate.triggered.connect(self.slotCircumgyrate)

    def createMenus(self):
        PrintMenu = self.menuBar().addMenu(self.tr("缩放"))
        PrintMenu.addAction(self.zoominAction)
        PrintMenu.addAction(self.deflateAction)
        circumgyrateMenu = self.menuBar().addMenu(self.tr("旋转"))
        circumgyrateMenu.addAction(self.circumgyrate)

    def createToolBars(self):
        fileToolBar = self.addToolBar("Print")
        fileToolBar.addAction(self.zoominAction)
        fileToolBar.addAction(self.deflateAction)
        fileToolBar.addAction(self.circumgyrate)

    def slotZoomin(self):
        if self.image.isNull():
            return
        martix = QMatrix4x4()
        martix.scale(2, 2)
        self.image = self.image.transformed(martix)
        self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
        self.resize(self.image.width(), self.image.height())

    def slotDeflate(self):
        if self.image.isNull():
            return
        martix = QMatrix4x4()
        martix.scale(0.5, 0.5)
        self.image = self.image.transformed(martix)
        self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
        self.resize(self.image.width(), self.image.height())

    def slotCircumgyrate(self):
        if self.image.isNull():
            return
        martix = QMatrix4x4()
        martix.rotate(90)
        self.image = self.image.transformed(martix)
        self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
        self.resize(self.image.width(), self.image.height())


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()