import sys
import os
from matplotlib import pyplot as plt
if __name__ == '__main__':
    assert len(sys.argv) == 3, 'Usage: python rundisk_line_plot.py <output_dir> <param_list>'
    markers = ['o', 's', 'D', '^', 'v', 'p', 'P', '*', 'X', 'H']
    output_dir = sys.argv[1]
    os.makedirs(output_dir, exist_ok=True)
    param_list = sys.argv[2]
    dump_file = output_dir + "/param_list.txt"
    print(f"param_list: {param_list}")
    with open(dump_file, 'w') as f:
        f.write(param_list)
    paper_name_end = param_list.find(';')
    paper_names = param_list[:paper_name_end].split('~')
    param_list = param_list[paper_name_end+1:]
    results_list = param_list.split(';')
    general_qps_list = []
    general_throughput_list = []
    general_avg_ttft_list = []
    for i in range(len(paper_names)):
        paper_name = paper_names[i]
        result_pack = results_list[i].split('-')
        qps_list = result_pack[0].split(',')
        throughput_list = result_pack[1].split(',')
        avg_ttft_list = result_pack[2].split(',')
        print(f"paper_name: {paper_name}")
        print(f"qps_list: {qps_list}")
        print(f"throughput_list: {throughput_list}")
        print(f"avg_ttft_list: {avg_ttft_list}")
        qps_list = [float(qps) for qps in qps_list] # x-axis
        throughput_list = [float(throughput) for throughput in throughput_list] # y-axis for graph 1.
        avg_ttft_list = [float(avg_ttft) for avg_ttft in avg_ttft_list] # y-axis for graph 2.
        general_qps_list.append(qps_list)
        general_throughput_list.append(throughput_list)
        general_avg_ttft_list.append(avg_ttft_list)
    
    last_output_dir = output_dir.split('/')[-1]
    plt.figure(figsize=(20,10))
    plt.suptitle(f"{last_output_dir}")
    plt.subplot(1, 2, 1)
    for i in range(len(paper_names)):
        # Add different markers.
        plt.plot(general_qps_list[i], general_throughput_list[i], label=paper_names[i], marker=markers[i])
    plt.xlabel("QPS")
    plt.ylabel("Throughput req/s")
    plt.legend()
    plt.subplot(1, 2, 2)
    for i in range(len(paper_names)):
        plt.plot(general_qps_list[i], general_avg_ttft_list[i], label=paper_names[i], marker=markers[i])
    plt.xlabel("QPS")
    plt.ylabel("AvgTTFT second")
    plt.legend()
    plt.savefig(f"./{output_dir}/qps_throughput_avg_ttft_original.png")

