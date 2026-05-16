import requests
from .base_client import AbstractAIClient


class AnthropicClient(AbstractAIClient):
    def __init__(self, config: dict):
        super().__init__(config)
        self.api_key = config.get('api_key', '')
        self.base_url = config.get('base_url', 'https://api.anthropic.com').rstrip('/')
        self.model = config.get('model', 'claude-sonnet-4-20250514')
        self.api_version = config.get('api_version', '2023-06-01')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 8192)
        self.timeout = config.get('timeout', 120)

    def chat(self, messages: list) -> str:
        url = f"{self.base_url}/v1/messages"
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
            'anthropic-version': self.api_version
        }

        system_msg = None
        filtered_messages = []
        for msg in messages:
            if msg['role'] == 'system':
                system_msg = msg['content']
            else:
                filtered_messages.append(msg)

        payload = {
            'model': self.model,
            'messages': filtered_messages,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature
        }
        if system_msg:
            payload['system'] = system_msg

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()
        content_blocks = data.get('content', [])
        text_parts = []
        for block in content_blocks:
            if block.get('type') == 'text':
                text_parts.append(block.get('text', ''))
        return '\n'.join(text_parts)

    def validate_connection(self) -> tuple:
        try:
            self.chat([
                {'role': 'user', 'content': 'Hello'}
            ])
            return True, '连接成功'
        except Exception as e:
            return False, str(e)
