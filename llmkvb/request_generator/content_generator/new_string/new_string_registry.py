from llmkvb.kvtypes import NewStringGeneratorType
from llmkvb.utils.base_registry import BaseRegistry
from llmkvb.request_generator.content_generator.new_string.segment_new_string import SegmentNewStringGenerator

class NewStringGeneratorRegistry(BaseRegistry):
    @classmethod
    def get_key_from_str(cls, key_str: str) -> NewStringGeneratorType:
        return NewStringGeneratorType.from_str(key_str)

NewStringGeneratorRegistry.register(NewStringGeneratorType.SEGMENT_NEW_STRING, SegmentNewStringGenerator)

