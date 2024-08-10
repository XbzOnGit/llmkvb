from abc import ABC, abstractmethod
from typing import List, Tuple


class BaseNewStringGenerator(ABC):
    def __init__(self, config: dict):
        self._config = config

    @abstractmethod
    def generate_new_string(self, **kwargs) -> Tuple[int, List[Tuple[int, int]]]:
        pass
