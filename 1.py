from random import randrange

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class MessageBox(QMessageBox):

    def __init__(self, *args, count=5, time=1000, auto=True, **kwargs):
        super(MessageBox, self).__init__(*args, **kwargs)
        self._count = count
        self._time = time
        self._auto = auto  # 是否自动关闭

        self.setStandardButtons(self.Close)  # 关闭按钮
        self.closeBtn = self.button(self.Close)  # 获取关闭按钮
        self.closeBtn.setText('关闭(%s)' % count)
        # self.closeBtn.setEnabled(False)
        self._timer = QTimer(self, timeout=self.doCountDown)
        self._timer.start(self._time)
        print('是否自动关闭', auto)

    def doCountDown(self):
        self.closeBtn.setText('关闭(%s)' % self._count)
        self._count -= 1
        if self._count <= 0:
            self.closeBtn.setText('关闭')
            self.closeBtn.setEnabled(True)
            self._timer.stop()
            if self._auto:  # 自动关闭
                self.accept()
                self.close()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication, QPushButton
    app = QApplication(sys.argv)
    w = QPushButton('点击弹出对话框')
    w.resize(200, 200)
    w.show()

    MessageBox().about(w,'标题','描述')
    w.clicked.connect(lambda: MessageBox(
        w, text='倒计时关闭对话框', auto=randrange(0, 10)).exec_())
    sys.exit(app.exec_())