from abc import ABC, abstractmethod


class BaseDistributionGenerator(ABC):
    def __init__(self, *args, **kwargs):
        if args:
            self.config = args[0]
        else:
            self.config = kwargs.get('config', None)

    @abstractmethod
    def get_number(self, **kwargs):
        pass
