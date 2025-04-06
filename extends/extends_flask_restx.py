from flask_restx import Api

restx_api = Api(
    version='1.0',
    title='AI Service API',
    description='基于大模型的RESTful API',
    doc='/docs',  # 启用Swagger UI
)