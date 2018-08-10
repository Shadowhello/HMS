from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from app_api.config import create_app
from app_api.views import init_views
from app_api.model import db
from utils.envir2 import Init_env_vars
from utils import gol
from app_api.dbconn import *

def run_api_server(app,host,port):
    # 异步
    http_server = WSGIServer((host,port), app,handler_class=WebSocketHandler)
    http_server.serve_forever()


if __name__ == '__main__':
    # 初始化
    Init_env_vars(['api.ini'])
    gol.set_value('tj_cxk',get_oracle_session(gol.get_value('SQLALCHEMY_DATABASE_URI2')))
    monkey.patch_all()
    app = create_app()
    db.init_app(app)
    init_views(app,db)

    # 获取全局变量
    HOST = gol.get_value('api_host')
    PORT = gol.get_value('api_port')
    app.logger.info('API(%s:%s)服务启动......' % (HOST, str(PORT)))
    # 运行应用
    run_api_server(app,HOST,PORT)

