#!/bin/bash
config_names="trace_cache_30000 trace_cache_100000 trace_cache_1000000 trace_cache_3000000"
for config_name in $config_names
do
    echo ""
    echo "Plotting $config_name with GPU+CPU+DISK"
    ./rundisk.sh $config_name
    echo ""
done