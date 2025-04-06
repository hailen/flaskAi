# flaskAi

使用 flask 实现一个小型 AI 应用后端接口

```shell
pip install -r requirement.txt
```

```shell
flask run

```

```shell
celery -A apps.tasks.celery worker --loglevel=info --concurrency=4 -P eventlet
```

```text
http://127.0.0.1:5000/docs  #  获取所有功能列表接口
```
