#!/bin/bash
# This script runs a one paper x one setup.
# Which is one bar if plotting throughput.
# Fixing setup to GPU+CPU+DISK.


# Define a function, input method, config, qps, returns throughput and avg ttft.
config_dir_path="./llmkvb/config/"
run_exp() {
    paper_name=$1
    config_name=$2
    qps_scale=$3
    if [ $paper_name == "baseline" ]; then
        output=$(python -m llmkvb.main \
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
        --llmkvb_config "$config_dir_path$config_name.yaml" \
        --llmkvb_trace_input_file "$config_name".jsonl \
        --llmkvb_qps_scale "$qps_scale" \
        --vllm_scheduler_config_cache_lookup_type prefix \
        --vllm_scheduler_config_cache_evict_type lru \
        --vllm_scheduler_config_cache_evict_op write \
        --vllm_scheduler_config_cpu_memory_size 64GB \
        --vllm_scheduler_config_gpu_cpu_thput 16GB/S \
        --vllm_scheduler_config_cpu_gpu_thput 16GB/S \
        --vllm_scheduler_config_disk_size 256GB \
        --vllm_scheduler_config_disk_cpu_thput 4000MB/S \
        --vllm_scheduler_config_cpu_disk_thput 4000MB/S \
        --cluster_config_num_replicas 2)    
    # else if cachedattention
    elif [ $paper_name == "cachedattention" ]; then
        output=$(python -m llmkvb.main  \
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
        --llmkvb_config "$config_dir_path$config_name.yaml" \
        --llmkvb_trace_input_file "$config_name".jsonl \
        --llmkvb_qps_scale "$qps_scale" \
        --vllm_scheduler_config_cache_lookup_type prefix \
        --vllm_scheduler_config_cache_evict_type lru \
        --vllm_scheduler_config_cache_evict_op write \
        --vllm_scheduler_config_cpu_memory_size 64GB \
        --vllm_scheduler_config_gpu_cpu_thput 16GB/S \
        --vllm_scheduler_config_cpu_gpu_thput 16GB/S \
        --vllm_scheduler_config_layer_pipeline \
        --vllm_scheduler_config_read_pipeline_buffer \
        --vllm_scheduler_config_gpu_write_through_cpu async \
        --vllm_scheduler_config_cpu_sysbuf_fraction 0.3 \
        --vllm_scheduler_config_disk_size 256GB \
        --vllm_scheduler_config_disk_cpu_thput 4000MB/S \
        --vllm_scheduler_config_cpu_disk_thput 4000MB/S \
        --vllm_scheduler_config_disk_cpu_prefetch \
        --cluster_config_num_replicas 2)
        # Note that scheduler-eviction removed for speedup.
    elif [ $paper_name == "ragcache" ]; then
        output=$(python -m llmkvb.main \
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
        --llmkvb_config "$config_dir_path$config_name.yaml" \
        --llmkvb_trace_input_file "$config_name".jsonl \
        --llmkvb_qps_scale "$qps_scale" \
        --vllm_scheduler_config_cache_lookup_type prefix \
        --vllm_scheduler_config_cache_evict_type pgdsf \
        --vllm_scheduler_config_cache_evict_op write \
        --vllm_scheduler_config_cpu_memory_size 64GB \
        --vllm_scheduler_config_gpu_cpu_thput 16GB/S \
        --vllm_scheduler_config_cpu_gpu_thput 16GB/S \
        --vllm_scheduler_config_disk_size 256GB \
        --vllm_scheduler_config_disk_cpu_thput 4000MB/S \
        --vllm_scheduler_config_cpu_disk_thput 4000MB/S \
        --vllm_scheduler_config_cache_reordering \
        --cluster_config_num_replicas 2)
    elif [ $paper_name == "cachegen" ]; then
        output=$(python -m llmkvb.main \
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
        --llmkvb_config "$config_dir_path$config_name.yaml" \
        --llmkvb_trace_input_file "$config_name".jsonl \
        --llmkvb_qps_scale "$qps_scale" \
        --vllm_scheduler_config_cache_lookup_type prefix \
        --vllm_scheduler_config_cache_evict_type lru \
        --vllm_scheduler_config_cache_evict_op write \
        --vllm_scheduler_config_cpu_memory_size 64GB \
        --vllm_scheduler_config_gpu_cpu_thput 16GB/S \
        --vllm_scheduler_config_cpu_gpu_thput 16GB/S \
        --vllm_scheduler_config_disk_size 256GB \
        --vllm_scheduler_config_disk_cpu_thput 4000MB/S \
        --vllm_scheduler_config_cpu_disk_thput 4000MB/S \
        --vllm_scheduler_config_quant_kv \
        --vllm_scheduler_config_quant_ratio 0.25 \
        --vllm_scheduler_config_decode_place gpu \
        --vllm_scheduler_config_decode_speed 60000 \
        --vllm_scheduler_config_encode_speed 60000 \
        --vllm_scheduler_config_gpu_write_through_cpu sync \
        --cluster_config_num_replicas 2 \
        --cluster_config_p2p_bandwidth_between_nodes 2GB/S)
        # Now cachegen writes through, but not pipelined like cachedattention.
    elif [ $paper_name == "cacheblend" ]; then
        output=$(python -m llmkvb.main \
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
        --llmkvb_config "$config_dir_path$config_name.yaml" \
        --llmkvb_trace_input_file "$config_name".jsonl \
        --llmkvb_qps_scale "$qps_scale" \
        --vllm_scheduler_config_cache_lookup_type prefix \
        --vllm_scheduler_config_cache_evict_type lru \
        --vllm_scheduler_config_cache_evict_op write \
        --vllm_scheduler_config_cpu_memory_size 64GB \
        --vllm_scheduler_config_gpu_cpu_thput 16GB/S \
        --vllm_scheduler_config_cpu_gpu_thput 16GB/S \
        --vllm_scheduler_config_disk_size 256GB \
        --vllm_scheduler_config_disk_cpu_thput 4000MB/S \
        --vllm_scheduler_config_cpu_disk_thput 4000MB/S \
        --cluster_config_num_replicas 2 \
        --vllm_scheduler_config_allow_reorder_kv_blocks)
    else
    echo "Invalid paper name"
    exit 1
    fi
    # INFO 09-07 16:27:48 simulator.py:91] Throughput: 5.292980613537639
# INFO 09-07 16:27:48 simulator.py:98] Average TTFT: 5.242194585462924
    throughput=$(echo $output | grep -oP 'Throughput: \K[0-9.]+')
    avg_ttft=$(echo $output | grep -oP 'Average TTFT: \K[0-9.]+')
    qps=$(echo $output | grep -oP 'scaled qps: \K[0-9.]+')
    printf "$throughput $avg_ttft $qps"
}


