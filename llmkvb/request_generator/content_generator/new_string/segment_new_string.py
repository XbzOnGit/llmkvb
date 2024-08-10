from typing import List, Tuple
import importlib
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
        self.prefix_ratio_generator = PrefixRatioGeneratorRegistry.get_from_str(\
            self._config["prefix_ratio_generator"]["provider"], self._config["prefix_ratio_generator"])
        self.prefix_ratio_left = self._config["prefix_ratio_generator"]["left"]
        self.prefix_ratio_right = self._config["prefix_ratio_generator"]["right"]
        self.segment_length_generator = SegmentLengthGeneratorRegistry.get_from_str(\
            self._config["segment_length_generator"]["provider"], self._config["segment_length_generator"])
        self.segment_length_left_per_length = self._config["segment_length_generator"]["left_per_length"]
        self.segment_length_right_per_length = self._config["segment_length_generator"]["right_per_length"]
        self.segment_interval_generator = SegmentIntervalGeneratorRegistry.get_from_str(\
            self._config["segment_interval_generator"]["provider"], self._config["segment_interval_generator"])
        self.segment_interval_left_per_length = self._config["segment_interval_generator"]["left_per_length"]
        self.segment_interval_right_per_length = self._config["segment_interval_generator"]["right_per_length"]
        self.max_following_segment_cnt = self._config["max_following_segment_cnt"]
    def generate_new_string(self, **kwargs) -> Tuple[int, List[Tuple[int, int]]]:
        input_length = kwargs.get("input_length", None)
        assert input_length is not None, "input_length is required"
        reuse_ratio = self.reuse_ratio_generator.get_number(length=input_length, min=0.0, max=1.0,\
                                                             left=self.reuse_ratio_left, right=self.reuse_ratio_right)
        prefix_ratio = self.prefix_ratio_generator.get_number(length=input_length, min=0.0, max=1.0,\
                                                              left=self.prefix_ratio_left, right=self.prefix_ratio_right)
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


