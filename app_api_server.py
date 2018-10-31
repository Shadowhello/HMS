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
from multiprocessing import Process, Queue
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
    # 全局进程队列
    gol_process_queue = Queue()
    report_process = Process(target=report_run_api, args=(gol_process_queue,))
    # 启动报告服务
    report_process.start()
    # 初始化
    Init_env_vars(['api.ini'])
    gol.set_value('tj_cxk',get_oracle_session(gol.get_value('SQLALCHEMY_DATABASE_URI2')))
    # monkey.patch_all()
    app = create_app()

    db.init_app(app)
    init_views(app,db,gol_process_queue)

    # 获取全局变量
    HOST = gol.get_value('api_host')
    PORT = gol.get_value('api_port')
    app.logger.info('API(%s:%s)服务启动......' % (HOST, str(PORT)))
    # 运行应用
    server_on_tornado_run(app,HOST,PORT)

