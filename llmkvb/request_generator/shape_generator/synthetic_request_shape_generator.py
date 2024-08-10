from typing import List

from llmkvb.entities import Shape_Request
from llmkvb.request_generator.shape_generator.base_request_shape_generator import BaseRequestShapeGenerator
from llmkvb.request_generator.shape_generator.request_interval_generator_registry import (
    RequestIntervalGeneratorRegistry,
)
from llmkvb.request_generator.shape_generator.request_length_generator_registry import (
    RequestLengthGeneratorRegistry,
)
from llmkvb.utils.random import set_seeds


class SyntheticRequestShapeGenerator(BaseRequestShapeGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._seed = self._config["seed"]

        self._request_length_generator = RequestLengthGeneratorRegistry.get_from_str(
            self._config["request_length_generator"]["provider"], self._config["request_length_generator"]
        )
        self._request_interval_generator = (
            RequestIntervalGeneratorRegistry.get_from_str(
                self._config["request_interval_generator"]["provider"], self._config["request_interval_generator"]
            )
        )

    def _generate_next_request(self, last_arrived_at: float) -> Shape_Request:
        inter_request_time = (
            self._request_interval_generator.get_next_inter_request_time()
        )
        if inter_request_time is None:
            return None
        arrived_at = last_arrived_at + inter_request_time

        (
            prefill_tokens,
            decode_tokens,
        ) = self._request_length_generator.get_next_num_tokens()

        if prefill_tokens is None or decode_tokens is None:
            return None

        return Shape_Request(
            arrived_at=arrived_at,
            input_length=int(prefill_tokens),
            output_length=int(decode_tokens)
        )

    def _generate_requests(self) -> List[Shape_Request]:
        requests = []

        current_time = 0

        # first priority is duration
        if "duration" in self._config:
            duration = self._config["duration"]
            while current_time < duration:
                request = self._generate_next_request(current_time)
                current_time = request.arrived_at
                requests.append(request)
        elif "num_requests" in self._config:
            for _ in range(self._config["num_requests"]):
                request = self._generate_next_request(current_time)
                current_time = request.arrived_at
                requests.append(request)
        else:
            assert self._config["request_interval_generator"]["provider"] == "trace"
            while True:
                request = self._generate_next_request(current_time)
                if request is None:
                    break
                current_time = request.arrived_at
                requests.append(request)

        return requests

    def generate_requests(self) -> List[Shape_Request]:
        assert (
            "num_requests" in self._config
            or "duration" in self._config
            or self._config["request_interval_generator"]["provider"] == "trace"
        )

        set_seeds(self._seed)

        requests = self._generate_requests()

        # sort requests by arrival time
        requests.sort(key=lambda x: (x.arrived_at, x.id))
        # remove any requests that arrived after the time limit
        if "duration" in self._config:
            duration = self._config["duration"]
            requests = [
                request
                for request in requests
                if request.arrived_at
                < duration
            ]

        return requests
