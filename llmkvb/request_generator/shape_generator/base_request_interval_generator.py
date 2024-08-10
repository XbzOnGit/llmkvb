from abc import ABC, abstractmethod



class BaseRequestIntervalGenerator(ABC):
    def __init__(self, config: dict):
        self._config = config

    @abstractmethod
    def get_next_inter_request_time(self) -> float:
        pass
