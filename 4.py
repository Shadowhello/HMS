import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from qregexeditor.api import RegexEditorWidget, QuickRefWidget

# 正则表达式 API

app = QApplication(sys.argv)
window = QMainWindow()
editor = RegexEditorWidget()
quick_ref = QuickRefWidget()
quick_ref.hide()
window.setCentralWidget(editor)
# show/hide quick reference widget
editor.quick_ref_requested.connect(quick_ref.setVisible)
window.show()
app.exec_()