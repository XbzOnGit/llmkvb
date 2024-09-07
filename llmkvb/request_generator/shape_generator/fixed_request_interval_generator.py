from llmkvb.request_generator.shape_generator.base_request_interval_generator import (
    BaseRequestIntervalGenerator,
)


class FixedRequestIntervalGenerator(BaseRequestIntervalGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._qps = self._config["qps"]
        assert self._qps > 0, "QPS must be greater than 0"
        self._fixed_interval = 1 / self._qps
        # print(f"FixedRequestIntervalGenerator: qps: {self._qps}, fixed_interval: {self._fixed_interval}")

    def get_next_inter_request_time(self) -> float:
        return self._fixed_interval