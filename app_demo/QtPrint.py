from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QTextEdit, QFileDialog, QDialog
"""
从类的字面意思我们也可以了解到QPageSetupDialog涉及页面设置的，QPrintDialog涉及打印，而QPrinter呢？QPrinter类是PyQt的打印主要使用，即打印类。大量和打印相关的函数均会涉及到该类。
"""
from PyQt5.QtPrintSupport import *
import sys

#         """
# 因为下面代码中QPageSetupDialog、QPrintDialog涉及到QPrinter()对象，所以将其在类初始化的时候生成，便于函数的调用。
#         """
class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.printer = QPrinter()
        info = QPrinterInfo()
        default_printer = info.defaultPrinterName() # 默认打印机名字
        all_printerslist = info.availablePrinterNames() # 各个打印机名字
        print_mode = info.defaultDuplexMode()          # 返回此打印机的默认双面打印模式。
        print(info.supportedDuplexModes)

        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('早点毕业吧--保存、打印文件')


        self.tx = QTextEdit(self)
        self.tx.setGeometry(20, 20, 300, 270)

        self.bt1 = QPushButton('打开文件',self)
        self.bt1.move(350,20)
        self.bt2 = QPushButton('打开多个文件',self)
        self.bt2.move(350,70)
        self.bt5 = QPushButton('保存文件',self)
        self.bt5.move(350,220)
        self.bt6 = QPushButton('页面设置',self)
        self.bt6.move(350,270)
        self.bt7 = QPushButton('打印文档',self)
        self.bt7.move(350,320)

        self.bt1.clicked.connect(self.openfile)
        self.bt2.clicked.connect(self.openfiles)
        self.bt5.clicked.connect(self.savefile)
        self.bt6.clicked.connect(self.pagesettings)
        self.bt7.clicked.connect(self.printdialog)

        self.show()

    # """
    #     这个函数的第二个参数是对话框的标题，第三个参数是设置打开文件的目录。当然我们还可以增加第四个，也就是增加一个过滤器，以便仅显示与过滤器匹配的文件。 例如：
    #
    # fnames = QFileDialog.getOpenFileNames(self, '学点编程吧:打开多个文件','./',"Text files (*.txt)")
    #
    #  """
    def openfile(self):

        fname = QFileDialog.getOpenFileName(self, '学点编程吧:打开文件','./')
        if fname[0]:
            with open(fname[0], 'r',encoding='gb18030',errors='ignore') as f:
                self.tx.setText(f.read())
    #     """
    # QFileDialog.getOpenFileNames将返回用户选择的一个或多个现有文件，注意这里返回值是元组。元组的第0个元素则是列表，
    #     """
    def openfiles(self):
        fnames = QFileDialog.getOpenFileNames(self, '学点编程吧:打开多个文件','./')
        if fnames[0]: 
            for fname in fnames[0]:
                with open(fname, 'r',encoding='gb18030',errors='ignore') as f:

                #所以我们通过对fnames[0]进行遍历，分别读取每个文件的内容，然后在QTextEdit显示出来。
                # 需要注意的是：我们使用了QTextEdit的append方法，让每次显示的内容均会存留在QTextEdit上。

                    self.tx.append(f.read())
    # """
    # getSaveFileName()具体的用法与getOpenFileNames()类似，只是用来保存文件的。最后我们使用write函数将QTextEdit的内容保存在文件中。获取的QTextEdit的内容可以使用这个函数toPlainText()。
    # """
    def savefile(self):
        fileName = QFileDialog.getSaveFileName(self, '学点编程吧:保存文件','./',"Text files (*.txt)")
        if fileName[0]:
            with open(fileName[0], 'w',encoding='gb18030',errors='ignore') as f:
                f.write(self.tx.toPlainText())
    # """
    # QPageSetupDialog类为打印机上的页面相关选项提供了一个配置对话框。这个就必须使用到QPrinter对象了。
    # """
    def pagesettings(self):

        printsetdialog = QPageSetupDialog(self.printer,self)
        printsetdialog.exec_()
        #这句话就相当于我们执行确认的页面设置信息。

    #     """
    # 这个函数就是告诉我们调用QPrintDialog准备进行打印了。
    # QPrintDialog类提供了一个用于指定打印机配置的对话框。对话框允许用户更改文档相关设置，如纸张尺寸和方向，打印类型（颜色或灰度），页面范围和打印份数。
    # 还提供控制以使用户可以从可用的打印机中进行选择，包括任何配置的网络打印机。通常，QPrintDialog对象使用QPrinter对象构造，并使用exec()函数执行。
    #
    #        """
#         """
# 在我们选择好打印机等等后，点击打印（即对话框被用户接受，则QPrinter对象被正确配置为打印），我们会调用QTextEdit中的print方法进行相关的打印
#         """
    def printdialog(self):

        printdialog = QPrintDialog(self.printer,self)

        if QDialog.Accepted == printdialog.exec_():
            self.tx.print(self.printer)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
