import time
import random
import requests


RETRYABLE_STATUSES = {429, 500, 502, 503, 504}
NON_RETRYABLE_STATUSES = {400, 401, 403, 404, 405, 422}


class MaxRetriesExceededError(Exception):
    def __init__(self, original_error, attempts):
        self.original_error = original_error
        self.attempts = attempts
        super().__init__(f"重试{attempts}次后仍然失败: {original_error}")


def execute_with_retry(func, max_retries=3, timeout=120, on_retry=None):
    last_exception = None
    for attempt in range(max_retries + 1):
        try:
            return func()
        except requests.Timeout as e:
            last_exception = e
            msg = f"请求超时({timeout}秒)"
            if attempt < max_retries:
                msg += f"，正在第{attempt + 1}次重试..."
            if on_retry:
                on_retry(msg)
        except requests.HTTPError as e:
            status = e.response.status_code if e.response is not None else 0
            if status in NON_RETRYABLE_STATUSES:
                if status == 401:
                    raise MaxRetriesExceededError(
                        ValueError("API密钥无效或未授权，请检查设置"), attempt + 1
                    )
                elif status == 403:
                    raise MaxRetriesExceededError(
                        ValueError("API权限不足，请检查账户权限"), attempt + 1
                    )
                elif status == 404:
                    raise MaxRetriesExceededError(
                        ValueError(f"API接口地址不存在: {e.response.url}"), attempt + 1
                    )
                elif status == 400:
                    raise MaxRetriesExceededError(
                        ValueError(f"请求参数错误: {e.response.text[:200]}"), attempt + 1
                    )
                raise
            last_exception = e
            msg = f"服务器错误({status})"
            if attempt < max_retries:
                msg += f"，正在第{attempt + 1}次重试..."
            if on_retry:
                on_retry(msg)
        except requests.ConnectionError as e:
            last_exception = e
            msg = "网络连接失败，请检查网络"
            if attempt < max_retries:
                msg += f"，正在第{attempt + 1}次重试..."
            if on_retry:
                on_retry(msg)
        except Exception as e:
            raise

        if attempt < max_retries:
            delay = (2 ** attempt) * (0.75 + random.random() * 0.5)
            time.sleep(delay)

    raise MaxRetriesExceededError(last_exception, max_retries + 1)
