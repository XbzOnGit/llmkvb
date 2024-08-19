import yaml
import argparse
from llmkvb.utils.random import set_seeds
from llmkvb.request_generator.request_generator_registry import RequestGeneratorRegistry
from llmkvb.executor.executor_registry import ExecutorRegistry
from copy import deepcopy
import sys
import json
from llmkvb.entities.request import Request as KV_Request

def parse_args():
    parser = argparse.ArgumentParser(description="LLMKVB: Large Language Model KV Cache Benchmark")
    parser.add_argument("--llmkvb_config", type=str, help="Path to the configuration file", default="./llmkvb/config/default.yaml")
    parser.add_argument("--llmkvb_trace_output_file", default=None)
    parser.add_argument("--llmkvb_executor", default="vidur")
    parser.add_argument("--llmkvb_trace_input_file", default=None)
    args = deepcopy(sys.argv[1:])
    args, not_recog = parser.parse_known_args(args)
    sys.argv[1:] = not_recog
    return args

def main():
    config = None
    args = parse_args()
    with open(args.llmkvb_config, "r") as f:
        config = yaml.safe_load(f)
    set_seeds(config["seed"])
    reqlist = None
    if args.llmkvb_trace_input_file is not None:
        reqlist = []
        with open(args.llmkvb_trace_input_file, "r") as f:
            for line in f:
                req_dict = json.loads(line)
                reqlist.append(KV_Request
                               (arrived_at=req_dict["arrived_at"], 
                                tokens=req_dict["tokens"], output_length=req_dict["output_length"]))
    else:
        reqgen = RequestGeneratorRegistry.get_from_str(config["request_generator"]["provider"], config["request_generator"])
        reqlist = reqgen.generate_requests()
    if args.llmkvb_trace_output_file is not None:
        with open(args.llmkvb_trace_output_file, "w") as f:
            for req in reqlist:
                dumpstr = req.dump_json_line_string()
                f.write(dumpstr)
    repeat_times = 1
    if "repeatition" in config:
        repeat_times = config["repeatition"]
    final_req_list = []
    for _ in range(repeat_times):
        final_req_list.extend(reqlist)
    if args.llmkvb_executor is not None:
        executor = ExecutorRegistry.get_from_str(args.llmkvb_executor)
        executor.execute(final_req_list)


if __name__ == "__main__":
    main()
