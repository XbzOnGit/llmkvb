#!/bin/bash
conda create -n llmkvb python=3.10
pip install -r requirements.txt
conda activate llmkvb
python3 -m llmkvb.main \
            --llmkvb_config ./llmkvb/config/ragcache_low.yaml \
            --llmkvb_trace_output_file ragcache_low.jsonl \
            --llmkvb_tracegen_only
            
python3 -m llmkvb.main \
            --llmkvb_config ./llmkvb/config/ragcache_high.yaml \
            --llmkvb_trace_output_file ragcache_high.jsonl \
            --llmkvb_tracegen_only

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