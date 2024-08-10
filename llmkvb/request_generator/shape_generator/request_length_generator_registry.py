from llmkvb.request_generator.shape_generator.fixed_request_length_generator import (
    FixedRequestLengthGenerator,
)
from llmkvb.request_generator.shape_generator.trace_request_length_generator import (
    TraceRequestLengthGenerator,
)
from llmkvb.request_generator.shape_generator.uniform_request_length_generator import (
    UniformRequestLengthGenerator,
)
from llmkvb.request_generator.shape_generator.zipf_request_length_generator import (
    ZipfRequestLengthGenerator,
)
from llmkvb.kvtypes import RequestLengthGeneratorType
from llmkvb.utils.base_registry import BaseRegistry


class RequestLengthGeneratorRegistry(BaseRegistry):
    @classmethod
    def get_key_from_str(cls, key_str: str) -> RequestLengthGeneratorType:
        return RequestLengthGeneratorType.from_str(key_str)


RequestLengthGeneratorRegistry.register(
    RequestLengthGeneratorType.ZIPF, ZipfRequestLengthGenerator
)
RequestLengthGeneratorRegistry.register(
    RequestLengthGeneratorType.UNIFORM, UniformRequestLengthGenerator
)
RequestLengthGeneratorRegistry.register(
    RequestLengthGeneratorType.TRACE, TraceRequestLengthGenerator
)
RequestLengthGeneratorRegistry.register(
    RequestLengthGeneratorType.FIXED, FixedRequestLengthGenerator
)
