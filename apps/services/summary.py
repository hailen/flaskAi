import time

import config.env
from apps.services import logger, REQUEST_TIMEOUT

import requests

from apps.tasks.celery import celery


### 调用大模型进行中英文互译


@celery.task(bind=True, name='async_summary', rate_limit='30/m')
def async_summary_task(self, text):
    try:
        """
        :param text: 汇总文本

        """
        # 调用大模型的API接口进行总结操作
        # 构造总结请求的 API URL和请求头
        api_url = config.env.LLMS_API_URL
        headers = {'Authorization': config.env.LLMS_API_URL}
        payload = {
            'text': text,
        }

        # 发送总结请求，设置超时时间
        logger.info(f"发送总结请求: {payload}")
        response = requests.post(api_url, headers=headers, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()  # 如果响应码不是 200，将引发异常

        # 解析响应数据
        data = response.json()

        summary_text = data.get('summary_text', '')

        logger.info(f"总结成功: {summary_text}")
        return summary_text


    except TimeoutError:
        # 任务执行超时，进行重试
        logger.error("请求超时，正在重试...")
        raise self.retry(countdown=5, max_retries=3)
    except requests.exceptions.RequestException as e:
        # 超时重试
        logger.error(f"请求异常: {e}, 正在重试...")
        raise self.retry(countdown=5, max_retries=3)

    except Exception as e:
        # 通用异常
        logger.exception("任务执行失败")
        raise self.retry(exc=e)
