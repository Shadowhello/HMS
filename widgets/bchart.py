import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib import pyplot as plt

# 在matplotlib中，整个图像为一个Figure对象；
# 在Figure对象中可以包含一个或者多个Axes对象；
# 每个Axes(ax)对象都是一个拥有自己坐标系统的绘图区域；

class BaseChart(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.initParas()
        #创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #在父类中激活Figure窗口（#此句必不可少，否则不能显示图形）
        super(BaseChart,self).__init__(self.fig)
        self.setParent(parent)
        # 设置标题
        # self.fig.suptitle(title, fontproperties=self.font)

    def initParas(self):
        self.font = FontProperties(fname=r"c:\windows\fonts\msyh.ttf", size=14)


    def setFont(self,font_name,font_size):
        font ={
            '微软雅黑':'msyh.ttf',
            '宋体': 'simsun.ttc',
            '黑体': 'simhei.ttf',
        }
        self.font = FontProperties(
            fname=r"c:\windows\fonts\%s" %font.get(font_name,'msyh.ttf'),
            size=font_size
        )


    def init_figure(self,lb_y:str,lb_x:str,datas:dict,title):
        # 创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title(title,fontproperties=self.font)
        # 画柱状图，设置柱的边缘为透明
        bars = self.axes.bar(xticks, values, width=0.5, edgecolor='none')
        # ha 文字指定在柱体中间， va指定文字位置 fontsize指定文字体大小
        for a, b in datas.items():
            plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom',fontsize=11)
        # 设置X轴 Y轴数据，两者都可以是list或者tuple
        x_axis = tuple(datas.keys())
        y_axis = tuple(datas.values())
        plt.bar(x_axis, y_axis, color='rgb')  # 如果不指定color，所有的柱体都会是一个颜色
        self.axes.hold(False)
        t = [1,2,3,4,5,6]
        s = [10,20,30,40,50,60]
        self.axes.plot(t, s)
        font = FontProperties(fname=r"c:\windows\fonts\msyh.ttf", size=14)
        self.axes.set_ylabel(lb_y,fontproperties=font)
        self.axes.set_xlabel(lb_x,fontproperties=font)
        self.axes.grid(True)


if __name__ == '__main__':
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    import sys
    app = QApplication(sys.argv)
    ui = QDialog()
    lt_main = QHBoxLayout()
    chart = BaseChart(ui,title="测试")
    chart.init_figure("Y轴","X轴",[])
    ui.setLayout(lt_main)
    ui.show()
    app.exec_()