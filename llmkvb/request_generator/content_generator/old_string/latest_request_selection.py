from llmkvb.request_generator.content_generator.old_string.base_request_selection import BaseRequestSelectionGenerator
from llmkvb.utils.zipf_generator import ZipfGenerator

class LatestRequestSelectionGenerator(BaseRequestSelectionGenerator):
    def __init__(self, config):
        super().__init__(config)
        self._pool_size = 0
        self._theta = config.get("theta", 0.99)
        self._seed = config.get("seed", 42)
    def update(self, **kwargs) -> None:
        self._pool_size += 1
    def request_selection(self, **kwargs) -> int:
        assert self._pool_size > 0, "pool size should be greater than 0"
        zipf_gen = ZipfGenerator(0, self._pool_size - 1, self._theta, False, self._seed)
        return self._pool_size - 1 - zipf_gen.next()
