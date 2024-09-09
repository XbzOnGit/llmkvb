#!/bin/bash
config_names="3000000_0234 3000000_0474 3000000_0533 3000000_0551"
for config_name in $config_names
do
    echo ""
    echo "Plotting $config_name with GPU+CPU+DISK"
    ./rundisk.sh $config_name
    echo ""
done