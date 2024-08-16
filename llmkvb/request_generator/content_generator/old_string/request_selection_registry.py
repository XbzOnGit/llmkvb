from llmkvb.request_generator.content_generator.old_string.uniform_request_selection import UniformRequestSelectionGenerator
from llmkvb.request_generator.content_generator.old_string.latest_request_selection import LatestRequestSelectionGenerator
from llmkvb.kvtypes import RequestSelectionGeneratorType
from llmkvb.utils.base_registry import BaseRegistry

class RequestSelectionGeneratorRegistry(BaseRegistry):
    @classmethod
    def get_key_from_str(cls, key_str: str) -> RequestSelectionGeneratorType:
        return RequestSelectionGeneratorType.from_str(key_str)

RequestSelectionGeneratorRegistry.register(RequestSelectionGeneratorType.UNIFORM, UniformRequestSelectionGenerator)
RequestSelectionGeneratorRegistry.register(RequestSelectionGeneratorType.LATEST, LatestRequestSelectionGenerator)