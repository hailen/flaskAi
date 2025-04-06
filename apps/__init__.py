import os
from json import JSONEncoder

from flask import Flask

from config import config
from extends import register_extends


def create_app():
    # 模式
    config_name = os.getenv('FLASK_ENV', 'development')
    app = Flask(__name__)
    # 设置应用配置
    app.config.from_object(config[config_name])
    # 序列化处理
    app.json_encoder = JSONEncoder

    # 初始化扩展
    register_extends(app)



    return app
