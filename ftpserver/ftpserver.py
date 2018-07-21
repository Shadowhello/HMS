from pyftpdlib.authorizers import DummyAuthorizer,AuthenticationFailed
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer,ThreadedFTPServer
from hashlib import md5
import os,logging
from logging.handlers import TimedRotatingFileHandler
from utils import gol
from utils.envir2 import Init_env_vars

class MyAuthorizer(DummyAuthorizer):

    #加密功能
    def validate_authentication(self, username, password, handler):
        password = md5(password.encode('latin1'))
        hash = md5(password).hexdigest()
        try:
            if self.user_table[username]['pwd'] != hash:
                raise KeyError
        except KeyError:
            raise AuthenticationFailed


class MyHandler(FTPHandler):

    def __init__(self, conn, server, ioloop=None):
        super(MyHandler,self).__init__(conn, server, ioloop)

    # 客户端连接时调用
    def on_connect(self):
        super(MyHandler, self).on_connect()

    # 客户端断开时调用
    def on_disconnect(self):
        super(MyHandler, self).on_disconnect()

    # 用户登录时调用
    def on_login(self,username):
        super(MyHandler,self).on_login(username)

    # 用户登录失败时调用
    def on_login_failed(self,username, password):
        super(MyHandler, self).on_login_failed(username, password)
        self.log('账户(%s)登录失败！'%username)

    # 传输成功时调用，file就是文件名,即客户端下载成功,更新主程序
    def on_file_sent(self,file):
        super(MyHandler, self).on_file_sent(file)
        self.log("客户端(%s:%s),下载文件 %s 成功！" %(self.remote_ip,self.remote_port,file))

    # 接收成功时候调用，file就是文件名,即客户端上传成功,
    def on_file_received(self,file):
        super(MyHandler, self).on_file_received(file)
        self.log("客户端(%s:%s),上传文件 %s 成功！" %(self.remote_ip,self.remote_port,file))

    # 没有被完整发送的时候调用
    def on_incomplete_file_sent(self,file):
        super(MyHandler, self).on_incomplete_file_sent(file)

    # 没有完整接收的时候调用
    def on_incomplete_file_received(self,file):
        super(MyHandler, self).on_incomplete_file_received(file)
        os.remove(file)

def run_ftp_server(para=None):
    # 初始化参数
    server_ip = gol.get_value('ftp_ip')
    server_port = gol.get_value('ftp_port')
    server_model = gol.get_value('ftp_model')
    masquerade_ip = gol.get_value('ftp_masquerade_ip')
    passive_ports = gol.get_value('ftp_passive_ports')
    max_cons = gol.get_value('ftp_max_cons')
    max_cons_per_ip = gol.get_value('ftp_max_cons_per_ip')

    # FTP日志
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    log_handler = TimedRotatingFileHandler(filename='ftpserver.log',
                                       when='d',
                                       interval=1,
                                       backupCount=7)
    formatter = logging.Formatter('[%(asctime)s-%(levelname)s] - %(message)s')
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)


    #实例化虚拟用户，这是FTP验证首要条件
    authorizer = DummyAuthorizer()

    #添加用户
    for i in ['update','pdf','equip']:
        user = gol.get_value('%s_user' %i)
        passwd = gol.get_value('%s_passwd' % i)
        path = gol.get_value('%s_path' % i)
        perm = gol.get_value('%s_perm' % i)
        # 添加用户权限和路径，括号内的参数是(用户名， 密码， 用户目录， 权限)
        authorizer.add_user(user, passwd, path, perm=perm)

    # 匿名账户
    # authorizer.add_anonymous("D:/")
    #初始化ftp句柄
    handler = MyHandler
    handler.authorizer = authorizer
    handler.max_login_attempts=20

    # 如果你在NAT之后，就用这个指定被动连接的参数
    if  not masquerade_ip:
        logger.info("FTP服务：主动模式！")
    else:
        handler.masquerade_address = masquerade_ip
        handler.passive_ports =  [int(i) for i in passive_ports]
        logger.info("FTP服务：被动模式！端口号：%s" %handler.passive_ports)

    # handler.passive_ports =range(10000,10005)
    #是否启用FXP特性，也就是文件交换协议，从此FTP服务器到另外的FTP服务器，默认False
    # handler.permit_foreign_addresses=True

    # 上传下载速度限制
    # dtp_handler = ThrottledDTPHandler
    # dtp_handler.read_limit = 30720  # 30 Kb/sec (30 * 1024)
    # dtp_handler.write_limit = 30720  # 30 Kb/sec (30 * 1024)
    # handler.dtp_handler = dtp_handler

    address = (server_ip,server_port)
    if server_model:
        server = ThreadedFTPServer(address, handler)
    else:
        server = FTPServer(address, handler)

    server.max_cons = int(max_cons)  # 给链接设置限制
    server.max_cons_per_ip = int(max_cons_per_ip)
    #开始服务
    server.serve_forever()

if __name__ =="__main__":
    Init_env_vars(['ftp.ini'])
    run_ftp_server()