from multiprocessing import Queue
from flask import send_file,make_response,request,jsonify,render_template,abort
from api.exception import *
from api.model import *
import os,ujson,time
import mimetypes

# 任务队列
task_queue = Queue()

# 初始化视图
def init_views(app,db):
    '''
    :param app:         应用程序本身
    :return:
    '''

    # HTML 报告生成 医生总检审核完成
    # PDF 报告生成，护理审阅完成
    @app.route('/api/report/create/<string:filetype>/<int:tjbh>', methods=['POST'])
    def report_create(filetype,tjbh):
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = tjbh
        pass

    # HTML 报告删除 医生取消审核
    # PDF 报告删除，护理取消审阅
    @app.route('/api/report/delete/<string:filetype>/<int:tjbh>', methods=['POST'])
    def report_delete(filetype,tjbh):
        pass

    # HTML 报告预览 用户发起
    # PDF 报告预览，用户发起
    @app.route('/api/report/preview/<string:filetype>/<int:tjbh>', methods=['GET'])
    def report_preview(filetype,tjbh):
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = str(tjbh)
        else:
            abort(404)
        if filetype =='html':      # request 请求
            abort(404)
        elif filetype =='pdf':     # report 报告
            result = db.session.query(MT_TJ_FILE_ACTIVE.filename).filter(MT_TJ_FILE_ACTIVE.tjbh == tjbh,
                                                                MT_TJ_FILE_ACTIVE.filetype == 'report').scalar()
            if result:
                print("http://10.8.200.201:8080/web/viewer.html?file=/tmp/%s" % result)
                return "http://10.8.200.201:8080/web/viewer.html?file=/tmp/%s" % result
        else:
            abort(404)

    # PDF 报告下载，用户发起
    @app.route('/api/report/down/pdf/<int:tjbh>', methods=['POST'])
    def report_down(tjbh):
        pass

    # PDF 报告下载，用户发起
    @app.route('/api/report/print/pdf/<int:tjbh>', methods=['GET'])
    def report_print(tjbh):
        pass

    # 设备 预览
    @app.route('/api/equip/preview/<int:equip_file>/<int:tjbh>', methods=['POST'])
    def equip_preview(equip_file,tjbh):
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = str(tjbh)

        pass

    # 设备 报告下载
    @app.route('/api/equip/down/<int:equip_file>/<int:tjbh>', methods=['POST'])
    def equip_down(equip_file,tjbh):
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = tjbh
        pass

    # 文件上传
    @app.route('/api/file/upload/', methods=['POST'])
    def file_upload():
        cur_path = get_cur_path(app.config['UPLOAD_FOLDER_PHOTO'])
        file_obj = request.files['file']
        user = request.headers['User']
        file_prefix, file_suffix = os.path.splitext(os.path.split(file_obj.filename)[1])
        new_file=os.path.join(cur_path, os.path.basename(file_obj.filename))
        file_obj.save(new_file)
        try:
            # 获取插入的SQL 更新 TJ_FILE_ACTIVE
            result = db.session.query(MT_TJ_FILE_ACTIVE).filter(MT_TJ_FILE_ACTIVE.tjbh == file_prefix[0:9],
                                                                MT_TJ_FILE_ACTIVE.filetype == file_prefix[-6:]).scalar()
            if result:
                db.session.delete(result)
            db.session.execute(get_file_upload_sql(new_file))
            db.session.commit()
        except Exception as e:
            print('更新失败！错误信息：%s' %e)
        if file_prefix[-6]=='000001':
            # 采血的照片，固定
            pass
        return ujson.dumps({'code':1,'mes':'上传成功','data':None})

    # 文件下载
    @app.route('/api/file/down/<int:tjbh>/<string:filetype>', methods=['GET'])
    def file_down(tjbh,filetype):
        '''
        :param tjbh:        体检编号
        :param filetype:    文件类型
        :return:
        '''
        result = db.session.query(MT_TJ_FILE_ACTIVE).filter(MT_TJ_FILE_ACTIVE.tjbh == tjbh,MT_TJ_FILE_ACTIVE.filetype == filetype).scalar()
        if result:
            response = make_response(send_file(result.localfile,as_attachment=True))
            response.headers['Content-Type'] = mimetypes.guess_type(result.filename)[0]
            response.headers['Content-Disposition'] = 'attachment; filename={}'.format(result.filename)
            return response
        else:
            return make_response("Not Found File")

            #return ujson.dumps({'code':1,'mes':'上传成功','data':None})

    # 程序更新
    @app.route('/api/version/<float:version>', methods=['GET'])
    def update_version(version):
        print('客户端：%s 更新请求，客户端版本号：%s' % (request.remote_addr,str(version)))
        result = db.session.query(MT_TJ_UPDATE).filter(MT_TJ_UPDATE.version >version).scalar()
        if result:
            response = make_response(send_file(result.ufile, as_attachment=True))
            response.headers['Content-Type'] = mimetypes.guess_type(result.ufile)[0]
            response.headers['Content-Disposition'] = 'attachment; filename={}'.format(result.ufile)
            return response
        else:
            abort(404)

    # @app.errorhandler(404)
    # def page_not_found(error):
    #     return render_template('404.html'), 404

    @app.errorhandler(BaseError)
    def custom_error_handler(e):
        if e.level in [BaseError.LEVEL_WARN, BaseError.LEVEL_ERROR]:
            if isinstance(e, OrmError):
                app.logger.exception('%s %s' % (e.parent_error, e))
            else:
                app.logger.exception('错误信息: %s %s' % (e.extras, e))
        response = jsonify(e.to_dict())
        response.status_code = e.status_code
        return response



# 获得当日的保存目录
def get_cur_path(dirname):
    dday = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    dyear = dday[0:4]
    dmonth = dday[0:7]
    cur_path = '%s%s/%s/%s/' %(dirname,dyear,dmonth,dday)
    if not os.path.exists(cur_path):
        os.makedirs(cur_path)

    return cur_path

def cur_datetime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

# 获得文件上传的SQL
def get_file_upload_sql(filename):
    file_prefix, file_suffix = os.path.splitext(os.path.split(filename)[1])
    dday = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    dyear = dday[0:4]
    dmonth = dday[0:7]
    sql = '''
    INSERT INTO TJ_FILE_ACTIVE(TJBH,DWBH,RYEAR,RMONTH,RDAY,LOCALFILE,FILENAME,FILETYPE,CREATETIME) 
    VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s') 
    ''' %(file_prefix[0:9],file_prefix[0:5],dyear,dmonth,dday,filename,os.path.split(filename)[1],file_prefix[-6:],cur_datetime())
    return sql