from llmkvb.request_generator.distribution_generator.normal_generator import NormalGenerator
from llmkvb.request_generator.distribution_generator.uniform_generator import UniformGenerator

from llmkvb.kvtypes import PrefixRatioGeneratorType
from llmkvb.utils.base_registry import BaseRegistry


class PrefixRatioGeneratorRegistry(BaseRegistry):
    @classmethod
    def get_key_from_str(cls, key_str: str) -> PrefixRatioGeneratorType:
        return PrefixRatioGeneratorType.from_str(key_str)

PrefixRatioGeneratorRegistry.register(PrefixRatioGeneratorType.UNIFORM, UniformGenerator)
PrefixRatioGeneratorRegistry.register(PrefixRatioGeneratorType.NORMAL, NormalGenerator)

