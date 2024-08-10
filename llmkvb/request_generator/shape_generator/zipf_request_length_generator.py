from typing import Tuple

from llmkvb.request_generator.shape_generator.base_request_length_generator import (
    BaseRequestLengthGenerator,
)
from llmkvb.utils.zipf_generator import ZipfGenerator


class ZipfRequestLengthGenerator(BaseRequestLengthGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._zipf_generator = ZipfGenerator(
            self._config["min_tokens"],
            self._config["max_tokens"],
            self._config["theta"],
            self._config["scramble"],
            self._config["seed"],
        )

    def get_next_num_tokens(self) -> Tuple[float, float]:
        total_tokens = self._zipf_generator.next()

        decode_tokens = total_tokens / (
            1 + self._config["prefill_to_decode_ratio"]
        )
        prefill_tokens = total_tokens - decode_tokens

        return prefill_tokens, decode_tokens
