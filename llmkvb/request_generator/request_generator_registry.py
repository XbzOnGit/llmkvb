from llmkvb.request_generator.synthetic_request_generator import (
    SyntheticRequestGenerator,
)
from llmkvb.request_generator.trace_replay_request_generator import (
    TraceReplayRequestGenerator,
)
from llmkvb.kvtypes import RequestGeneratorType
from llmkvb.utils.base_registry import BaseRegistry


class RequestGeneratorRegistry(BaseRegistry):
    @classmethod
    def get_key_from_str(cls, key_str: str) -> RequestGeneratorType:
        return RequestGeneratorType.from_str(key_str)


RequestGeneratorRegistry.register(
    RequestGeneratorType.SYNTHETIC, SyntheticRequestGenerator
)
RequestGeneratorRegistry.register(
    RequestGeneratorType.TRACE_REPLAY, TraceReplayRequestGenerator
)