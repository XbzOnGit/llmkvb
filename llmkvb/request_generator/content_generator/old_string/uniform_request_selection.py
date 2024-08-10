from scipy.stats import uniform
from llmkvb.request_generator.content_generator.old_string.base_request_selection import BaseRequestSelectionGenerator
class UniformRequestSelectionGenerator(BaseRequestSelectionGenerator):
    def __init__(self, config):
        super().__init__(config)
        self._pool_size = 0
    def update(self, **kwargs) -> None:
        self._pool_size += 1
    def request_selection(self, **kwargs) -> int:
        assert self._pool_size > 0, "pool size should be greater than 0"
        max_distance = kwargs.get("max_distance", None)
        st = 0
        sc = self._pool_size
        if max_distance is not None:
            assert max_distance > 0, "max_distance should be greater than 0"
            if max_distance < self._pool_size:
                st = self._pool_size - max_distance
                sc = max_distance
        else:
            max_distance = self._pool_size
        unform_dist = uniform(loc=st, scale=sc)
        retval = int(unform_dist.rvs())
        while retval >= max_distance:
            retval = int(unform_dist.rvs())
        return retval
        
