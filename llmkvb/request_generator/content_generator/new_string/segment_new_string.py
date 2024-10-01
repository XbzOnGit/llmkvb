from typing import List, Tuple
import random
from llmkvb.request_generator.content_generator.new_string.base_new_string import (
    BaseNewStringGenerator,
)
from llmkvb.request_generator.content_generator.new_string.reuse_ratio_registry import (
    ReuseRatioGeneratorRegistry,
)
from llmkvb.request_generator.content_generator.new_string.prefix_ratio_registry import (
    PrefixRatioGeneratorRegistry,
)
from llmkvb.request_generator.content_generator.new_string.segment_length_registry import (
    SegmentLengthGeneratorRegistry,
)
from llmkvb.request_generator.content_generator.new_string.segment_interval_registry import (
    SegmentIntervalGeneratorRegistry,
)


class SegmentNewStringGenerator(BaseNewStringGenerator):
    def __init__(self, config):
        super().__init__(config)
        self.reuse_ratio_generator = ReuseRatioGeneratorRegistry.get_from_str(\
            self._config["reuse_ratio_generator"]["provider"], self._config["reuse_ratio_generator"])
        self.reuse_ratio_left = self._config["reuse_ratio_generator"]["left"]
        self.reuse_ratio_right = self._config["reuse_ratio_generator"]["right"]
        if "prefix_ratio_generator" not in self._config:
            default_prefix_config = {"provider": "uniform", "left": 1.0, "right": 1.0}
            self.prefix_ratio_generator = PrefixRatioGeneratorRegistry.get_from_str(default_prefix_config["provider"],
                                                                                     default_prefix_config)
            self.prefix_ratio_left = default_prefix_config["left"]
            self.prefix_ratio_right = default_prefix_config["right"]
        else:
            self.prefix_ratio_generator = PrefixRatioGeneratorRegistry.get_from_str(\
                self._config["prefix_ratio_generator"]["provider"], self._config["prefix_ratio_generator"])
            self.prefix_ratio_left = self._config["prefix_ratio_generator"]["left"]
            self.prefix_ratio_right = self._config["prefix_ratio_generator"]["right"]
        if "segment_length_generator" not in self._config:
            default_segment_length_config = {"provider": "uniform", "left_per_length": 0, "right_per_length": 0.8}
            self.segment_length_generator = SegmentLengthGeneratorRegistry.get_from_str(
                default_segment_length_config["provider"],
                default_segment_length_config)
            self.segment_length_left_per_length = default_segment_length_config["left_per_length"]
            self.segment_length_right_per_length = default_segment_length_config["right_per_length"]
        else:
            self.segment_length_generator = SegmentLengthGeneratorRegistry.get_from_str(\
                self._config["segment_length_generator"]["provider"], self._config["segment_length_generator"])
            self.segment_length_left_per_length = self._config["segment_length_generator"]["left_per_length"]
            self.segment_length_right_per_length = self._config["segment_length_generator"]["right_per_length"]
        if "segment_interval_generator" not in self._config:
            default_segment_interval_config = {"provider": "uniform", "left_per_length": 0, "right_per_length": 0.8}
            self.segment_interval_generator = SegmentIntervalGeneratorRegistry.get_from_str(
                default_segment_interval_config["provider"],
                default_segment_interval_config)
            self.segment_interval_left_per_length = default_segment_interval_config["left_per_length"]
            self.segment_interval_right_per_length = default_segment_interval_config["right_per_length"]
        else:
            self.segment_interval_generator = SegmentIntervalGeneratorRegistry.get_from_str(\
                self._config["segment_interval_generator"]["provider"], self._config["segment_interval_generator"])
            self.segment_interval_left_per_length = self._config["segment_interval_generator"]["left_per_length"]
            self.segment_interval_right_per_length = self._config["segment_interval_generator"]["right_per_length"]
        self.max_following_segment_cnt = self._config.get("max_following_segment_cnt", 1)
        if "no_reuse_probability" in self._config:
            self.no_reuse_probability = self._config["no_reuse_probability"]
        else:
            self.no_reuse_probability = 0.0
    def generate_new_string(self, **kwargs) -> Tuple[int, List[Tuple[int, int]]]:
        input_length = kwargs.get("input_length", None)
        assert input_length is not None, "input_length is required"
        if self.no_reuse_probability > 0.0 and random.random() < self.no_reuse_probability:
            return (0, [])
        assert self.reuse_ratio_left >= 0.0 and self.reuse_ratio_left <= 1.0, "reuse_ratio_left should be in [0, 1]"
        assert self.reuse_ratio_right >= 0.0 and self.reuse_ratio_right <= 1.0, "reuse_ratio_right should be in [0, 1]"
        assert self.prefix_ratio_left >= 0.0 and self.prefix_ratio_left <= 1.0, "prefix_ratio_left should be in [0, 1]"
        assert self.prefix_ratio_right >= 0.0 and self.prefix_ratio_right <= 1.0, "prefix_ratio_right should be in [0, 1]"
        reuse_ratio = self.reuse_ratio_generator.get_number(length=input_length, min=0.0, max=1.0,\
                                                             left=self.reuse_ratio_left, right=self.reuse_ratio_right)
        prefix_ratio = self.prefix_ratio_generator.get_number(length=input_length, min=0.0, max=1.0,\
                                                              left=self.prefix_ratio_left, right=self.prefix_ratio_right)
        assert reuse_ratio >= 0.0 and reuse_ratio <= 1.0, "reuse_ratio should be in [0, 1]"
        assert prefix_ratio >= 0.0 and prefix_ratio <= 1.0, "prefix_ratio should be in [0, 1]"
        reuse_length = round(input_length * reuse_ratio)
        prefix_length = round(reuse_length * prefix_ratio)
        remaining_length = reuse_length - prefix_length
        last_end = prefix_length - 1
        following_seg_cnt = 0
        max_following_segment_cnt = self.max_following_segment_cnt
        retval = (prefix_length, [])
        while remaining_length > 0:
            # Interval first, cos there have been prefix there.
            eff_int_len = input_length - last_end - 1 - remaining_length
            interval = self.segment_interval_generator.get_number(length=eff_int_len, min=0, max=eff_int_len,\
                                                                   left_per_length=self.segment_interval_left_per_length, \
                                                                    right_per_length=self.segment_interval_right_per_length)
            interval = round(interval)
            if interval < 0:
                interval = 0
            if interval > eff_int_len:
                interval = eff_int_len
            length = None
            if max_following_segment_cnt is not None and following_seg_cnt == max_following_segment_cnt:
                length = remaining_length
            else:
                # FIXME: Is min = 1 too small here, should it be configurable?
                length = self.segment_length_generator.get_number(length=remaining_length, min=1, max=remaining_length, \
                                                                  left_per_length=self.segment_length_left_per_length, \
                                                                    right_per_length=self.segment_length_right_per_length)
            length = round(length)
            if length < 1:
                length = 1
            if length > remaining_length:
                length = remaining_length
            retval[1].append((last_end + 1 + interval, length))
            last_end = last_end + interval + length
            remaining_length -= length
            following_seg_cnt += 1
        return retval


