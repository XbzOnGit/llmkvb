from abc import ABC, abstractmethod
from typing import Tuple



class BaseRequestLengthGenerator(ABC):
    def __init__(self, config: dict):
        self._config = config

    @abstractmethod
    def get_next_num_tokens(self) -> Tuple[float, float]:
        pass
