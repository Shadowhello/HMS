from ctypes import CDLL

# 截图工具
def screen_shot():
    dll = CDLL('ScreenShot.dll')
    dll.PrScrn()



if __name__ =="__main__":
    screen_shot()