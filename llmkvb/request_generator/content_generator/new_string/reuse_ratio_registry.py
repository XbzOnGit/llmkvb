from llmkvb.request_generator.distribution_generator.normal_generator import NormalGenerator
from llmkvb.request_generator.distribution_generator.uniform_generator import UniformGenerator

from llmkvb.kvtypes import ReuseRatioGeneratorType
from llmkvb.utils.base_registry import BaseRegistry

class ReuseRatioGeneratorRegistry(BaseRegistry):
    @classmethod
    def get_key_from_str(cls, key_str: str) -> ReuseRatioGeneratorType:
        return ReuseRatioGeneratorType.from_str(key_str)

ReuseRatioGeneratorRegistry.register(ReuseRatioGeneratorType.UNIFORM, UniformGenerator)
ReuseRatioGeneratorRegistry.register(ReuseRatioGeneratorType.NORMAL, NormalGenerator)


