import requests
from .base_client import AbstractAIClient


class OpenAICompatClient(AbstractAIClient):
    def __init__(self, config: dict):
        super().__init__(config)
        self.api_key = config.get('api_key', '')
        self.base_url = config.get('base_url', 'https://api.openai.com/v1').rstrip('/')
        self.model = config.get('model', 'gpt-4o')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 4096)
        self.timeout = config.get('timeout', 120)

    def chat(self, messages: list) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        payload = {
            'model': self.model,
            'messages': messages,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens
        }
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()
        choices = data.get('choices', [])
        if not choices:
            return ''
        return choices[0].get('message', {}).get('content', '')

    def validate_connection(self) -> tuple:
        try:
            response = self.chat([
                {'role': 'user', 'content': 'Hello'}
            ])
            return True, '连接成功'
        except Exception as e:
            return False, str(e)
