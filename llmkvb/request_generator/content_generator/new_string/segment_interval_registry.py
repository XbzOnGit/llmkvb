from llmkvb.request_generator.distribution_generator.normal_generator import NormalGenerator
from llmkvb.request_generator.distribution_generator.uniform_generator import UniformGenerator

from llmkvb.kvtypes import SegmentIntervalGeneratorType
from llmkvb.utils.base_registry import BaseRegistry

class SegmentIntervalGeneratorRegistry(BaseRegistry):
    @classmethod
    def get_key_from_str(cls, key_str: str) -> SegmentIntervalGeneratorType:
        return SegmentIntervalGeneratorType.from_str(key_str)

SegmentIntervalGeneratorRegistry.register(SegmentIntervalGeneratorType.UNIFORM, UniformGenerator)
SegmentIntervalGeneratorRegistry.register(SegmentIntervalGeneratorType.NORMAL, NormalGenerator)


