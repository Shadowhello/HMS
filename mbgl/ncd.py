from .ncd_ui import *
from utils.readparas import GolParasMixin

class NCDManager(GolParasMixin,NCD_UI):

    def __init__(self):
        super(NCDManager, self).__init__("慢病管理")