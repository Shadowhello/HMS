from flask import send_file,make_response,request,jsonify,abort,url_for
from app_api.exception import *
from app_api.model import *
import os,ujson,time,urllib.parse,requests
import mimetypes
from utils import gol,str2
from app_api.dbconn import *
import win32api
import win32print

# 初始化视图
def init_views(app,db,queue=None):

    '''
    :param app:         应用程序本身
    :return:
    '''

    @app.route("/")
    def static_create():
        return url_for('static', filename='/css/report.css')

    #二维码生成
    # @app.route('/api/qrcode/post?tjbh=<string:tjbh>&xm=<string:xm>&sfzh=<string:sfzh>&sjhm=<string:sjhm>&login_id=<string:login_id>', methods=['POST'])
    @app.route('/api/qrcode/<string:tjbh>/<string:login_id>', methods=['GET'])
    def qrcode_create(tjbh,login_id):
        print(' %s：客户端(%s)：微信二维码请求！参数 tjbh：%s，login_id：%s' % (cur_datetime(), request.remote_addr, tjbh, login_id))
        user = get_user_info(tjbh,db)
        if user:
            url = 'http://10.7.200.27:8080/tjadmin/pInfoSubmit'
            head = {}
            head['realName'] = urllib.parse.quote(user['xm'])
            head['idCardNum'] = user['sfzh']
            head['phoneNumber'] = user['sjhm']
            head['email'] = ''
            head['address'] = ''
            head['Content-Type'] = 'application/json'
            try:
                response = requests.post(url, headers=head)
                if response.status_code == 200:
                    # f = open(r'C:\Users\Administrator\Desktop\pdf测试\1.png', "wb")
                    # for chunk in response.iter_content(chunk_size=512):
                    #     if chunk:
                    #         f.write(chunk)
                    # f.close()
                    return response.content
                else:
                    abort(404)
            except Exception as e:
                print("微信二维码请求失败！")
                abort(404)
        else:
            abort(404)

    # HTML 报告生成 医生总检审核完成
    # PDF 报告生成，护理审阅完成
    @app.route('/api/report/create/<string:filetype>/<int:tjbh>/<string:login_id>', methods=['GET','POST'])
    def report_create(filetype,tjbh,login_id):
        print(' %s：客户端(%s)：%s报告生成请求！参数 tjbh：%s，login_id：%s'  % (cur_datetime(), request.remote_addr,filetype, tjbh, login_id))
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = str(tjbh)
        else:
            abort(404)
        mes_obj = {'tjbh':tjbh,'action':filetype}
        if queue:
            # print('%s 队列插入消息：%s' %(cur_datetime(),ujson.dumps(mes_obj)))
            queue.put(mes_obj)
        if filetype=='html':
            return ujson.dumps({'code': 1, 'mes': 'HTML报告生成', 'data': ''})
        elif filetype=='pdf':
            # 审阅完成
            return ujson.dumps({'code': 1, 'mes': 'PDF报告生成', 'data': ''})
        else:
            abort(404)

    # HTML 报告删除 医生取消审核
    # PDF 报告删除，护理取消审阅
    @app.route('/api/report/delete/<string:filetype>/<int:tjbh>/<string:login_id>', methods=['GET','POST'])
    def report_delete(filetype,tjbh,login_id):
        print(' %s：客户端(%s)：%s报告取消审核请求！参数 tjbh：%s，login_id：%s' % (cur_datetime(), request.remote_addr, filetype, tjbh, login_id))
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = str(tjbh)
        else:
            abort(404)
        if filetype=='html':
            # 审核取消
            try:
                sql1 = "UPDATE TJ_TJDJB SET TJZT='4' WHERE TJBH = '%s' " % tjbh
                sql2 = "UPDATE TJ_BGGL SET BGZT='0',BGTH='0' WHERE TJBH = '%s' " % tjbh
                db.session.execute(sql1)
                db.session.execute(sql2)
            except Exception as e:
                print()
            return ujson.dumps({'code': 1, 'mes': '取消审核，HTML报告删除', 'data': ''})
        elif filetype=='pdf':
            # 审阅完成
            # 审核取消
            try:
                sql1 = "UPDATE TJ_TJDJB SET TJZT='4' WHERE TJBH = '%s' " % tjbh
                sql2 = "UPDATE TJ_BGGL SET BGZT='0',BGTH='1' WHERE TJBH = '%s' " % tjbh
                db.session.execute(sql1)
                db.session.execute(sql2)
                db.commit()
            except Exception as e:
                db.rollback()
            return ujson.dumps({'code': 1, 'mes': '取消审阅，PDF报告删除', 'data': ''})
        else:
            abort(404)

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
            sql = "select bglj from tj_bggl where tjbh='%s';" %tjbh
            result = db.session.execute(sql).scalar()
            if result:
                filename = os.path.join(result,'%s.html' %tjbh)
                if os.path.exists(filename):
                    return send_file(filename)

            abort(404)
        elif filetype =='pdf':     # report 报告
            result = db.session.query(MT_TJ_FILE_ACTIVE.filename).filter(MT_TJ_FILE_ACTIVE.tjbh == tjbh,MT_TJ_FILE_ACTIVE.filetype == 'report').scalar()
            if result:
                print("http://10.8.200.201:8080/web/viewer.html?file=/tmp/%s" % result)
                return "http://10.8.200.201:8080/web/viewer.html?file=/tmp/%s" % result
        else:
            abort(404)

    # PDF 报告下载，用户发起
    @app.route('/api/report/down/pdf/<int:tjbh>', methods=['GET'])
    def report_down(tjbh):
        print(' %s：客户端(%s)：%s报告下载请求！' % (cur_datetime(), request.remote_addr,tjbh))
        # 当前
        result = db.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).scalar()
        if result:
            filename = os.path.join(result.bglj,"%s.pdf" %tjbh)
            if os.path.exists(filename):
                # 返回下载
                response = make_response(send_file(filename, as_attachment=True))
                response.headers['Content-Type'] = mimetypes.guess_type(os.path.basename(filename))[0]
                response.headers['Content-Disposition'] = 'attachment; filename={}'.format(os.path.basename(filename))
                return response

        # 历史
        session = gol.get_value('tj_cxk')
        result = session.query(MT_TJ_PDFRUL).filter(MT_TJ_PDFRUL.TJBH == tjbh).order_by(MT_TJ_PDFRUL.CREATETIME.desc()).scalar()
        if result:
            filename = os.path.join('D:/pdf/',result.PDFURL)
            if os.path.exists(filename):
                #返回下载
                response = make_response(send_file(filename, as_attachment=True))
                response.headers['Content-Type'] = mimetypes.guess_type(os.path.basename(filename))[0]
                response.headers['Content-Disposition'] = 'attachment; filename={}'.format(os.path.basename(filename))
                return response

        # 向历史的报告服务发送请求
        url = "http://10.8.200.201:4000/api/file/down/%s/%s" %(tjbh,'report')
        api_file_down(url)


    # PDF 报告打印，用户发起
    @app.route('/api/report/print/pdf/<int:tjbh>/<string:printer>', methods=['POST'])
    def report_print(tjbh,printer):
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = str(tjbh)
        else:
            abort(404)
        result = db.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).scalar()
        if result:
            filename = os.path.join(result.bglj,"%s.pdf" %tjbh)
        else:
            # 历史
            session = gol.get_value('tj_cxk')
            result = session.query(MT_TJ_PDFRUL).filter(MT_TJ_PDFRUL.TJBH == tjbh).order_by(MT_TJ_PDFRUL.CREATETIME.desc()).scalar()
            if result:
                filename = os.path.join('D:/pdf/',result.PDFURL)
            else:
                filename = os.path.join('D:/tmp/','%s.pdf' %tjbh)
                url = "http://10.8.200.201:4000/api/file/down/%s/%s" % (tjbh, 'report')
                request_get(url,filename)

        if print_pdf(filename,printer):
            return ujson.dumps({'code': 1, 'mes': '报告打印成功！', 'data': ''})
        else:
            return ujson.dumps({'code': 0, 'mes': '报告打印失败！', 'data': ''})

    # 设备 预览
    @app.route('/api/equip/preview/<string:equip_file>/<string:tjbh>', methods=['POST'])
    def equip_preview(equip_file,tjbh):
        pass

    # 设备 报告下载
    @app.route('/api/equip/down/<int:equip_file>/<int:tjbh>', methods=['POST'])
    def equip_down(equip_file,tjbh):
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = tjbh
        pass

    # 设备 报告上传
    @app.route('/api/equip/upload/', methods=['POST'])
    def equip_upload():
        cur_path = get_cur_path(app.config['UPLOAD_FOLDER_EQUIP'])
        file_obj = request.files['file']
        new_file=os.path.join(cur_path, os.path.basename(file_obj.filename))
        file_obj.save(new_file)
        # 返回上传路径
        file_type = os.path.basename(file_obj.filename)[-3:]
        if file_type =='_08':
            print('%s 心电图：%s 文件上传成功！' %(cur_datetime(),new_file))
        elif file_type =='_01':
            print('%s 电测听：%s 文件上传成功！' %(cur_datetime(),new_file))
        elif file_type =='_04':
            print('%s 骨密度：%s 文件上传成功！' %(cur_datetime(),new_file))
        return ujson.dumps({'code': 1, 'mes': '上传成功', 'data': new_file})

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
    @app.route('/api/file/down/<string:tjbh>/<string:filetype>', methods=['GET'])
    def file_down(tjbh,filetype):
        '''
        :param tjbh:        体检编号
        :param filetype:    文件类型
        :return:
        '''
        result = db.session.query(MT_TJ_FILE_ACTIVE).filter(MT_TJ_FILE_ACTIVE.tjbh == tjbh,MT_TJ_FILE_ACTIVE.filetype == filetype).order_by(desc(MT_TJ_FILE_ACTIVE.createtime)).scalar()
        if result:
            response = make_response(send_file(result.localfile,as_attachment=True))
            response.headers['Content-Type'] = mimetypes.guess_type(result.filename)[0]
            response.headers['Content-Disposition'] = 'attachment; filename={}'.format(result.filename)
            return response
        else:
            abort(404)

    # 程序更新
    @app.route('/api/version/<float:version>', methods=['GET'])
    def update_version(version):
        print(' %s：客户端(%s)：版本更新请求！当前版本号：%s' % (cur_datetime(), request.remote_addr, str(version)))
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

