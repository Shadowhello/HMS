import ctypes,os

# 载入动态库->初始化->卡认证->读卡->关闭连接
class IdCard(object):

    def __init__(self,dll_name="termb.dll",port_type='usb'):
        '''
        :param port_type: 连接用USB口/串口。port：连接串口（COM1~COM16）或USB口(1001~1016)
        :param dll_name: 动态库名字，带文件路径，默认根目录
        '''
        self.ports = list(range(1,17))+list(range(1001,1017))
        # if port_type == 'usb':
        #     self.ports = range(1001, 1017)
        # else:
        #     self.ports = range(1, 17)

        # 加载动态库
        try:
            self.dll_obj = ctypes.windll.LoadLibrary(dll_name)
            # self.dll_obj = ctypes.WinDLL("termb.dll")
        except Exception as e:
            print('未找到身份证读卡器驱动DLL：%s' % dll_name)
            self.dll_obj = None

        # 卡连接状态
        self.is_conn=None

    # 本函数用于PC与华视电子第二代居民身份证阅读器的连接
    def open(self):
        '''
        :return:
            # 值   意义
            # 1   正确
            # 2   端口打开失败
            # 0   动态库加载失败
        '''
        for port in self.ports:
            if self.dll_obj.CVR_InitComm(port)==1:
                self.is_conn = True
                return True
        else:
            return False

    # 本函数用于关闭PC到阅读器的连接
    def close(self):
        '''
        :return:
            # 值   意义
            # 1   正确
            # 0   错误
        '''
        if self.is_conn:
            self.dll_obj.CVR_CloseComm()

    # 本函数用于读卡器和卡片之间的合法身份确认。卡认证循环间隔大于300ms。
    # 若卡片放置后发生认证错误时，应移走卡片重新放置。
    def legal(self):
        '''
        :return:
            # 值   意义  说明
            # 1   正确  卡片认证成功
            # 2   错误  寻卡失败
            # 3   错误  选卡失败
            # 0   错误  初始化失败
        '''

        return self.dll_obj.CVR_Authenticate()


    # 本函数用于通过阅读器从第二代居民身份证中读取相应信息。
    # 卡认证成功以后才可做读卡操作，读卡完毕若继续读卡应移走二代证卡片重新放置做卡认证。
    def read(self,active:int):
        # '''
        # :param active:
        #     参数名  含义                     取值范围
        #     active  临时目录中保存哪些文件   见取值说明
        #     ############################################
        #     取值说明：
        #         值	意义
        #         1	wz.txt，xp.wlt，zp.bmp，fp.dat
        #         2	wz.txt，xp.wlt，fp.dat
        #         4	wz.txt，zp.bmp，fp.dat
        #     ############################################
        #     文件说明：
        #         文件名	意义
        #         wz.txt	身份证基本信息，如姓名、性别等
        #         xp.wlt	加密的头像数据
        #         zp.bmp	解密的头像数据
        #         fp.dat	指纹数据，若无指纹则该文件大小仍为1024字节，每个字节均为0
        #     #############################################
        #     1、wz.txt文件格式
        #     读卡成功后在临时目录下生成wz.txt（文字信息）和zp.bmp（照片信息）
        #     临时目录跟当前登录用户名称有关，如C:\Users\mac\AppData\Local\Temp\chinaidcard
        #     wz.txt内容示例如下：
        #     张红叶
        #     女
        #     汉
        #     19881118
        #     河北省邯郸市临漳县称勾镇称勾东村复兴路25号
        #     130423198811184328
        #     临漳县公安局
        #     20110330-20210330
        #
        # :return:
        #         值	意义
        #         1	正确
        #         0	错误
        #         99	异常
        # '''
        return self.dll_obj.CVR_Read_Content(active)


    # 读卡至内存
    def read2(self):
        self.dll_obj.CVR_ReadBaseMsg()


if __name__=="__main__":
    file_wx = os.path.join(os.environ["TMP"], 'chinaidcard\wz.txt')
    file_zp = os.path.join(os.environ["TMP"], 'chinaidcard\zp.bmp')
    c_obj = IdCard()
    if c_obj.dll_obj:
        open_state = c_obj.open()
        if open_state==1:
            legal_state = c_obj.legal()
            if legal_state == 1:
                if c_obj.read(4)==1:
                    user_info = open(file_wx).read().split('\n')
                    print(user_info)
                    os.remove(file_wx)
                    os.remove(file_zp)
            elif legal_state==2:
                print('寻卡失败！')
            elif legal_state==3:
                print('选卡失败！')
            else:
                print('初始化失败！')
        else:
            print('动态库加载失败！')


