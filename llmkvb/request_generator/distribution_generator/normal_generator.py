from llmkvb.request_generator.distribution_generator.base_distribution_generator import BaseDistributionGenerator
from scipy.stats import truncnorm

class NormalGenerator(BaseDistributionGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_number(self, **kwargs):
        length = kwargs.get("length", None)
        thismin = kwargs.get("min", None)
        thismax = kwargs.get("max", None)
        assert thismin is not None, "min is required"
        assert thismax is not None, "max is required"
        assert thismax >= thismin, "max should be greater than min"
        thismean = None
        thisstdvar = None
        if "mean_per_length" in kwargs:
            unit_mean = kwargs.get("mean_per_length", None)
            thismean = unit_mean * length
        else:
            thismean = kwargs.get("mean", None)
            assert thismean is not None, "mean is required when mean_per_length is not provided"
        assert thismean >= thismin and thismean <= thismax, "mean should be in the range of min and max"
        if "stdvar_per_length" in kwargs:
            unit_stdvar = kwargs.get("stdvar_per_length", None)
            thisstdvar = unit_stdvar * length
        else:
            thisstdvar = kwargs.get("stdvar", None)
            assert thisstdvar is not None, "stdvar is required when stdvar_per_length is not provided"
        assert thisstdvar >= 0, "stdvar should be no less than 0"
        normal_dist = truncnorm(
            (thismin-thismean)/thisstdvar, (thismax-thismean)/thisstdvar, loc=thismean, scale=thisstdvar
        )
        return float(normal_dist.rvs())
