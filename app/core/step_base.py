"""Step base class without Qt dependencies. Uses callbacks instead of Signals."""

from ..ai.client_factory import create_client
from ..ai.retry_handler import execute_with_retry, MaxRetriesExceededError
from ..ai.base_client import AbstractAIClient


class AbstractStep:
    def __init__(self, step_index, step_name, context, project_manager, config,
                 on_progress=None, on_log=None, on_completed=None):
        self.step_index = step_index
        self.step_name = step_name
        self.context = context
        self.project_manager = project_manager
        self.config = config
        self._cancelled = False
        self._on_progress = on_progress
        self._on_log = on_log
        self._on_completed = on_completed

    def run(self):
        self._log('INFO', f'[{self.step_name}] 开始执行...')
        self._progress(0, f'开始: {self.step_name}')

        try:
            self.context = self.execute()
            self._progress(100, f'完成: {self.step_name}')
            self._log('INFO', f'[{self.step_name}] 执行完成')
            if self._on_completed:
                self._on_completed(self.step_index, True, self.context)
            return self.context
        except MaxRetriesExceededError as e:
            error_msg = str(e)
            self._log('ERROR', f'[{self.step_name}] {error_msg}')
            if self._on_completed:
                self._on_completed(self.step_index, False, error_msg)
            raise
        except Exception as e:
            error_msg = str(e)
            self._log('ERROR', f'[{self.step_name}] 执行失败: {error_msg}')
            if self._on_completed:
                self._on_completed(self.step_index, False, error_msg)
            raise

    def execute(self):
        raise NotImplementedError("子类必须实现execute方法")

    def cancel(self):
        self._cancelled = True

    def _call_ai(self, system_prompt, user_prompt, progress_start=10, progress_end=90):
        self._progress(progress_start, '正在连接AI...')

        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]

        max_retries = self.config.get('max_retries', 3)
        timeout = self.config.get('timeout', 120)

        def on_retry(msg):
            self._log('WARN', msg)

        def do_chat():
            client = create_client(self.config)
            return client.chat(messages)

        response = execute_with_retry(do_chat, max_retries=max_retries,
                                      timeout=timeout, on_retry=on_retry)
        self._progress(progress_end, 'AI响应完成')
        return response

    def _write_output(self, sub_dir, filename, content):
        return self.project_manager.write_file(self.step_index, sub_dir, filename, content)

    def _log(self, level, message):
        if self._on_log:
            self._on_log(self.step_index, level, message)

    def _progress(self, percent, message=''):
        if self._on_progress:
            self._on_progress(self.step_index, percent, message)
