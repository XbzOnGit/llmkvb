from llmkvb.kvtypes import BaseIntEnum

class RequestIntervalGeneratorType(BaseIntEnum):
    POISSON = 1
    GAMMA = 2
    STATIC = 3
    TRACE = 4
    FIXED = 5
