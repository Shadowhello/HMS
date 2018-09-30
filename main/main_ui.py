from widgets.bwidget import *
from importlib import import_module
from .about import about_msessage
from .menu_config import *
from utils import gol
from functools import partial
import time

class StatusLabel(QLabel):

    def __init__(self,p_str=None,parent=None):
        super(StatusLabel,self).__init__(p_str,parent)
        self.setStyleSheet('''font: 75 11pt \"微软雅黑\";color: rgb(255, 255, 255);''')

#状态栏
class StatusBar(QStatusBar):

    def __init__(self):
        super(StatusBar,self).__init__()
        self.initUI()
        #定时器
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.on_time_show)

    # 初始化界面
    def initUI(self):
        self.lb_version = StatusLabel('版本：V%s' %gol.get_value('system_version',''))
        self.lb_login = StatusLabel('用户：%s '%gol.get_value('login_user_name',''))
        self.lb_hostname = StatusLabel('主机：%s ' % gol.get_value('host_name','未获取到'))
        self.lb_hostip = StatusLabel('IP：%s ' % gol.get_value('host_ip','未获取到'))
        self.lb_room = StatusLabel('房间：%s ' % gol.get_value('login_area', '未获取到'))
        self.lb_handle_mes = StatusLabel()
        self.lb_login_time = StatusLabel(' 登录时间：%s ' % gol.get_value('login_time',''))
        self.lb_cur_time = StatusLabel()
        self.lb_cur_time.setText(" 当前时间：%s " %time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        self.addWidget(self.lb_version)
        self.addWidget(self.lb_login)
        self.addWidget(self.lb_hostname)
        self.addWidget(self.lb_hostip)
        self.addWidget(self.lb_room)
        self.addWidget(self.lb_handle_mes)
        self.addPermanentWidget(self.lb_login_time)
        self.addPermanentWidget(self.lb_cur_time)

    def on_time_show(self):
        now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.lb_cur_time.setText("当前时间：%s" %now)

    def on_change_mes(self,p_str):
        self.handle_mes.setText(p_str)

#工具栏
class ToolBar(QToolBar):

    def __init__(self):
        super(ToolBar,self).__init__()
        self.setIconSize(QSize(32,32))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setFloatable(True)

#菜单栏
class MenuBar(QMenuBar):

    def __init__(self,parent):
        super(MenuBar,self).__init__(parent)
        self.tree = MenuObjTree()
        self.sys_action_obj = {}
        self.init()


    def init(self):
        toolbar = ToolBar()
        for menubar_name in self.tree.menubar_names:
            menu = self.addMenu(menubar_name)
            if not self.tree.menubar_status(menubar_name):
                menu.setEnabled(False)
            # 保证同时只能选择一个
            action_group = QActionGroup(self)
            action_group.setExclusive(True)    #
            # # 菜单
            for action_name in self.tree.menu_names(menubar_name):
                action_obj = self.tree.menu_obj(menubar_name,action_name)
                action = Action(self, action_obj)
                # 存入字典
                self.sys_action_obj[action.sid] = action
                if action.sid == 1008:
                    menu.addAction('退出', self.parentWidget().close, shortcut="Ctrl+Q")
                else:
                    action.triggered.connect(partial(self.parentWidget().openWidget,action))
                    if not self.tree.menu_status(menubar_name, action_name):
                        action.setDisabled(True)

                    menu.addAction(action_group.addAction(action))

                #############################判断菜单是否在工具栏中显示######################################

                if self.tree.menu_is_tool(menubar_name, action_name):
                    toolbar.addAction(action)
                #
                self.parentWidget().addToolBar(toolbar)

        ######################所有用户均有权限##########################################
        menu_help = self.addMenu(Icon('帮助'), '帮助')
        # menu_help.addAction(Icon('操作手册'), '操作手册')
        # menu_help.addAction(Icon('注册'), '注册')
        self.menu_help_skin = menu_help.addMenu(Icon('皮肤'), '更换皮肤')
        #self.menu_help_skin.addAction('默认', partial(self.on_menu_help_skin_triggered, '默认'))
        # for skin in skins:
        #     self.menu_help_skin.addAction(skin, partial(self.on_menu_help_skin_triggered, skin))
        menu_help.addAction(Icon('意见'), '意见')
        menu_help.addAction(Icon('关于'), '关于',self.about)

    # 获取用户默认的菜单栏，便于程序自动打开
    def default_action(self,sid):
        return self.sys_action_obj.get(sid,None)

    def about(self):
        QMessageBox.about(self, "明州体检",about_msessage)

# 菜单 按钮
class Action(QAction):
    def __init__(self, parent, paras: dict):
        self.pid = paras.get('pid', 0)
        self.sid = paras.get('sid', 99)
        self.is_tool = paras.get('is_tool', False)
        super(Action, self).__init__(parent)
        self.setToolTip(paras.get('tip', ''))
        self.setText(paras.get('title', '此菜单名称未获取到'))
        self.setIcon(Icon(paras.get('icon', 'mztj')))
        self.setEnabled(paras.get('state', False))
        self.setParent(parent)
        self.class_name = None

    @property
    def module(self):

        module_class_info = SYS_MENU_MODULE_CLASS.get(self.sid, {})
        if module_class_info:
            module_name = module_class_info.get('module', '')
            class_name = module_class_info.get('class', '')
            enable = module_class_info.get('enabled', False)
            if module_name:
                if enable:
                    self.class_name = class_name
                    try:
                        return import_module(module_name)
                    except Exception as e:
                        mes_about(self.parentWidget(), '模块：%s 导入失败！错误信息：%s' % (module_name, e))
                        return ''

                mes_about(self.parentWidget(), '未开放此模块！')

        return ''

    @property
    def cls_name(self):
        return self.class_name


# 解析登录用户的菜单树
class MenuObjTree(object):
    def __init__(self, obj=SYS_MENU_TREE):  # 可设置为用户级菜单
        self.obj = obj

    # 所有菜单栏
    @property
    def menubars(self):
        return self.obj.get('childs', {})

    # 获取菜单栏名称列表
    @property
    def menubar_names(self):
        return self.menubars.keys()

    # 获取菜单栏对象字典
    def menubar_obj(self, menu_bar_name: str):
        return self.menubars.get(menu_bar_name, {})

    def menubar_status(self, menu_bar_name: str):
        return self.menubar_obj(menu_bar_name).get('state', True)

    # 获取当前菜单栏下 所有菜单对象
    def menus(self, menu_bar_name: str):
        return self.menubar_obj(menu_bar_name).get('childs', {})

    # 获取当前菜单栏下所有菜单名称
    def menu_names(self, menu_bar_name: str):
        return self.menus(menu_bar_name).keys()

    # 获取当前菜单栏下当前菜单对象
    def menu_obj(self, menu_bar_name: str, menu_name: str):
        return self.menus(menu_bar_name).get(menu_name, {})

    # 当前菜单对象状态
    def menu_status(self, menu_bar_name: str, menu_name: str):
        return self.menu_obj(menu_bar_name, menu_name).get('state', True)

    # 当前菜单工具栏中是否显示
    def menu_is_tool(self, menu_bar_name: str, menu_name: str):
        return self.menu_obj(menu_bar_name, menu_name).get('is_tool', False)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = StatusBar()
    ui.show()
    app.exec_()

