from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os,sys

#基础控件实现
def app_path(name):
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    return "%s%s" %(dirname,name)

def file_ico(name):
    #print("图标目标：%s" %os.path.join(app_path(r"\resource\image"),name))
    return os.path.join(app_path(r"\resource\image"),name)

def file_style(name):
    return os.path.join(app_path(r"\resource\style"),name)

def file_tmp(name):
    return os.path.join(app_path(r"\tmp"), name)

class Icon(QIcon):

    def __init__(self,name):
        super(Icon,self).__init__()
        self.addPixmap(QPixmap(file_ico(name)),QIcon.Normal,QIcon.On)

def mes_warn(parent,message):
    button = QMessageBox.warning(parent,"明州体检", message,QMessageBox.Yes | QMessageBox.No)
    return button

def mes_about(parent,message):
    QMessageBox.about(parent, '明州体检', message)