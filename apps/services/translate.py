
import config.env
from apps.services import logger, REQUEST_TIMEOUT

import requests

from apps.tasks.celery import celery


### 调用大模型进行中英文互译


@celery.task(bind=True, name='async_translation', rate_limit='30/m')
def async_translation_task(self, text, source_lang, target_lang):
    try:
        """
        :param text: 需要翻译的文本
        :param source_lang: zh/en 源文本类型
        :param target_lang: zh/en 目标文本类型
        
        """
        # 调用大模型的API接口进行翻译操作
        # 构造翻译请求的 API URL和请求头
        api_url = config.env.LLMS_API_URL
        headers = {'Authorization': config.env.LLMS_API_URL}
        payload = {
            'text': text,
            'source_lang': source_lang,
            'target_lang': target_lang
        }

        # 发送翻译请求，设置超时时间
        logger.info(f"发送翻译请求: {payload}")
        response = requests.post(api_url, headers=headers, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()  # 如果响应码不是 200，将引发异常

        # 解析响应数据
        data = response.json()
        translated_text = data.get('translated_text', '')

        logger.info(f"翻译成功: {translated_text}")
        return translated_text


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
