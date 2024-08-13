from abc import ABC, abstractmethod
import sys
class BaseExecutor(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def execute(self):
        pass