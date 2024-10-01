# Examples
## Env setup
### Use venv
1. Ensure that you have Python 3.10 installed on your system. Refer <https://www.bitecode.dev/p/installing-python-the-bare-minimum>
2. `cd` into the repository root
3. Create a virtual environment using `venv` module using `python3.10 -m venv .venv`
4. Activate the virtual environment using `source .venv/bin/activate`
5. Install the dependencies using `python -m pip install -r requirements.txt`
6. Run `deactivate` to deactivate the virtual environment
### Use conda
1. conda create a python3.10 environment.  
2. ```python -m pip install -r requirements.txt```  
3. remove source .venv/bin/activate from the scripts in this repo.  
## Vary on copy pattern to show the benefit of RAGCache
With a new requests sharing prefix with old ones, they can differ in which old request to choose.  
ragcache_low chooses from latest requests, while ragcache_high chooses from a distant request(and make the trace a large working set replayed for 3 times).  
For latest copy pattern, cache-reordering of ragcache has little effect, while for the large working set replayed one, it should benefit much.  
1. Write two yamls in config folder.  
Although the reuse_ratio = possible_reused_tokens / total_tokens are the same, they differ in how those tokens are distributed.  
In ragcache_low, 
ragcache_low.yaml:  
```
request_generator:
  content_generator:
    new_string_generator:
      no_reuse_probability: 0.2
      reuse_ratio_generator:
        left: 0.83
        provider: uniform
        right: 0.83
    old_string_generator:
      request_selection_generator:
        provider: latest
  local_files_only: true
  provider: synthetic
  shape_generator:
    num_requests: 600
    provider: synthetic
    request_interval_generator:
      provider: poisson
      qps: 5.0
    request_length_generator:
      max_tokens: 15000
      min_tokens: 15000
      prefill_to_decode_ratio: 1500
      provider: uniform
    seed: 42
  tokenizer_name: bert-base-uncased
  tokenizer_type: transformers
seed: 42
```
ragcache_high.yaml:  
```
request_generator:
  first_no_reuse: 200
  content_generator:
    new_string_generator:
      reuse_ratio_generator:
        left: 1.0
        provider: uniform
        right: 1.0
    old_string_generator:
      request_selection_generator:
        provider: fixed_distance
        distance: 200
  local_files_only: true
  provider: synthetic
  shape_generator:
    num_requests: 600
    provider: synthetic
    request_interval_generator:
      provider: poisson
      qps: 5.0
    request_length_generator:
      max_tokens: 15000
      min_tokens: 15000
      prefill_to_decode_ratio: 1500
      provider: uniform
    seed: 39
  tokenizer_name: bert-base-uncased
  tokenizer_type: transformers
seed: 39
```
2. Run gen_traces.sh from root of repo.  
```
#!/bin/bash

source .venv/bin/activate
config_names="ragcache_low ragcache_high"
for config_name in $config_names; do
        echo "$config_name.jsonl generation."
        python3 -m llmkvb.main \
            --llmkvb_config "./llmkvb/config/$config_name.yaml" \
            --llmkvb_trace_output_file "$config_name".jsonl \
            --llmkvb_tracegen_only
        python3 ./llmkvb/request_generator/trace_properties/unique_length_and_reuse_ratio.py ./"$config_name".jsonl
done
```
3. Launch experiments and plot the graph.  
To launch one.  
On the first run, it will train the time predictor, which can take some time.  
```
python -m llmkvb.main \
        --replica_config_device a40 \
        --replica_config_network_device a40_pairwise_nvlink \
        --replica_config_model_name meta-llama/Meta-Llama-3-8B \
        --cluster_config_num_replicas 1 \
        --replica_config_tensor_parallel_size 1 \
        --replica_config_num_pipeline_stages 1 \
        --replica_scheduler_config_type vllm  \
        --vllm_scheduler_config_batch_size_cap 256  \
        --vllm_scheduler_config_max_tokens_in_batch 16384 \
        --random_forrest_execution_time_predictor_config_prediction_max_prefill_chunk_size 16384 \
        --random_forrest_execution_time_predictor_config_prediction_max_tokens_per_request 16384 \
        --llmkvb_config ./llmkvb/config/ragcache_low.yaml \
        --llmkvb_trace_input_file ragcache_low.jsonl \
        --llmkvb_qps_scale 0.5 \
        --vllm_scheduler_config_cache_lookup_type prefix \
        --vllm_scheduler_config_cache_evict_type lru \
        --vllm_scheduler_config_cache_evict_op write \
        --vllm_scheduler_config_cpu_memory_size 64GB \
        --vllm_scheduler_config_gpu_cpu_thput 16GB/S \
        --vllm_scheduler_config_cpu_gpu_thput 16GB/S \
        --vllm_scheduler_config_disk_size 256GB \
        --vllm_scheduler_config_disk_cpu_thput 4000MB/S \
        --vllm_scheduler_config_cpu_disk_thput 4000MB/S \
        --cluster_config_num_replicas 2
```
To plot graphs.  
```
#!/bin/bash
exp="ragcache_low ragcache_high"
./rundisk_line.sh $exp ./exps/"$exp"_yymmdd 0.1 0.2 5
```
Currently plotting a graph with 5 papers and 5 points of qps can take about half an hour.  