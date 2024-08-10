from llmkvb.request_generator.distribution_generator.normal_generator import NormalGenerator
from llmkvb.request_generator.distribution_generator.uniform_generator import UniformGenerator

from llmkvb.kvtypes import SegmentLengthGeneratorType
from llmkvb.utils.base_registry import BaseRegistry

class SegmentLengthGeneratorRegistry(BaseRegistry):
    @classmethod
    def get_key_from_str(cls, key_str: str) -> SegmentLengthGeneratorType:
        return SegmentLengthGeneratorType.from_str(key_str)

SegmentLengthGeneratorRegistry.register(SegmentLengthGeneratorType.UNIFORM, UniformGenerator)
SegmentLengthGeneratorRegistry.register(SegmentLengthGeneratorType.NORMAL, NormalGenerator)


