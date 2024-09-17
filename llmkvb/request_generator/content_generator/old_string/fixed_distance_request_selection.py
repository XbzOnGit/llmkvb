from llmkvb.request_generator.content_generator.old_string.base_request_selection import BaseRequestSelectionGenerator
import sys
class FixedDistanceRequestSelectionGenerator(BaseRequestSelectionGenerator):
    def __init__(self, config):
        super().__init__(config)
        self._pool_size = 0
        self._fixed_distance = config['distance']
    def update(self, **kwargs) -> None:
        self._pool_size += 1
    def request_selection(self, **kwargs) -> int:
        assert self._pool_size > 0, "pool size should be greater than 0"
        max_distance = kwargs.get("max_distance", None)
        the_distance = self._fixed_distance
        if max_distance is not None:
            if self._fixed_distance > max_distance:
                print(f"WARNING: FIXED distance from {self._fixed_distance} to {max_distance}", file=sys.stderr)
                the_distance = max_distance
        return self._pool_size - the_distance
        
