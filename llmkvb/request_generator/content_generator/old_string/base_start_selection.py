from abc import ABC, abstractmethod



class BaseStartSelectionGenerator(ABC):
    def __init__(self, config: dict):
        self._config = config
    @abstractmethod
    def select(self, **kwargs) -> int:
        pass
