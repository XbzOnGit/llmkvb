from typing import Tuple

from llmkvb.request_generator.shape_generator.base_request_length_generator import (
    BaseRequestLengthGenerator,
)


class FixedRequestLengthGenerator(BaseRequestLengthGenerator):
    def get_next_num_tokens(self) -> Tuple[float, float]:
        return (
            self._config["prefill_tokens"],
            self._config["decode_tokens"],
        )
