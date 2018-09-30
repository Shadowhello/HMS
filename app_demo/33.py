# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys


class DialogOptionsWidget(QWidget):
    def __init__(self, parent=None):
        super(DialogOptionsWidget, self).__init__(parent)

    def addCheckBox(self, text, value):
        pass

    def addSpacer():
        pass

    def value():
        pass


class StandardDialog(QDialog):
    def __init__(self, parent=None):
        super(StandardDialog, self).__init__(parent)

        self.setWindowTitle("Standard Dialog")

        frameStyle = QFrame.Sunken | QFrame.Panel

        mainLayout = QVBoxLayout(self)
        toolbox = QToolBox()
        mainLayout.addWidget(toolbox)

        self.errorMessageDialog = QErrorMessage(self)

        pushButton_integer = QPushButton("QInputDialog.get&Int()")
        pushButton_double = QPushButton("QInputDialog.get&Double()")
        pushButton_item = QPushButton("QInputDialog.getIte&m()")
        pushButton_text = QPushButton("QInputDialog.get&Text()")
        pushButton_multiLineText = QPushButton("QInputDialog.get&MultiLineText()")
        pushButton_color = QPushButton("QColorDialog.get&Color()")
        pushButton_font = QPushButton("QFontDialog.get&Font()")
        pushButton_directory = QPushButton("QFileDialog.getE&xistingDirectory()")
        pushButton_openFileName = QPushButton("QFileDialog.get&OpenFileName()")
        pushButton_openFileNames = QPushButton("QFileDialog.&getOpenFileNames()")
        pushButton_saveFileName = QPushButton("QFileDialog.get&SaveFileName()")
        pushButton_critical = QPushButton("QMessageBox.critica&l()")
        pushButton_information = QPushButton("QMessageBox.i&nformation()")
        pushButton_question = QPushButton("QQMessageBox.&question()")
        pushButton_warning = QPushButton("QMessageBox.&warning()")
        pushButton_error = QPushButton("QErrorMessage.showM&essage()")

        self.label_integer = QLabel()
        self.label_double = QLabel()
        self.label_item = QLabel()
        self.label_text = QLabel()
        self.label_multiLineText = QLabel()
        self.label_color = QLabel()
        self.label_font = QLabel()
        self.label_directory = QLabel()
        self.label_openFileName = QLabel()
        self.label_openFileNames = QLabel()
        self.label_saveFileName = QLabel()
        self.label_critical = QLabel()
        self.label_information = QLabel()
        self.label_question = QLabel()
        self.label_warning = QLabel()
        self.label_error = QLabel()

        self.label_integer.setFrameStyle(frameStyle)
        self.label_double.setFrameStyle(frameStyle)
        self.label_item.setFrameStyle(frameStyle)
        self.label_text.setFrameStyle(frameStyle)
        self.label_multiLineText.setFrameStyle(frameStyle)
        self.label_color.setFrameStyle(frameStyle)
        self.label_font.setFrameStyle(frameStyle)
        self.label_directory.setFrameStyle(frameStyle)
        self.label_openFileName.setFrameStyle(frameStyle)
        self.label_openFileNames.setFrameStyle(frameStyle)
        self.label_saveFileName.setFrameStyle(frameStyle)
        self.label_critical.setFrameStyle(frameStyle)
        self.label_information.setFrameStyle(frameStyle)
        self.label_question.setFrameStyle(frameStyle)
        self.label_warning.setFrameStyle(frameStyle)
        self.label_error.setFrameStyle(frameStyle)

        page = QWidget()
        layout = QGridLayout(page)
        layout.setColumnStretch(1, 1)
        layout.setColumnMinimumWidth(1, 250)
        layout.addWidget(pushButton_integer, 0, 0)
        layout.addWidget(self.label_integer, 0, 1)
        layout.addWidget(pushButton_double, 1, 0)
        layout.addWidget(self.label_double, 1, 1)
        layout.addWidget(pushButton_item, 2, 0)
        layout.addWidget(self.label_item, 2, 1)
        layout.addWidget(pushButton_text, 3, 0)
        layout.addWidget(self.label_text, 3, 1)
        layout.addWidget(pushButton_multiLineText, 4, 0)
        layout.addWidget(self.label_multiLineText, 4, 1)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Ignored, QSizePolicy.MinimumExpanding), 5, 0)
        toolbox.addItem(page, "Input Dialog")

        page = QWidget()
        layout = QGridLayout(page)
        layout.setColumnStretch(1, 1)
        # layout.setColumnMinimumWidth(1,250)
        layout.addWidget(pushButton_color, 0, 0)
        layout.addWidget(self.label_color, 0, 1)
        colorDialogOptionsWidget = DialogOptionsWidget()
        colorDialogOptionsWidget.addCheckBox("Do not use native dialog", QColorDialog.DontUseNativeDialog)
        colorDialogOptionsWidget.addCheckBox("Show alpha channel", QColorDialog.ShowAlphaChannel)
        colorDialogOptionsWidget.addCheckBox("No buttons", QColorDialog.NoButtons)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Ignored, QSizePolicy.MinimumExpanding), 1, 0)
        layout.addWidget(colorDialogOptionsWidget, 2, 0, 1, 2)
        toolbox.addItem(page, "Color Dialog")

        page = QWidget()
        layout = QGridLayout(page)
        layout.setColumnStretch(1, 1)
        layout.addWidget(pushButton_font, 0, 0)
        layout.addWidget(self.label_font, 0, 1)
        fontDialogOptionsWidget = DialogOptionsWidget()
        fontDialogOptionsWidget.addCheckBox("Do not use native dialog", QFontDialog.DontUseNativeDialog)
        fontDialogOptionsWidget.addCheckBox("No buttons", QFontDialog.NoButtons)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Ignored, QSizePolicy.MinimumExpanding), 1, 0)
        layout.addWidget(fontDialogOptionsWidget, 2, 0, 1, 2)
        toolbox.addItem(page, "Font Dialog")

        page = QWidget()
        layout = QGridLayout(page)
        layout.setColumnStretch(1, 1)
        layout.addWidget(pushButton_directory, 0, 0)
        layout.addWidget(self.label_directory, 0, 1)
        layout.addWidget(pushButton_openFileName, 1, 0)
        layout.addWidget(self.label_openFileName, 1, 1)
        layout.addWidget(pushButton_openFileNames, 2, 0)
        layout.addWidget(self.label_openFileNames, 2, 1)
        layout.addWidget(pushButton_saveFileName, 3, 0)
        layout.addWidget(self.label_saveFileName, 3, 1)
        fileDialogOptionsWidget = DialogOptionsWidget()
        fileDialogOptionsWidget.addCheckBox("Do not use native dialog", QFileDialog.DontUseNativeDialog)
        fileDialogOptionsWidget.addCheckBox("Show directories only", QFileDialog.ShowDirsOnly)
        fileDialogOptionsWidget.addCheckBox("Do not resolve symlinks", QFileDialog.DontResolveSymlinks)
        fileDialogOptionsWidget.addCheckBox("Do not confirm overwrite", QFileDialog.DontConfirmOverwrite)
        fileDialogOptionsWidget.addCheckBox("Do not use sheet", QFileDialog.DontUseSheet)
        fileDialogOptionsWidget.addCheckBox("Readonly", QFileDialog.ReadOnly)
        fileDialogOptionsWidget.addCheckBox("Hide name filter details", QFileDialog.HideNameFilterDetails)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Ignored, QSizePolicy.MinimumExpanding), 4, 0)
        layout.addWidget(fileDialogOptionsWidget, 5, 0, 1, 2)
        toolbox.addItem(page, "File Dialogs")

        page = QWidget()
        layout = QGridLayout(page)
        layout.setColumnStretch(1, 1)
        layout.addWidget(pushButton_critical, 0, 0)
        layout.addWidget(self.label_critical, 0, 1)
        layout.addWidget(pushButton_information, 1, 0)
        layout.addWidget(self.label_information, 1, 1)
        layout.addWidget(pushButton_question, 2, 0)
        layout.addWidget(self.label_question, 2, 1)
        layout.addWidget(pushButton_warning, 3, 0)
        layout.addWidget(self.label_warning, 3, 1)
        layout.addWidget(pushButton_error, 4, 0)
        layout.addWidget(self.label_error, 4, 1)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Ignored, QSizePolicy.MinimumExpanding), 5, 0)
        toolbox.addItem(page, "Message Boxes")

        pushButton_integer.clicked.connect(self.setInteger)
        pushButton_double.clicked.connect(self.setDouble)
        pushButton_item.clicked.connect(self.setItem)
        pushButton_text.clicked.connect(self.setText)
        pushButton_multiLineText.clicked.connect(self.setMultiLineText)
        pushButton_color.clicked.connect(self.setColor)
        pushButton_font.clicked.connect(self.setFont)
        pushButton_directory.clicked.connect(self.setExistingDirectory)
        pushButton_openFileName.clicked.connect(self.setOpenFileName)
        pushButton_openFileNames.clicked.connect(self.setOpenFileNames)
        pushButton_saveFileName.clicked.connect(self.setSaveFileName)
        pushButton_critical.clicked.connect(self.criticalMessage)
        pushButton_information.clicked.connect(self.informationMessage)
        pushButton_question.clicked.connect(self.questionMessage)
        pushButton_warning.clicked.connect(self.warningMessage)
        pushButton_error.clicked.connect(self.errorMessage)

        # 输入对话框 取整数

    def setInteger(self):
        intNum, ok = QInputDialog.getInt(self, "QInputDialog.getInteger()", "Percentage:", 25, 0, 100, 1)
        if ok:
            self.label_integer.setText(str(intNum))

    # 输入对话框 取实数
    def setDouble(self):
        doubleNum, ok = QInputDialog.getDouble(self, "QInputDialog.getDouble()", "Amount:", 37.56, -10000, 10000, 2)
        if ok:
            self.label_double.setText(str(doubleNum))

    # 输入对话框 取列表项
    def setItem(self):
        items = ["Spring", "Summer", "Fall", "Winter"]
        item, ok = QInputDialog.getItem(self, "QInputDialog.getItem()", "Season:", items, 0, False)
        if ok and item:
            self.label_item.setText(item)

    # 输入对话框 取文本
    def setText(self):
        text, ok = QInputDialog.getText(self, "QInputDialog.getText()", "User name:", QLineEdit.Normal,
                                        QDir.home().dirName())
        if ok and text:
            self.label_text.setText(text)

    # 输入对话框 取多行文本
    def setMultiLineText(self):
        text, ok = QInputDialog.getMultiLineText(self, "QInputDialog.getMultiLineText()", "Address:",
                                                 "John Doe\nFreedom Street")
        if ok and text:
            self.label_multiLineText.setText(text)

    # 颜色对话框 取颜色
    def setColor(self):
        # options = QColorDialog.ColorDialogOptions(QFlag.QFlag(colorDialogOptionsWidget.value()))
        color = QColorDialog.getColor(Qt.green, self, "Select Color")

        if color.isValid():
            self.label_color.setText(color.name())
            self.label_color.setPalette(QPalette(color))
            self.label_color.setAutoFillBackground(True)

    # 字体对话框 取字体
    def setFont(self):
        # options = QFontDialog.FontDialogOptions(QFlag(fontDialogOptionsWidget.value()))
        # font, ok = QFontDialog.getFont(ok, QFont(self.label_font.text()), self, "Select Font",options)
        font, ok = QFontDialog.getFont()
        if ok:
            self.label_font.setText(font.key())
            self.label_font.setFont(font)

    # 目录对话框 取目录
    def setExistingDirectory(self):
        # options = QFileDialog.Options(QFlag(fileDialogOptionsWidget->value()))
        # options |= QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
                                                     "QFileDialog.getExistingDirectory()",
                                                     self.label_directory.text())
        if directory:
            self.label_directory.setText(directory)

    # 打开文件对话框 取文件名
    def setOpenFileName(self):
        # options = QFileDialog.Options(QFlag(fileDialogOptionsWidget.value()))
        # selectedFilter
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                         "QFileDialog.getOpenFileName()",
                                                         self.label_openFileName.text(),
                                                         "All Files (*);;Text Files (*.txt)")
        if fileName:
            self.label_openFileName.setText(fileName)

    # 打开文件对话框 取一组文件名
    def setOpenFileNames(self):
        # options = QFileDialog.Options(QFlag(fileDialogOptionsWidget.value()))
        # selectedFilter
        openFilesPath = "D:/documents/pyMarksix/draw/"
        files, ok = QFileDialog.getOpenFileNames(self,
                                                 "QFileDialog.getOpenFileNames()",
                                                 openFilesPath,
                                                 "All Files (*);;Text Files (*.txt)")

        if len(files):
            self.label_openFileNames.setText(", ".join(files))

    # 保存文件对话框 取文件名
    def setSaveFileName(self):
        # options = QFileDialog.Options(QFlag(fileDialogOptionsWidget.value()))
        # selectedFilter
        fileName, ok = QFileDialog.getSaveFileName(self,
                                                   "QFileDialog.getSaveFileName()",
                                                   self.label_saveFileName.text(),
                                                   "All Files (*);;Text Files (*.txt)")
        if fileName:
            self.label_saveFileName.setText(fileName)

    def criticalMessage(self):
        # reply = QMessageBox.StandardButton()
        MESSAGE = "批评！"
        reply = QMessageBox.critical(self,
                                     "QMessageBox.critical()",
                                     MESSAGE,
                                     QMessageBox.Abort | QMessageBox.Retry | QMessageBox.Ignore)
        if reply == QMessageBox.Abort:
            self.label_critical.setText("Abort")
        elif reply == QMessageBox.Retry:
            self.label_critical.setText("Retry")
        else:
            self.label_critical.setText("Ignore")

    def informationMessage(self):
        MESSAGE = "信息"
        reply = QMessageBox.information(self, "QMessageBox.information()", MESSAGE)
        if reply == QMessageBox.Ok:
            self.label_information.setText("OK")
        else:
            self.label_information.setText("Escape")

    def questionMessage(self):
        MESSAGE = "疑问"
        reply = QMessageBox.question(self, "QMessageBox.question()",
                                     MESSAGE,
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.label_question.setText("Yes")
        elif reply == QMessageBox.No:
            self.label_question.setText("No")
        else:
            self.label_question.setText("Cancel")

    def warningMessage(self):
        MESSAGE = "警告文本"
        msgBox = QMessageBox(QMessageBox.Warning,
                             "QMessageBox.warning()",
                             MESSAGE,
                             QMessageBox.Retry | QMessageBox.Discard | QMessageBox.Cancel,
                             self)
        msgBox.setDetailedText("详细信息。。。")
        # msgBox.addButton("Save &Again", QMessageBox.AcceptRole)
        # msgBox.addButton("&Continue", QMessageBox.RejectRole)
        if msgBox.exec() == QMessageBox.AcceptRole:
            self.label_warning.setText("Retry")
        else:
            self.label_warning.setText("Abort")

    def errorMessage(self):
        self.errorMessageDialog.showMessage(
            "This dialog shows and remembers error messages. "
            "If the checkbox is checked (as it is by default), "
            "the shown message will be shown again, "
            "but if the user unchecks the box the message "
            "will not appear again if QErrorMessage.showMessage() "
            "is called with the same message.")
        self.label_error.setText("If the box is unchecked, the message "
                                 "won't appear again.")


app = QApplication(sys.argv)
form = StandardDialog()
form.show()
app.exec_()