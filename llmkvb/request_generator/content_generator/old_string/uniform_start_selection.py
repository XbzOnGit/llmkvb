from scipy.stats import uniform
from llmkvb.request_generator.content_generator.old_string.base_start_selection import BaseStartSelectionGenerator
class UniformStartSelectionGenerator(BaseStartSelectionGenerator):
    def __init__(self, config):
        super().__init__(config)
    def select(self, **kwargs) -> int:
        left = kwargs.get("left", None)
        right = kwargs.get("right", None)
        assert left is not None, "left is required"
        assert right is not None, "right is required"
        assert right >= left, "right should be greater than left"
        unform_dist = uniform(loc=left, scale=right-left+1)
        retval = int(unform_dist.rvs())
        while retval > right:
            retval = int(unform_dist.rvs())
        return retval
        
