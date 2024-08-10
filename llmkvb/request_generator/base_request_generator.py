from abc import ABC, abstractmethod
from typing import List
from llmkvb.entities import Request
import sys
class BaseRequestGenerator(ABC):
    def __init__(self, config: dict):
        self.config = config
        if "tokenizer_type" not in self.config:
            raise ValueError("tokenizer_type is not specified in the trace config file.")
        if self.config["tokenizer_type"] not in ["transformers"]:
            raise ValueError("tokenizer_type is not supported.")
        self.tokenizer_type: str = self.config["tokenizer_type"]
        self.tokenizer = None
        if self.tokenizer_type == "transformers":
            import transformers
            local_files_only= "local_files_only" in self.config and self.config["local_files_only"]
            self.tokenizer = transformers.AutoTokenizer.from_pretrained(self.config["tokenizer_name"], local_files_only=local_files_only)
        if "content_type" not in self.config:
            raise ValueError("content_type is not specified in the trace config file.")
        if self.config["content_type"] not in ["tokens", "string"]:
            raise ValueError("content_type is not supported.")
        self.content_type: str = self.config["content_type"]
        self.trace_output_file = None
        if "trace_output_file" in self.config:
            self.trace_output_file = self.config["trace_output_file"]
            

    @abstractmethod
    def generate_requests(self) -> List[Request]:
        pass

    def generate(self) -> List[Request]:
        requests = self.generate_requests()
        # Do not concatenate on dump.
        # It is more convinient to dump just tokens for vidur.
        # For real serving systems, should convert tokens into string first.
        if self.content_type != "tokens":
            assert self.content_type == "string"
            for request in requests:
                request.convert_tokens_to_string(self.tokenizer)
        try:
            if self.trace_output_file is not None:
                # Dump as jsonl.
                with open(self.trace_output_file, 'w') as f:
                    for request in requests:
                        f.write(request.dump_json_line_string())
        except:
            print("No dump_trace or no trace_file specified in the trace config file.", file=sys.stderr)
        return requests
        