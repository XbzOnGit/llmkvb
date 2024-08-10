from llmkvb.request_generator.distribution_generator.base_distribution_generator import BaseDistributionGenerator
from scipy.stats import uniform
class UniformGenerator(BaseDistributionGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_number(self, **kwargs):
        thismin = kwargs.get("min", None)
        thismax = kwargs.get("max", None)
        assert thismin is not None, "min is required"
        assert thismax is not None, "max is required"
        assert thismax >= thismin, "max should be greater than min"
        length = kwargs.get("length", None)
        assert length is not None, "length is required"
        a = None
        b = None
        if "mean_per_length" in kwargs or "mean" in kwargs:
            thismean = None
            thisstdvar = None
            assert "stdvar_per_length" in kwargs or "stdvar" in kwargs, "stdvar is required"
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
            a = thismean - (3 ** 0.5) * thisstdvar
            b = thismean + (3 ** 0.5) * thisstdvar
            a = max(a, thismin)
            b = min(b, thismax)
            b = max(b, a)
        else:
            assert ("left_per_length" in kwargs or "left" in kwargs) and ("right_per_length" in kwargs or "right" in kwargs), "left and right are required"
            thisleft = None
            thisright = None
            if "left_per_length" in kwargs:
                unit_left = kwargs.get("left_per_length", None)
                thisleft = unit_left * length
            else:
                thisleft = kwargs.get("left", None)
                assert thisleft is not None, "left is required when left_per_length is not provided"
            if "right_per_length" in kwargs:
                unit_right = kwargs.get("right_per_length", None)
                thisright = unit_right * length
            else:
                thisright = kwargs.get("right", None)
                assert thisright is not None, "right is required when right_per_length is not provided"
            a = max(thismin, thisleft)
            b = min(thismax, thisright)
            b = max(b, a)
        unform_dist = uniform(loc=a, scale=b-a)
        return float(unform_dist.rvs())
        