from .base_client import AbstractAIClient
from .openai_compat_client import OpenAICompatClient
from .anthropic_client import AnthropicClient


class UnknownProviderError(Exception):
    pass


def create_client(config: dict) -> AbstractAIClient:
    provider = config.get('current_provider', 'openai_compat')
    return create_client_by_provider(config, provider)


def create_client_by_provider(config: dict, provider: str) -> AbstractAIClient:
    provider_config = config.get('providers', {}).get(provider, config)

    if provider in ('openai_compat', 'deepseek', 'custom'):
        base = provider_config.get('base_url', '')
        if provider == 'deepseek' and not base:
            provider_config = dict(provider_config)
            provider_config['base_url'] = 'https://api.deepseek.com'
        return OpenAICompatClient(provider_config)
    elif provider == 'anthropic':
        return AnthropicClient(provider_config)
    else:
        raise UnknownProviderError(f"未知的AI提供商: {provider}")
