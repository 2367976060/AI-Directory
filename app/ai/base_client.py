from abc import ABC, abstractmethod


class AbstractAIClient(ABC):
    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def chat(self, messages: list) -> str:
        ...

    @abstractmethod
    def validate_connection(self) -> tuple:
        ...
