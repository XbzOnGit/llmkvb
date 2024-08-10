import csv
from abc import ABC, abstractmethod
from typing import List

from llmkvb.entities import Shape_Request


class BaseRequestShapeGenerator(ABC):
    def __init__(self, config: dict):
        self._config = config
        self._should_write_json_trace = True if "output_dir" in self._config else False
        if self._should_write_json_trace:
            self.output_dir = self._config["output_dir"]

    def _write_requests_to_file(self, requests: List[Shape_Request]) -> None:
        request_shape_file = f"{self.output_dir}/requests_shape.csv"
        with open(request_shape_file, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "input_length", "output_length"])
            for request in requests:
                writer.writerow(
                    [request.arrived_at, request.input_length, request.output_length]
                )

    @abstractmethod
    def generate_requests(self) -> List[Shape_Request]:
        pass

    def generate(self) -> List[Shape_Request]:
        requests = self.generate_requests()

        if self._should_write_json_trace:
            self._write_requests_to_file(requests)

        return requests
