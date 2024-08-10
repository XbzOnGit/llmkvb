from llmkvb.request_generator.shape_generator.synthetic_request_shape_generator import (
    SyntheticRequestShapeGenerator,
)
from llmkvb.request_generator.shape_generator.trace_replay_request_shape_generator import (
    TraceReplayRequestShapeGenerator,
)

from llmkvb.kvtypes import RequestShapeGeneratorType
from llmkvb.utils.base_registry import BaseRegistry


class RequestShapeGeneratorRegistry(BaseRegistry):
    @classmethod
    def get_key_from_str(cls, key_str: str) -> RequestShapeGeneratorType:
        return RequestShapeGeneratorType.from_str(key_str)


RequestShapeGeneratorRegistry.register(
    RequestShapeGeneratorType.SYNTHETIC, SyntheticRequestShapeGenerator
)
RequestShapeGeneratorRegistry.register(
    RequestShapeGeneratorType.TRACE_REPLAY, TraceReplayRequestShapeGenerator
)
