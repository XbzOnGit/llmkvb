#!/bin/bash
papers="baseline ragcache cachedattention cachegen"
# assert paper len > 0
if [ -z "$papers" ]; then
    echo "Please specify the papers to run"
    exit 1
fi
if [ $# -lt 4 ]; then
    echo "Usage: $0 <trace> <qps_scale_start> <qps_scale_interval> <point_number>"
    exit 1
fi
config_name=$1
qps_scale_start=$2
qps_scale_interval=$3
point_number=$4
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
python3 rundisk_line_plot.py $param_list