from .ncd_ui import *
from utils.readparas import GolParasMixin

class NCD(GolParasMixin,NCD_UI):

    def __init__(self):
        super(NCD, self).__init__("慢病管理")