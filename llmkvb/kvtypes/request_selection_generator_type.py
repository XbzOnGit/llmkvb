from llmkvb.kvtypes import BaseIntEnum

class RequestSelectionGeneratorType(BaseIntEnum):
    UNIFORM = 1
    LATEST = 2
    FIXED_DISTANCE = 3

