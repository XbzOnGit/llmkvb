import json
class Request:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def convert_tokens_to_string(self, tokenizer):
        self.string = tokenizer.convert_tokens_to_string(self.tokens)
        del self.tokens
    def dump_json_line_string(self) -> str:
        return json.dumps(self.__dict__) + "\n"
