from llmkvb.utils.random import set_seeds
from llmkvb.request_generator.request_generator_registry import RequestGeneratorRegistry
import yaml
def main():
    config = None
    with open("./llmkvb/config/default.yaml", "r") as f:
        config = yaml.safe_load(f)
    set_seeds(config["seed"])
    reqgen = RequestGeneratorRegistry.get_from_str(config["request_generator"]["provider"], config["request_generator"])
    reqlist = reqgen.generate_requests()
    with open("output.jsonl", "w") as f:
        for req in reqlist:
            dumpstr = req.dump_json_line_string()
            f.write(dumpstr)



if __name__ == "__main__":
    main()
