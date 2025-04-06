from flask_restx import Namespace, Resource, fields, Api

from apps.services.translate import async_translation_task

ns = Namespace('Translate',
               description='中英互译接口',
               path='/translate')

translation_model = ns.model('Translation', {
    'text': fields.String(required=True, min_length=1, max_length=2000, description='文本'),
    'source_lang': fields.String(enum=['zh', 'en'], description='源文本语言'),
    'target_lang': fields.String(enum=['en', 'zh'], description='目标文本语言')
})

result_model = ns.model('AsyncResult', {
    'task_id': fields.String(description='异步任务ID'),
    'status_url': fields.String(description='状态查询地址')
})


@ns.route('/zh-en', methods=['POST'])
class TranslationAPI(Resource):
    @ns.expect(translation_model)
    @ns.marshal_with(result_model, code=202)
    @ns.response(202, '任务已提交')
    def post(self):
        """中译英接口"""
        # 业务逻辑调用services层
        payload = ns.payload
        task = async_translation_task.apply_async(args=[payload['text'], payload.get('source_lang', 'zh'), payload.get('target_lang', 'en')])
        return {
            'task_id': task.id,
            'status_url': f"/translate/status/{task.id}"
        }, 202


# 任务状态查询接口
@ns.route('/tasks/<string:task_id>/status')
class TaskStatus(Resource):
    @ns.doc(params={'task_id': '异步任务ID'})
    def get(self, task_id):
        """查询翻译任务状态"""
        task = async_translation_task.AsyncResult(task_id)

        response = {
            'task_id': task.id,
            'state': task.state,
            'status': '任务正在处理中'
        }

        if task.state == 'SUCCESS':
            response['status'] = '任务成功'
            response['result'] = task.result
        elif task.state == 'FAILURE':
            response['status'] = '任务失败'
            response['error'] = str(task.info)

        return response
