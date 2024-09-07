#!/bin/bash
# Run on a trace && CPU+GPU+DISK setup.
# Then plot throughput(qps just big enough) and corresponding avg ttft.
if [ $# -ne 1 ]; then
    echo "Usage: $0 <config_name>"
    exit 1
fi
papers="baseline cachedattention ragcache"
throughput_list=""
avg_ttft_list=""
paper_name_list=""
config_name=$1
for paper in $papers; do
    echo "Running $paper"
    result_str=$(./runqpsdisk.sh $paper $config_name)
    # qps=$(echo $result_str | grep -oP "qps to get to max throughput: \K[0-9.]+")
    # For now, ignore the threshold qps.
    throughput=$(echo $result_str | grep -oP "Throughput: \K[0-9.]+")
    avg_ttft=$(echo $result_str | grep -oP "Average ttft: \K[0-9.]+")
    echo "$paper, throughput: $throughput, avg_ttft: $avg_ttft"
    echo ""
    if [ ${#throughput_list} -eq 0 ]; then
        throughput_list="$throughput"
        avg_ttft_list="$avg_ttft"
        paper_name_list="$paper"
    else
        throughput_list="$throughput_list,$throughput"
        avg_ttft_list="$avg_ttft_list,$avg_ttft"
        paper_name_list="$paper_name_list,$paper"
    fi
done
plot_dir="exps/$config_name"
# echo "python3 rundisk_plot.py $plot_dir $config_name $paper_name_list $throughput_list $avg_ttft_list"
python3 rundisk_plot.py $plot_dir $config_name $paper_name_list $throughput_list $avg_ttft_list