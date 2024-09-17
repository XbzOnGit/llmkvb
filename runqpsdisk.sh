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
        --vllm_scheduler_config_disk_size 1024GB \
        --vllm_scheduler_config_disk_cpu_thput 4000MB/S \
        --vllm_scheduler_config_cpu_disk_thput 4000MB/S \
        --cluster_config_num_replicas 2 \
        --global_scheduler_config_type locality \
        --locality_global_scheduler_config_threshold_of_imbanlance_ratio 2.0)    
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
        --vllm_scheduler_config_gpu_write_through_cpu \
        --vllm_scheduler_config_cpu_sysbuf_fraction 0.3 \
        --vllm_scheduler_config_disk_size 1024GB \
        --vllm_scheduler_config_disk_cpu_thput 4000MB/S \
        --vllm_scheduler_config_cpu_disk_thput 4000MB/S \
        --vllm_scheduler_config_disk_cpu_prefetch \
        --cluster_config_num_replicas 2 \
        --global_scheduler_config_type locality \
        --locality_global_scheduler_config_threshold_of_imbanlance_ratio 2.0)
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
        --vllm_scheduler_config_disk_size 1024GB \
        --vllm_scheduler_config_disk_cpu_thput 4000MB/S \
        --vllm_scheduler_config_cpu_disk_thput 4000MB/S \
        --vllm_scheduler_config_cache_reordering \
        --cluster_config_num_replicas 2 \
        --global_scheduler_config_type locality \
        --locality_global_scheduler_config_threshold_of_imbanlance_ratio 2.0)
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
        --vllm_scheduler_config_disk_size 1024GB \
        --vllm_scheduler_config_disk_cpu_thput 4000MB/S \
        --vllm_scheduler_config_cpu_disk_thput 4000MB/S \
        --vllm_scheduler_config_quant_kv \
        --vllm_scheduler_config_quant_ratio 0.25 \
        --vllm_scheduler_config_decode_place gpu \
        --vllm_scheduler_config_decode_speed 60000 \
        --cluster_config_num_replicas 2 \
        --global_scheduler_config_type locality \
        --locality_global_scheduler_config_threshold_of_imbanlance_ratio 2.0 \
        --cluster_config_p2p_bandwidth_between_nodes 2GB/S)
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
        --vllm_scheduler_config_disk_size 1024GB \
        --vllm_scheduler_config_disk_cpu_thput 4000MB/S \
        --vllm_scheduler_config_cpu_disk_thput 4000MB/S \
        --cluster_config_num_replicas 2 \
        --global_scheduler_config_type locality \
        --locality_global_scheduler_config_threshold_of_imbanlance_ratio 2.0 \
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


allowed_error_for_throughput=0.1
allowed_error_for_qps_scale=0.05
if [ $# -lt 2 ]; then
    echo "Usage: $0 <paper> <trace> [optional: allowed_error_for_throughput] [optional: allowed_error_for_qps_scale]"
    exit 1
elif [ $# -eq 3 ]; then
    allowed_error_for_throughput=$3
elif [ $# -eq 4 ]; then
    allowed_error_for_throughput=$3
    allowed_error_for_qps_scale=$4
fi
source .venv/bin/activate
paper_name=$1
config_name=$2

# Check if config_name.jsonl exists
if [ ! -f "$config_name.jsonl" ]; then
    echo "$config_name.jsonl generation."
    python -m llmkvb.main \
        --llmkvb_config "$config_dir_path$config_name.yaml" \
        --llmkvb_trace_output_file "$config_name".jsonl \
        --llmkvb_tracegen_only
fi

# if paper_name is baseline
max_qps_scale=1.8

# Find a qps_scale that is big enough.
max_result=$(run_exp $paper_name $config_name $max_qps_scale)
# Get the first line of this string.
max_qps_throughput=$(echo $max_result | cut -d' ' -f1)
max_qps_avg_ttft=$(echo $max_result | cut -d' ' -f2)
max_qps=$(echo $max_result | cut -d' ' -f3)
echo "max qps $max_qps"
echo "max qps throughput $max_qps_throughput"

left_qps_scale=0.2
right_qps_scale="$max_qps_scale"
the_throughput=0
the_qps=0
the_avg_ttft=0

qps_list=""
throughput_list=""
avg_ttft_list=""
# binary seach until throughput close enough to max_qps_throughput
while [ $(echo "$right_qps_scale - $left_qps_scale > $allowed_error_for_qps_scale" | bc -l) -eq 1 ]; do
    qps_scale=$(echo "($left_qps_scale + $right_qps_scale) / 2" | bc -l)
    echo ""
    echo "Running with qps_scale $qps_scale"
    result=$(run_exp $paper_name $config_name $qps_scale)
    throughput=$(echo $result | cut -d' ' -f1)
    avg_ttft=$(echo $result | cut -d' ' -f2)
    real_qps=$(echo $result | cut -d' ' -f3)
    echo "qps: $real_qps"
    echo "thput: $throughput"
    echo "avg_ttft: $avg_ttft"
    the_throughput=$throughput
    the_avg_ttft=$avg_ttft
    the_qps=$real_qps
    if [ ${#qps_list} -eq 0 ]; then
        qps_list="$real_qps"
        throughput_list="$throughput"
        avg_ttft_list="$avg_ttft"
    else
        qps_list="$qps_list,$real_qps"
        throughput_list="$throughput_list,$throughput"
        avg_ttft_list="$avg_ttft_list,$avg_ttft"
    fi
    if [ $(echo "$max_qps_throughput - $throughput > $allowed_error_for_throughput" | bc -l) -eq 1 ]; then
        # Not enough throughput, increase qps_scale
        left_qps_scale=$qps_scale
    else
        right_qps_scale=$qps_scale
    fi
    echo ""
done
plot_dir="exps/$config_name/$paper_name"
mkdir -p $plot_dir
python3 runqpsdisk_plot.py $plot_dir $qps_list $throughput_list $avg_ttft_list
echo ""
echo "qps to get max throughput: $the_qps"
echo "Throughput: $the_throughput"
echo "Average ttft: $the_avg_ttft"


