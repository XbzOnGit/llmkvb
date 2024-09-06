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
    parser.add_argument('--llmkvb_qps_scale', type=float, default=1.0)
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
    qps_scale = args.llmkvb_qps_scale
    assert qps_scale > 0
    qps = config["request_generator"]["shape_generator"]["request_interval_generator"]["qps"]
    assert qps > 0
    now_qps = qps * qps_scale
    print(f"qps: {now_qps}")
    reqlist = None
    max_arrival_time = 0.0
    if args.llmkvb_trace_input_file is not None:
        reqlist = []
        with open(args.llmkvb_trace_input_file, "r") as f:
            for line in f:
                req_dict = json.loads(line)
                req_dict["arrived_at"] = req_dict["arrived_at"] / qps_scale
                if req_dict["arrived_at"] > max_arrival_time:
                    max_arrival_time = req_dict["arrived_at"]
                reqlist.append(KV_Request
                               (arrived_at=req_dict["arrived_at"], 
                                tokens=req_dict["tokens"], output_length=req_dict["output_length"]))
    else:
        reqgen = RequestGeneratorRegistry.get_from_str(config["request_generator"]["provider"], config["request_generator"])
        reqlist = reqgen.generate_requests()
        for req in reqlist:
            req.arrived_at = req.arrived_at / qps_scale
            if req.arrived_at > max_arrival_time:
                max_arrival_time = req.arrived_at
    if args.llmkvb_trace_output_file is not None:
        with open(args.llmkvb_trace_output_file, "w") as f:
            for req in reqlist:
                dumpstr = req.dump_json_line_string()
                f.write(dumpstr)
    repeat_times = 1
    if "repeatition" in config:
        repeat_times = config["repeatition"]
    repeat_interval = 1 / now_qps
    print(f"repeat_interval: {repeat_interval}\n\n")
    base_arrive_time = max_arrival_time + repeat_interval
    base_len = len(reqlist)
    # total_cnt = base_len
    for _ in range(repeat_times - 1):
        for i in range(base_len):
            # print(f"Should have {total_cnt} arrivaing at {base_arrive_time + reqlist[i].arrived_at}")
            # total_cnt += 1
            reqlist.append(KV_Request(arrived_at=base_arrive_time + reqlist[i].arrived_at, 
                                      tokens=reqlist[i].tokens, output_length=reqlist[i].output_length))
        base_arrive_time += (max_arrival_time + repeat_interval)
        # print(f"base_arrive_time of {_}: {base_arrive_time}")
    if args.llmkvb_executor is not None:
        executor = ExecutorRegistry.get_from_str(args.llmkvb_executor)
        executor.execute(reqlist)


if __name__ == "__main__":
    main()
