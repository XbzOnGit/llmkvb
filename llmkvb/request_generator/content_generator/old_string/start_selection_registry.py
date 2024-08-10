from llmkvb.request_generator.content_generator.old_string.uniform_start_selection import UniformStartSelectionGenerator
from llmkvb.kvtypes import StartSelectionGeneratorType
from llmkvb.utils.base_registry import BaseRegistry

class StartSelectionGeneratorRegistry(BaseRegistry):
    @classmethod
    def get_key_from_str(cls, key_str: str) -> StartSelectionGeneratorType:
        return StartSelectionGeneratorType.from_str(key_str)

StartSelectionGeneratorRegistry.register(StartSelectionGeneratorType.UNIFORM, UniformStartSelectionGenerator)