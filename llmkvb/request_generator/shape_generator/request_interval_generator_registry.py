from llmkvb.request_generator.shape_generator.gamma_request_interval_generator import (
    GammaRequestIntervalGenerator,
)
from llmkvb.request_generator.shape_generator.poisson_request_interval_generator import (
    PoissonRequestIntervalGenerator,
)
from llmkvb.request_generator.shape_generator.static_request_interval_generator import (
    StaticRequestIntervalGenerator,
)
from llmkvb.request_generator.shape_generator.trace_request_interval_generator import (
    TraceRequestIntervalGenerator,
)
from llmkvb.request_generator.shape_generator.fixed_request_interval_generator import (
    FixedRequestIntervalGenerator,
)
from llmkvb.kvtypes import RequestIntervalGeneratorType
from llmkvb.utils.base_registry import BaseRegistry


class RequestIntervalGeneratorRegistry(BaseRegistry):
    @classmethod
    def get_key_from_str(cls, key_str: str) -> RequestIntervalGeneratorType:
        return RequestIntervalGeneratorType.from_str(key_str)


RequestIntervalGeneratorRegistry.register(
    RequestIntervalGeneratorType.GAMMA, GammaRequestIntervalGenerator
)
RequestIntervalGeneratorRegistry.register(
    RequestIntervalGeneratorType.POISSON, PoissonRequestIntervalGenerator
)
RequestIntervalGeneratorRegistry.register(
    RequestIntervalGeneratorType.STATIC, StaticRequestIntervalGenerator
)
RequestIntervalGeneratorRegistry.register(
    RequestIntervalGeneratorType.TRACE, TraceRequestIntervalGenerator
)
RequestIntervalGeneratorRegistry.register(
    RequestIntervalGeneratorType.FIXED, FixedRequestIntervalGenerator
)