from llmkvb.kvtypes.base_int_enum import BaseIntEnum

# STNTHETIC can also be generated from a trace with shape and custom rules indicating reuse part.
# which should behave the same with TRACE_REPLAY one.
class RequestGeneratorType(BaseIntEnum):
    SYNTHETIC = 1
    TRACE_REPLAY = 2