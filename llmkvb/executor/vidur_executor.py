# Add import path, making it can find vidur module
import sys
import os
# Find the current absolute path
__abs_file_path__ = os.path.abspath(__file__)
__vidur_dir__ = os.path.join(os.path.dirname(__abs_file_path__), "vidur")
sys.path.append(__vidur_dir__)


from llmkvb.executor.base_executor import BaseExecutor
from llmkvb.executor.vidur.vidur.entities.request import Request
from llmkvb.executor.vidur.vidur.config import SimulationConfig
from llmkvb.executor.vidur.vidur.simulator import Simulator

class VidurExecutor(BaseExecutor):
    def __init__(self):
        super().__init__()
        self.simulation_config : SimulationConfig = SimulationConfig.create_from_cli_args()
    def execute(self, reqlist: list):
        # cd to vidur directory
        original_dir = os.getcwd()
        os.chdir(__vidur_dir__)
        external_trace = []
        for req in reqlist:
            vidur_req = Request(arrived_at=req.arrived_at, num_prefill_tokens=len(req.tokens), 
                                num_decode_tokens=req.output_length - len(req.tokens), num_processed_tokens=0, tokens=req.tokens)
            external_trace.append(vidur_req)
        self.simulation_config.external_trace_injected = True
        self.simulation_config.external_trace = external_trace
        self.simulator = Simulator(self.simulation_config)
        self.simulator.run()
        # cd back
        os.chdir(original_dir)

        
            
            
            
            