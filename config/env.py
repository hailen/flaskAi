import os

# 应用运行地址
FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
# 应用运行端口
FLASK_PORT = os.getenv('FLASK_PORT', 5000)
# 应用启动文件
FLASK_APP = os.getenv('FLASK_APP', 'app.py')
# 应用环境变量
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
# 是否调试模式
FLASK_DEBUG = (os.getenv('FLASK_DEBUG', 'True') == 'True')


# 缓存服务地址
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
# 缓存服务端口
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

# 大模型URL
LLMS_API_URL = os.getenv('LLMS_API_URL', 'xxxxxxxxxxxxx')
# 大模型key
LLMS_API_KEY = os.getenv('LLMS_API_KEY', 'xxxxxxxxxxxxxxx')
