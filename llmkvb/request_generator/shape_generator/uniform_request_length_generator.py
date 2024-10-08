import math
import random
from typing import Tuple

from llmkvb.request_generator.shape_generator.base_request_length_generator import (
    BaseRequestLengthGenerator,
)


class UniformRequestLengthGenerator(BaseRequestLengthGenerator):
    def get_next_num_tokens(self) -> Tuple[float, float]:
        total_tokens = random.uniform(
            self._config["min_tokens"],
            self._config["max_tokens"]
        )

        decode_tokens = math.ceil(
            total_tokens
            / (1 + self._config["prefill_to_decode_ratio"])
        )
        prefill_tokens = total_tokens - decode_tokens
        assert prefill_tokens > 0 and decode_tokens > 0

        return prefill_tokens, decode_tokens
