from .film_print_ui import *
from .model import *


# 报告追踪
class FilmPrint(FilmPrintUI):

    def __init__(self):
        super(FilmPrint, self).__init__()
        self.initParas()
        # 绑定信号槽
        # self.btn_query.clicked.connect(self.on_btn_query_click)
        # self.btn_print.clicked.connect(self.on_btn_print_click)
        # 右键、双击、单击
        # self.table_print.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        # self.table_print.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单
        # self.table_print.itemClicked.connect(self.on_table_set)
        # self.table_print.itemDoubleClicked.connect(self.on_btn_item_click)
        # 快速减速
        # self.gp_quick_search.returnPressed.connect(self.on_quick_search)    # 快速检索
        # 特殊变量
        self.cur_tjbh = None


    # 初始化部分参数
    def initParas(self):
        self.ini_is_remote = gol.get_value('print_network',1)
        self.ini_printer = gol.get_value('print_printer', '79号打印机')
        self.gp_print_setup.setParas(self.ini_is_remote,self.ini_printer)
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()
        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)

        self.lt_where_search.s_dwbh.setValues(self.dwmc_bh,self.dwmc_py)