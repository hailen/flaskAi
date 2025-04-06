import os
from config.env import REDIS_HOST, REDIS_PORT


# 全局配置
class BaseConfig(object):
    DEBUG = False
    TESTING = False
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    REDIS_URI = "redis://{}:{}".format(REDIS_HOST, REDIS_PORT)


# 开发环境
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = 'development'


# 测试环境
class TestingConfig(BaseConfig):
    DEBUG = True
    ENV = 'testing'


# 生产环境
class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV = 'production'
