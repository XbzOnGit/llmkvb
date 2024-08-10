# Select from a sequence, like ycsb.
# Can implement a uniform first.
# Pass in nothing, just call update to put new requests inside.
from abc import ABC, abstractmethod

class BaseRequestSelectionGenerator(ABC):
    def __init__(self, config: dict):
        self._config = config
    @abstractmethod
    def update(self, **kwargs) -> None:
        pass
    @abstractmethod
    def request_selection(self, **kwargs) -> int:
        pass
