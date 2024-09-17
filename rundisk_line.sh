#!/bin/bash
papers="baseline ragcache cachedattention cachegen cacheblend"
# assert paper len > 0
if [ -z "$papers" ]; then
    echo "Please specify the papers to run"
    exit 1
fi
if [ $# -lt 5 ]; then
    echo "Usage: $0 <trace> <output dir> <qps_scale_start> <qps_scale_interval> <point_number>"
    exit 1
fi
config_name=$1
output_dir=$2
qps_scale_start=$3
qps_scale_interval=$4
point_number=$5
param_list=""
for paper in $papers; do
    if [ ${#param_list} -eq 0 ]; then
        param_list="$paper"
    else
        param_list="$param_list~$paper"
    fi
done
# baseline~cachedattention~cachegen
for paper in $papers; do
    echo "Running $paper $config_name"
    result=$(./runqpsdisk_line.sh $paper $config_name $qps_scale_start $qps_scale_interval $point_number)
    # echo $result
    qps_list=$(echo $result | grep -oP '(?<=qps_list: )\S+')
    # echo $qps_list
    throughput_list=$(echo $result | grep -oP '(?<=throughput_list: )\S+')
    # echo $throughput_list
    avg_ttft_list=$(echo $result | grep -oP '(?<=avg_ttft_list: )\S+')
    # echo $avg_ttft_list
    param_list="$param_list;$qps_list-$throughput_list-$avg_ttft_list"
done
python3 rundisk_line_plot.py $output_dir $param_list