from ftplib import FTP
import os

class FTPClient(object):

    def __init__(self,user,password,host,port=21):
        self.ftp_conn=FTP()
        self.ftp_conn.connect(host, port)
        self.ftp_conn.login(user, password)

    def download(self,path,filename,bufsize=8192):
        '''
        :param path: 下载路径
        :param filename: 下载文件名，带路径
        :param bufsize: 下载块大小
        :return: None
        '''
        local_file=os.path.join(path,os.path.basename(filename))
        with open(local_file, 'wb') as fp:
            # 注意RETR后面的空格
            # 接收服务器上的文件并写入本地
            self.ftp_conn.retrbinary('RETR ' + filename, fp.write, bufsize)



    def upload(self,path,filename,bufsize=8192):
        '''
        :param path: 上传路径
        :param filename: 上传文件，带路径
        :param bufsize: 上传块大小
        :return: None
        '''
        remote_file=os.path.join(path,os.path.basename(filename))
        with open(filename, 'rb') as fp:
            # 注意STOR后面的空格
            # 上传文件
            flag=self.ftp_conn.storbinary('STOR ' + remote_file, fp, bufsize)
            print("flag:%s" %flag)
            return flag


    def close(self):
        if self.ftp_conn:
            self.ftp_conn.quit()



if __name__=="__main__":
    ftp=FTPClient("admin","admin","10.8.200.201",21)
    # 测试下载
    #ftp.download("d:/","/2015/2015-03/2015-03-05/130650078.pdf")
    # 测试下载
    #ftp.upload("/2013/2013-05/2013-05-01/","d:/60.pdf")