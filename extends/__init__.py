from apps.views import namespaces
from extends.extends_dotenv import init_dotenv
from extends.extends_flask_restx import restx_api


def register_extends(app):

    # 初始化配置文件
    init_dotenv()
    # 初始化flask-restx
    restx_api.init_app(app)
    # 注册命名空间
    for ns in namespaces:
        restx_api.add_namespace(ns)
