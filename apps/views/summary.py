from flask_restx import reqparse, Namespace, fields, Resource
from apps.services.summary import async_summary_task

ns = Namespace('Summary',
               description='总结接口',
               path='/summary')


summary_model = ns.model('Summary', {
    'text': fields.String(required=True, min_length=1,max_length=2000, description='总结文本'),
})

result_model = ns.model('AsyncResult', {
    'task_id': fields.String(description='异步任务ID'),
    'status_url': fields.String(description='状态查询地址')
})


@ns.route('/submit', methods=['POST'])
class SummaryAPI(Resource):
    @ns.expect(summary_model)
    @ns.marshal_with(result_model, code=202)
    @ns.response(202, '任务已提交')
    def post(self):
        """总结接口"""
        # 业务逻辑调用services层
        payload = ns.payload
        task = async_summary_task.apply_async([payload['text'],])
        return {
            'task_id': task.id,
            'status_url': f"/summary/tasks/{task.id}/status"
        }, 202


# 任务状态查询接口
@ns.route('/tasks/<string:task_id>/status')
class TaskStatus(Resource):
    @ns.doc(params={'task_id': '异步任务ID'})
    def get(self, task_id):
        """查询任务状态"""
        task = async_summary_task.AsyncResult(task_id)

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
