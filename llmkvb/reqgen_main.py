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
    reqid = 0
    for req in reqlist:
        print(f"reqid: {reqid}")
        print(f"arrived_at: {req.arrived_at}")
        print(f"output_length: {req.output_length}")
        print(f"tokens: {req.tokens}")
        print("\n")
        reqid += 1



if __name__ == "__main__":
    main()
