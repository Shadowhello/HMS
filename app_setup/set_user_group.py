from widgets.cwidget import *
from .model import *

class SetUserGroup(Widget):

    def __init__(self,parent=None):
        super(SetUserGroup,self).__init__(parent)
        self.initUI()

    def initParas(self):
        pass

    def initUI(self):
        lt_main = QHBoxLayout()
        lt_main_left = QHBoxLayout()
        gp_main_left = QGroupBox('角色')
        ###########################################################
        self.lw_sys_permissions = QListWidget()
        results = self.session.query(MT_Permissions).all()
        self.lw_sys_permissions.addItems([result.pname for result in results])
        lt_main_left.addWidget(self.lw_sys_permissions)
        gp_main_left.setLayout(lt_main_left)
        ###########################################################
        lt_main_right = QHBoxLayout()
        gp_main_right = QGroupBox('功能菜单')