if [ $# -lt 5 ]; then
    echo "Usage: $0 <paper> <trace> <qps_scale_start> <qps_scale_interval> <point_number>"
    exit 1
fi

source .venv/bin/activate
paper_name=$1
config_name=$2
qps_scale_start=$3
qps_scale_interval=$4
point_number=$5

# Check if config_name.jsonl exists
if [ ! -f "$config_name.jsonl" ]; then
    echo "$config_name.jsonl generation."
    python -m llmkvb.main \
        --llmkvb_config "$config_dir_path$config_name.yaml" \
        --llmkvb_trace_output_file "$config_name".jsonl \
        --llmkvb_tracegen_only
fi

echo "Running $paper_name $config_name"
# Loop from qps_scale_start, with qps_scale_interval, for point_number times.
current_qps_scale=$qps_scale_start
qps_scale_cnt=0
qps_list=""
throughput_list=""
avg_ttft_list=""
while [ $qps_scale_cnt -lt $point_number ]; do
    result=$(run_exp $paper_name $config_name $current_qps_scale)
    throughput=$(echo $result | cut -d' ' -f1)
    avg_ttft=$(echo $result | cut -d' ' -f2)
    real_qps=$(echo $result | cut -d' ' -f3)
    if [ ${#qps_list} -eq 0 ]; then
        qps_list="$real_qps"
        throughput_list="$throughput"
        avg_ttft_list="$avg_ttft"
    else
        qps_list="$qps_list,$real_qps"
        throughput_list="$throughput_list,$throughput"
        avg_ttft_list="$avg_ttft_list,$avg_ttft"
    fi
    current_qps_scale=$(echo "$current_qps_scale + $qps_scale_interval" | bc -l)
    qps_scale_cnt=$(($qps_scale_cnt + 1))
done
echo "qps_list: $qps_list"
echo "throughput_list: $throughput_list"
echo "avg_ttft_list: $avg_ttft_list"
echo "qps_list: $qps_list" >> dump_$config_name_$paper_name.txt
echo "throughput_list: $throughput_list" >> dump_$config_name_$paper_name.txt
echo "avg_ttft_list: $avg_ttft_list" >> dump_$config_name_$paper_name.txt



