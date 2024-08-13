from llmkvb.executor.vidur_executor import VidurExecutor
from llmkvb.kvtypes import ExecutorType
from llmkvb.utils.base_registry import BaseRegistry

class ExecutorRegistry(BaseRegistry):
    @classmethod
    def get_key_from_str(cls, key_str: str) -> ExecutorType:
        return ExecutorType.from_str(key_str)

ExecutorRegistry.register(ExecutorType.VIDUR, VidurExecutor)