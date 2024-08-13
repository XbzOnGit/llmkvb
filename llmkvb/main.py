import yaml
import argparse
from llmkvb.utils.random import set_seeds
from llmkvb.request_generator.request_generator_registry import RequestGeneratorRegistry
from llmkvb.executor.executor_registry import ExecutorRegistry
from copy import deepcopy
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="LLMKVB: Large Language Model KV Cache Benchmark")
    parser.add_argument("--llmkvb_config", type=str, help="Path to the configuration file", default="./llmkvb/config/default.yaml")
    parser.add_argument("--llmkvb_trace_output_file", default=None)
    parser.add_argument("--llmkvb_executor", default="vidur")
    args = deepcopy(sys.argv[1:])
    args, _ = parser.parse_known_args(args)
    return args

def main():
    config = None
    args = parse_args()
    with open(args.llmkvb_config, "r") as f:
        config = yaml.safe_load(f)
    set_seeds(config["seed"])
    reqgen = RequestGeneratorRegistry.get_from_str(config["request_generator"]["provider"], config["request_generator"])
    reqlist = reqgen.generate_requests()
    if args.llmkvb_trace_output_file is not None:
        with open(args.llmkvb_trace_output_file, "w") as f:
            for req in reqlist:
                dumpstr = req.dump_json_line_string()
                f.write(dumpstr)
    if args.llmkvb_executor is not None:
        executor = ExecutorRegistry.get_from_str(args.llmkvb_executor)
        executor.execute(reqlist)


if __name__ == "__main__":
    main()
