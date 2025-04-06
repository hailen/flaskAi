from celery import Celery
from config.env import REDIS_HOST, REDIS_PORT

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'


celery = Celery(__name__, broker=CELERY_BROKER_URL)
celery.conf.update(result_backend=CELERY_RESULT_BACKEND)