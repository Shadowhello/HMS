#from utils.readparas import GolParasMixin
from .tjsd_ui import *
from .model import *
from utils.api import APIRquest

class TJSD(GolParasMixin,TJSD_UI):

    def __init__(self):
        super(TJSD,self).__init__("导检收单")
        self.init()
        self.initParas()
        # 绑定信号槽
        self.le_tjbh.returnPressed.connect(self.on_le_tjbh_press)
        self.camera.photo_take.connect(self.on_btn_photo_take)
        #self.camera.photo_see.connect(self.on_btn_photo_see)

    def initParas(self):
        # 上传队列
        self.queue_upload = Queue()
        self.api = APIRquest(self.login_id,self.api_host,self.api_port,self.log)
        self.api_file_upload_url = gol.get_value('api_file_upload')
        if self.camera:
            # 如果摄像头打开了，则开启上传线程
            self.timer_upload_thread = ThreadUpload(self.queue_upload,self.api,self.api_file_upload_url,self.log)
            self.timer_upload_thread.start()

    def on_le_tjbh_press(self):
        if not self.le_tjbh.text():
            mes_about(self, '请输入体检编号！')
            return
        # 人员信息
        result = self.session.query(MV_RYXX).filter(MV_RYXX.tjbh == self.le_tjbh.text()).scalar()
        if result:
            self.gp_user.setData(result.to_dict)
        else:
            mes_about(self, '不存在，请确认后重新输入！')
            self.gp_user.clearData()
        # 项目结果
        results = self.session.execute(get_item_state_sql(tjbh=self.le_tjbh.text())).fetchall()
        self.table_item_state.load(results)
        self.gp_middle_bottom.setTitle('项目状态 (%s)' % self.table_item_state.rowCount())
        # 设置图片名称
        self.camera.set_save_file(image_file(self.le_tjbh.text()))

    # 拍照
    def on_btn_photo_take(self,filename):
        if self.gp_user.user_id:
            if filename=="tmp.png":
                pass
            else:
                self.queue_upload.put(filename)
        else:
            mes_about(self,'请扫描体检编号或者条码号！')

def image_file(tjbh):
    filename=os.path.join('%s' %gol.get_value('path_tmp') ,'%s_000002.%s' %(tjbh,gol.get_value('photo_save_type')))
    return filename