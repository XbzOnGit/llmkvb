from typing import List

import pandas as pd

from llmkvb.entities import Shape_Request
from llmkvb.logger import init_logger
from llmkvb.request_generator.shape_generator.base_request_shape_generator import BaseRequestShapeGenerator

logger = init_logger(__name__)


class TraceReplayRequestShapeGenerator(BaseRequestShapeGenerator):
    """
    Reads a trace csv file containing request arrival time, its prompt and completion token values to generate
    inter-request times, number of tokens.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._trace_file = self._config["trace_file"]
        # load into a pd dataframe
        self._trace_df = pd.read_csv(self._trace_file)
        # restrict trace_df to be a subset of rows that have the same date
        self._trace_df = self._trace_df[
            self._trace_df["Date"] == self._config["date"]
        ]

        # scale prefill and decode tokens
        self._trace_df["PromptTokenCount"] = (
            self._trace_df["PromptTokenCount"]
            * self._config["prefill_scale_factor"]
        )
        self._trace_df["CompletionTokenCount"] = (
            self._trace_df["CompletionTokenCount"]
            * self._config["decode_scale_factor"]
        )

        # make sure all the prefill and decode counts are integers
        self._trace_df["PromptTokenCount"] = self._trace_df["PromptTokenCount"].astype(
            int
        )
        self._trace_df["CompletionTokenCount"] = self._trace_df[
            "CompletionTokenCount"
        ].astype(int)

        # make sure that there is at least one prefill and decode token
        self._trace_df["PromptTokenCount"] = self._trace_df["PromptTokenCount"].clip(
            lower=1
        )
        self._trace_df["CompletionTokenCount"] = self._trace_df[
            "CompletionTokenCount"
        ].clip(lower=1)

        # make sure the total does not exceed the max tokens, adjust the prefill tokens if needed
        total_tokens = (
            self._trace_df["PromptTokenCount"] + self._trace_df["CompletionTokenCount"]
        )
        diff_tokens = total_tokens - self._config["max_tokens"]
        diff_tokens = diff_tokens.clip(lower=0)
        self._trace_df["PromptTokenCount"] = (
            self._trace_df["PromptTokenCount"] - diff_tokens
        )

        assert all(
            self._trace_df["PromptTokenCount"] + self._trace_df["CompletionTokenCount"]
            <= self._config["max_tokens"]
        )

        # rescale the time to change QPS
        self._trace_df["Time"] = (
            self._trace_df["Time"]
            * self._config["time_scale_factor"]
        )

        # compute pd ratio and log the 25, 50, 75, 90, 95, 99 percentiles
        pd_ratio = (
            self._trace_df["PromptTokenCount"] / self._trace_df["CompletionTokenCount"]
        )
        logger.info(
            f"Loaded trace file {self._trace_file} with {len(self._trace_df)} requests"
        )
        logger.info(
            f"Prompt/decode token ratio stats\n:{pd_ratio.describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.95, 0.99])}"
        )

    def generate_requests(self) -> List[Shape_Request]:
        requests = []

        for _, row in self._trace_df.iterrows():
            request = Shape_Request(
                arrived_at=row["Time"],
                input_length=row["PromptTokenCount"],
                output_length=row["CompletionTokenCount"],
            )

            requests.append(request)

        return requests
