from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from app_api.config import create_app
from app_api.views import init_views
from app_api.model import db
from utils.envir2 import Init_env_vars
from utils import gol
from app_api.dbconn import *
import multiprocessing
from multiprocessing import Process, Queue,Pool
from report_build_start import report_run_api
import ujson
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

def server_on_gevent_run(app,host,port):
    # 异步
    http_server = WSGIServer((host,port), app,handler_class=WebSocketHandler)
    http_server.serve_forever()

def server_on_tornado_run(app,host,port):
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(port,host)
    IOLoop.instance().start()

if __name__ == '__main__':
    import cgitb
    cgitb.enable(logdir="./error/",format="text")
    multiprocessing.freeze_support()
    Init_env_vars(['api.ini'])
    # 全局进程队列
    gol_print_queue = Queue()
    gol_report_queue = Queue()
    process_print_num = gol.get_value('process_print_num', 3)
    process_report_num = gol.get_value('process_report_num', 3)
    ##############打印进程########################
    for i in range(process_print_num):
        print_process = Process(target=report_run_api, args=(gol_print_queue,),name="报告生成进程%s" %str(i+1))
        # 启动报告服务
        print_process.start()
    ##############报告进程########################
    for i in range(process_report_num):
        report_process = Process(target=report_run_api, args=(gol_report_queue,),name="报告生成进程%s" %str(i+1))
        # 启动报告服务
        report_process.start()
    ##############创建进程组####################
    # p = Pool(processes=process_count)
    # for i in range(process_count):
    #     p.apply_async(report_run_api,(gol_process_queue,))  # 向进程池添加任务

    gol.set_value('tj_cxk',get_oracle_session(gol.get_value('SQLALCHEMY_DATABASE_URI2')))
    # monkey.patch_all()
    app = create_app()

    db.init_app(app)
    init_views(app,db,gol_print_queue,gol_report_queue)
    # 获取全局变量
    HOST = gol.get_value('api_host')
    PORT = gol.get_value('api_port')
    app.logger.info('API(%s:%s)服务启动......' % (HOST, str(PORT)))
    # 运行应用
    # server_on_tornado_run(app,'10.7.200.101',5005)
    server_on_tornado_run(app, HOST, PORT)