# 获取前缀、后缀名称
def get_pre_suf(filename):
    return os.path.splitext(os.path.basename(filename))

# 获得用户信息二维码
def get_user_info(tjbh,db):
    sql = "select XM,SFZH,SJHM FROM TJ_TJDAB WHERE DABH = (SELECT DABH FROM TJ_TJDJB where TJBH='%s') ;" %tjbh
    print(sql)
    results = db.session.execute(sql).fetchall()
    if results:
        result = results[0]
        if all([result[1],result[2]]):
            return {'xm':str2(result[0]),'sfzh':result[1],'sjhm':result[2]}
        else:
            return {}
    else:
        return {}

def api_file_down(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        abort(404)


def print_pdf(filename,printer=None):
    try:
        if printer:
            win32api.ShellExecute(0, 'print', filename, printer, '.', 0)
            return True
        else:
            win32api.ShellExecute(0, 'print', filename, win32print.GetDefaultPrinter(), '.', 0)
            return True
    except Exception as e:
        print('打印失败！错误信息：%s \n 处理方式：请安装PDF阅读器 AcroRd32.exe 并设置为默认打开方式。')
        return False

def request_get(url,save_file=None):
    '''
    :param url:             请求地址
    :param save_file:       下载文件 save_file
    :return:
    '''
    response = requests.get(url)
    if response.status_code==200:
        try:
            f = open(save_file, "wb")
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
            f.close()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False