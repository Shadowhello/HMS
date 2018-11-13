from flask import send_file,make_response,request,jsonify,abort,url_for
from app_api.exception import *
from app_api.model import *
import zeep,json,base64,os,ujson,time,urllib.parse,requests
import mimetypes,subprocess
from utils import gol,str2
from app_api.dbconn import *
import win32api
import win32print

# 初始化视图
def init_views(app,db,print_queue=None,report_queue=None):

    '''
    :param app:         应用程序本身
    :return:
    '''
    @app.route("/")
    def static_create():
        return url_for('static', filename='/css/report.css')

    # 获取彩超、内镜图像
    @app.route('/api/pacs/pic/<string:tjbh>/<string:ksbm>/<string:xmbh>', methods=['POST'])
    def get_pacs_pic(tjbh, ksbm,xmbh):
        url = "http://10.8.200.220:7059/WebGetFileView.asmx?WSDL"
        client = zeep.Client(url)
        try:
            result = json.loads(client.service.f_GetUISFilesByTJ_IID(tjbh + xmbh))
            #filenames = []
            if result['IsSuccess'] == 'true':
                sql = "DELETE FROM TJ_PACS_PIC WHERE tjbh='%s' and zhbh ='%s';" % (tjbh, xmbh)
                db.session.execute(sql)
                pic_datas = result['Datas']
                count = 0
                for pic_data in pic_datas:
                    count = count + 1
                    pic_name = '%s_%s_%s.jpg' % (tjbh, xmbh, count)
                    pic_pk = '%s%s' % (tjbh, xmbh)
                    filename = os.path.join("D:\space\pic",pic_name )
                    with open(filename, "wb") as f:
                        f.write(base64.b64decode(pic_data))

                    sql = "INSERT INTO TJ_PACS_PIC(TJBH,KSBM,PICPATH,PICNAME,ZHBH,PATH,PK)VALUES('%s','%s','%s','%s','%s','%s','%s')" %(
                        tjbh,ksbm,pic_name,pic_name,xmbh,pic_name,pic_pk
                    )
                    db.session.execute(sql)
                    # filenames.append(filename)
                return ujson.dumps({'code': 1, 'mes': '图片传输成功', 'data': ''})
            abort(404)
        except Exception as e:
            print(e)
            abort(404)

    #二维码生成
    # @app.route('/api/qrcode/post?tjbh=<string:tjbh>&xm=<string:xm>&sfzh=<string:sfzh>&sjhm=<string:sjhm>&login_id=<string:login_id>', methods=['POST'])
    @app.route('/api/qrcode/<string:tjbh>/<string:login_id>', methods=['GET'])
    def qrcode_create(tjbh,login_id):
        print(' %s：客户端(%s)：微信二维码请求！参数 tjbh：%s，login_id：%s' % (cur_datetime(), request.remote_addr, tjbh, login_id))
        user = get_user_info(tjbh,db)
        if user:
            url = 'http://10.7.200.60:80/tjadmin/pInfoSubmit'
            #url = 'http://10.7.200.27:8089/tjadmin/pInfoSubmit'
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
        if report_queue:
            # print('%s 队列插入消息：%s' %(cur_datetime(),ujson.dumps(mes_obj)))
            report_queue.put(mes_obj)
        else:
            abort(404)
        if filetype=='html':
            return ujson.dumps({'code': 1, 'mes': 'HTML报告生成', 'data': ''})
        elif filetype=='pdf':
            # 审阅完成
            return ujson.dumps({'code': 1, 'mes': 'PDF报告生成', 'data': ''})
        else:
            abort(404)

    # HTML 报告删除 医生取消审核
    # PDF 报告删除，护理取消审阅
    @app.route('/api/report/delete/<string:filetype>/<int:tjbh>/<string:login_id>/<string:czlx>', methods=['GET','POST'])
    def report_delete(filetype,tjbh,login_id,czlx):
        print(' %s：客户端(%s)：%s报告取消审核请求！参数 tjbh：%s，login_id：%s，czlx：%s' % (cur_datetime(), request.remote_addr, filetype, tjbh, login_id,czlx))
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = str(tjbh)
        else:
            abort(404)
        if filetype=='html':
            # 审核取消
            try:
                sql1 = " UPDATE TJ_TJDJB SET TJZT='%s' WHERE TJBH = '%s' ;" %(tjbh,czlx)
                db.session.execute(sql1)
                if czlx =='5':
                    sql2 = " UPDATE TJ_BGGL SET BGZT='0',BGTH='0' WHERE TJBH = '%s' ;" % tjbh
                    db.session.execute(sql2)
            except Exception as e:
                print(e)
            return ujson.dumps({'code': 1, 'mes': '取消审核，删除HTML报告成功', 'data': ''})
        elif filetype=='pdf':
            # 审阅完成
            # 审核取消
            try:
                sql1 = "UPDATE TJ_TJDJB SET TJZT='%s' WHERE TJBH = '%s' " %(tjbh,czlx)
                sql2 = "UPDATE TJ_BGGL SET BGZT='0',BGTH='1' WHERE TJBH = '%s' " % tjbh
                db.session.execute(sql1)
                db.session.execute(sql2)
            except Exception as e:
                print(e)
            return ujson.dumps({'code': 1, 'mes': '取消审阅，删除PDF报告成功', 'data': ''})
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
                # print("http://10.8.200.201:8080/web/viewer.html?file=/tmp/%s" % result)
                return "http://10.8.200.201:8080/web/viewer.html?file=/tmp/%s" % result
        else:
            abort(404)

    # PDF 报告下载，用户发起
    @app.route('/api/report/down/pdf/<int:tjbh>', methods=['GET'])
    def report_down(tjbh):
        print(' %s：客户端(%s)：%s报告下载请求！' % (cur_datetime(), request.remote_addr,tjbh))
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = str(tjbh)
        else:
            abort(404)
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
        return api_file_down(url)


    # PDF 报告打印，用户发起
    @app.route('/api/report/print/pdf/<int:tjbh>/<string:printer>', methods=['POST'])
    def report_print(tjbh,printer):
        print(' %s：客户端(%s)：%s报告打印请求！' % (cur_datetime(), request.remote_addr, tjbh))
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = str(tjbh)
        else:
            abort(404)
        result = db.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).scalar()
        if result:
            if result.bglj:
                filename = os.path.join(result.bglj,"%s.pdf" %tjbh)
                if os.path.exists(filename):
                    mes_obj = {'filename': filename, 'action': 'print', 'printer': printer}
                    if print_queue:
                        print_queue.put(mes_obj)
                        return ujson.dumps({'code': 1, 'mes': '报告打印成功！', 'data': ''})

        # else:
            # 历史
        session = gol.get_value('tj_cxk')
        result = session.query(MT_TJ_PDFRUL).filter(MT_TJ_PDFRUL.TJBH == tjbh).order_by(MT_TJ_PDFRUL.CREATETIME.desc()).scalar()
        if result:
            filename = os.path.join('D:/pdf/',result.PDFURL)
        else:
            filename = os.path.join('D:/tmp/','%s.pdf' %tjbh)
            url = "http://10.8.200.201:4000/api/file/down/%s/%s" % (tjbh, 'report')
            request_get(url,filename)
        if os.path.exists(filename):
            mes_obj = {'filename': filename, 'action': 'print','printer':printer}
            if print_queue:
                print_queue.put(mes_obj)
                return ujson.dumps({'code': 1, 'mes': '报告打印成功！', 'data': ''})
            else:
                abort(404)
            # result= print_pdf_gsprint(filename,printer)
            # if result==0:
            #     return ujson.dumps({'code': 1, 'mes': '报告打印成功！', 'data': ''})
            # else:
            #     return ujson.dumps({'code': 0, 'mes': '报告打印失败！', 'data': ''})
        else:
            abort(404)

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
        results = db.session.query(MT_TJ_FILE_ACTIVE).filter(MT_TJ_FILE_ACTIVE.tjbh == tjbh,MT_TJ_FILE_ACTIVE.filetype == filetype).order_by(desc(MT_TJ_FILE_ACTIVE.createtime)).all()
        if results:
            filename = results[0].localfile
            # print(results[0].localfile)
            # response = make_response(send_file(results[0].localfile,as_attachment=True))
            # response.headers['Content-Type'] = mimetypes.guess_type(results[0].filename)[0]
            # response.headers['Content-Disposition'] = 'attachment; filename={}'.format(results[0].filename)
            # return response
            # 返回下载
            response = make_response(send_file(filename, as_attachment=True))
            response.headers['Content-Type'] = mimetypes.guess_type(os.path.basename(filename))[0]
            response.headers['Content-Disposition'] = 'attachment; filename={}'.format(os.path.basename(filename))
            return response
        else:
            abort(404)

    # 程序更新
    @app.route('/api/version_file/<string:platform>/<float:version>', methods=['GET'])
    def update_file(platform,version):
        print(' %s：(%s)客户端(%s)：版本文件下载请求！当前版本号：%s' % (cur_datetime(),platform,request.remote_addr, str(version)))
        if platform=='win7':
            platform_name ='1'
        else:
            platform_name = '0'
        result = db.session.query(MT_TJ_UPDATE).filter(MT_TJ_UPDATE.version >version,MT_TJ_UPDATE.platform==platform_name).scalar()
        if result:
            response = make_response(send_file(result.ufile, as_attachment=True))
            response.headers['Content-Type'] = mimetypes.guess_type(result.ufile)[0]
            response.headers['Content-Disposition'] = 'attachment; filename={}'.format(result.ufile)
            return response
        else:
            abort(404)

    # 程序更新
    @app.route('/api/version/<string:platform>/<float:version>', methods=['GET'])
    def update_version(platform, version):
        print(' %s：(%s)客户端(%s)：版本更新请求！当前版本号：%s' % (cur_datetime(), platform, request.remote_addr, str(version)))
        if platform == 'win7':
            platform_name = '1'
        else:
            platform_name = '0'
        result = db.session.query(MT_TJ_UPDATE).filter(MT_TJ_UPDATE.version > version,
                                                       MT_TJ_UPDATE.platform == platform_name).scalar()
        if result:
            return ujson.dumps({'version': result.version, 'describe': str2(result.describe)})
        else:
            abort(404)

    # 图片识别出文字
    @app.route('/api/pic2txt/', methods=['POST'])
    def pic2txt():
        file_obj = request.files['file']
        print(' %s：客户端(%s)：OCR服务请求：%s' % (cur_datetime(), request.remote_addr,file_obj.filename))
        url = "http://10.7.200.127:10006/api/pic2txt/"
        try:
            response = requests.post(url, files=request.files)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print('URL：%s 请求失败！错误信息：%s' % (url, e))
            abort(404)

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
    # print(sql)
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


def print_pdf_gsprint(filename,printer=None):
    if not printer:
        printer = win32print.GetDefaultPrinter()
    command =r'gsprint -color -printer "%s" %s' %(printer,filename)
    result = subprocess.run(command, shell=True)
    return result.returncode

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